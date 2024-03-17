from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import psycopg2

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database URL provided by Render
db_url = "postgres://untitledmaster:TRpOF79DgGJfadr9MxV0RzLCtQtPIm59@dpg-cnrie1v109ks73fgq4gg-a.oregon-postgres.render.com/lizanime"


def create_table():
    try:
        # Establish a connection to the PostgreSQL database using the database URL
        conn = psycopg2.connect(db_url)

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # Example SQL command: Create a table named 'favorite_animes' if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS favorite_animes
                        (id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        rating INTEGER NOT NULL)''')

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        print("Table 'favorite_animes' created successfully.")

    except psycopg2.Error as e:
        print("Error creating table:", e)

@app.route('/add_anime', methods=['POST'])
def add_favorite_anime():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract anime name and rating from the JSON data
        name = data.get('name')
        rating = data.get('rating')

        # Check if name and rating are provided
        if not name or not rating:
            return jsonify({'error': 'Name and rating are required.'}), 400

        # Establish a connection to the PostgreSQL database using the database URL
        conn = psycopg2.connect(db_url)

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # Example SQL command: Insert data into the 'favorite_animes' table
        cursor.execute("INSERT INTO favorite_animes (name, rating) VALUES (%s, %s)", (name, rating))

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return jsonify({'message': f"Saved '{name}' as a favorite anime with rating {rating}."}), 201

    except psycopg2.Error as e:
        return jsonify({'error': 'Error connecting to the database.'}), 500

@app.route('/get_animes', methods=['GET'])
def get_favorite_animes():
    try:
        # Establish a connection to the PostgreSQL database using the database URL
        conn = psycopg2.connect(db_url)

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # Example SQL query: Select all data from the 'favorite_animes' table
        cursor.execute("SELECT * FROM favorite_animes")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Convert the rows to a list of dictionaries
        animes = [{'id': row[0], 'name': row[1], 'rating': row[2]} for row in rows]

        return jsonify(animes)

    except psycopg2.Error as e:
        return jsonify({'error': 'Error connecting to the database.'}), 500

@app.route('/anime_episodes1', methods=['GET'])
def get_anime_episodes():
    anime = request.args.get('anime')
    if anime:
        url = f'https://xsaniime.com/anime/{anime}/'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            episodes_div = soup.find('div', id='episodes')
            anime_data = []

            if episodes_div:
                episodes_list = episodes_div.find_all('li')

                for episode_li in episodes_list:
                    episode_url = episode_li.a['href']
                    episode_name = episode_li.a['title']

                    episode_response = requests.get(episode_url)
                    if episode_response.status_code == 200:
                        episode_soup = BeautifulSoup(episode_response.text, 'html.parser')
                        data_embed_links = episode_soup.find_all(attrs={"data-embed": True})
                        data_embed = [link['data-embed'] for link in data_embed_links]
                    else:
                        data_embed = []

                    anime_data.append({
                        'title': episode_name,
                        'urls': data_embed,
                    })

                return jsonify(anime_data)
            else:
                return jsonify({'error': 'No episodes found.'}), 404
        else:
            return jsonify({'error': 'Failed to fetch the webpage.'}), 500
    else:
        return jsonify({'error': 'Anime name parameter missing.'}), 400

@app.route('/anime_data', methods=['GET'])
def get_anime_data():
    url = 'https://x.xsanime.com/episodes/'
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all the div elements with class "block-post"
        episode_divs = soup.find_all('div', class_='block-post')
        anime_data = []
        for episode_div in episode_divs:
            # Find the <a> element within the div
            episode_link = episode_div.find('a')
            # Extract the href attribute (link) and the image URL
            link = episode_link['href']
            title = episode_link['title']
            img_url = episode_link.find('img')['data-img']
            episode = episode_link.find('span', class_='episode').text.strip()
            year = episode_link.find('span', class_='year').text.strip()
            response2 = requests.get(link)
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            episode_urls = soup2.find_all('div', class_='servList')
            episode_servers = []
            for episode_url in episode_urls:
                data_embed_links = episode_url.find_all(attrs={"data-embed": True})
                for i, linky in enumerate(data_embed_links, 1):
                    urll = linky['data-embed']
                    episode_servers.append({f'url{i}': urll})
            anime_data.append({
                'title': title,
                'url': link,
                'img_url': img_url,
                'episode': episode,
                'year': year,
                'urls': episode_servers,
            })
        return jsonify(anime_data)
    else:
        return jsonify({'message': 'Nothing was found'})

@app.route('/anime_datapro', methods=['GET'])
def get_anime_datapro():
    url = 'https://xsaniime.com/'
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all the div elements with class "block-post"
        episode_divs = soup.find_all('div', class_='block-post')
        anime_data = []
        for episode_div in episode_divs:
            # Find the <a> element within the div
            episode_link = episode_div.find('a')
            # Extract the href attribute (link) and the image URL
            link = episode_link['href']
            title = episode_link['title']
            img_url = episode_link.find('img')['data-img']
            year = episode_link.find('span', class_='year').text.strip()

            # Check if there is an episode link
            if 'episode' in link:
                tag = 'episode'
            elif 'movie' in link:
                tag = 'movie'
            else:
                tag = 'anime'

            response2 = requests.get(link)
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            episode_urls = soup2.find_all('div', class_='servList')
            episode_servers = []
            for episode_url in episode_urls:
                data_embed_links = episode_url.find_all(attrs={"data-embed": True})
                for i, linky in enumerate(data_embed_links, 1):
                    urll = linky['data-embed']
                    episode_servers.append({f'url{i}': urll})
            anime_data.append({
                'title': title,
                'url': link,
                'img_url': img_url,
                'year': year,
                'tag': tag,
                'urls': episode_servers,
            })
        return jsonify(anime_data)
    else:
        return jsonify({'message': 'Nothing was found'})


if __name__ == '__main__':
    create_table()  # Create the 'favorite_animes' table if it doesn't exist
    app.run(host='0.0.0.0', port=5000, debug=False)
