from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import psycopg2
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from github import Github, GithubException

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


username_placeholder = "USERNAME"  # Replace with actual placeholder text
rating_placeholder = "RATING"  # Replace with actual placeholder text
playtime_placeholder = "PLAYTIME HOURS"  # Replace with actual placeholder text

def get_svg_content(username):
  # Simulate fetching user data (replace with your actual logic)
  ratings = {"rapid": 1500, "blitz": 1600, "bullet": 1700}
  playtime = 100

  svg_content = f"""
<svg width="800" height="400">
  <rect x="0" y="0" width="800" height="400" fill="#0a0a0a" />

  <g transform="translate(50, 50)">
    <circle cx="50" cy="50" r="50" fill="#f5f5f5" />
    <text x="50" y="120" font-size="22" fill="#f5f5f5">{username}</text>

    <circle cx="100" cy="150" r="5" fill="#4a4a4a" /> 
    <text x="110" y="155" font-size="12" fill="#f5f5f5">Offline</text>
  </g>

  <g transform="translate(450, 50)">
    <g transform="translate(0, 0)">
      <text x="0" y="20" font-size="18" fill="#f5f5f5">Rapid:</text>
      <text x="70" y="20" font-size="18" fill="#f5f5f5">{ratings['rapid']}</text>
      <path d="M20 5 L25 10 L15 10 Z" fill="#f5f5f5" transform="translate(50, 0)" /> </g>
    <g transform="translate(0, 50)">
      <text x="0" y="20" font-size="18" fill="#f5f5f5">Blitz:</text>
      <text x="60" y="20" font-size="18" fill="#f5f5f5">{ratings['blitz']}</text>
      <path d="M10 5 L15 10 L5 10 Z" fill="#f5f5f5" transform="translate(40, 0)" /> </g>
    <g transform="translate(0, 100)">
      <text x="0" y="20" font-size="18" fill="#f5f5f5">Bullet:</text>
      <text x="65" y="20" font-size="18" fill="#f5f5f5">{ratings['bullet']}</text>
      <path d="M20 5 L15 15 L25 15 Z" fill="#f5f5f5" transform="translate(40, 0)" /> </g>
    <g transform="translate(0, 150)">
      <text x="0" y="20" font-size="18" fill="#f5f5f5">Playtime:</text>
      <text x="100" y="20" font-size="18" fill="#f5f5f5">{playtime}</text>
    </g>
  </g>
</svg>
"""
  # Replace placeholders with actual values
  svg_content = svg_content.replace(username_placeholder, username)
  svg_content = svg_content.replace(rating_placeholder, rating_placeholder)  # Update once you implement user data retrieval
  svg_content = svg_content.replace(playtime_placeholder, playtime)  # Update once you implement user data retrieval
  return svg_content

@app.route("/user")
username = "dzdz"
def user_svg(username):
  svg_data = get_svg_content(username)
  response = make_response(svg_data)
  response.headers['Content-Type'] = 'image/svg+


url = 'https://www.fushaar.com/'



def fetch_server_links(link):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        servers = soup.find_all('div', class_='jtab')
        server_links = [server.find('iframe')['data-lazy-src'] if server.find('iframe') else None for server in servers]
        return server_links
    else:
        return []

@app.route('/movie_data', methods=['GET'])
def get_movie_data():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movies = soup.find_all('article', class_='poster')
        anime_data = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_link = {executor.submit(fetch_server_links, movie.find('a')['href']): movie for movie in movies}
            for future in concurrent.futures.as_completed(future_to_link):
                movie = future_to_link[future]
                try:
                    server_links = future.result()
                except Exception as exc:
                    print(f"Error fetching server links for {movie.find('a')['href']}: {exc}")
                    server_links = []

                title = movie.find('div', class_='info').find('h3').get_text(strip=True)
                img_url = movie.find('a').find('img')['data-lazy-src']
                genre = movie.find('div', class_='gerne').get_text(strip=True)
                year = movie.find('ul', class_='labels').find('li', class_='year').get_text(strip=True)
                rating = movie.find('div', class_='rate').find('span', class_='greyinfo').get_text(strip=True)

                movie_info = {
                    'Title': title,
                    'Link': movie.find('a')['href'],
                    'Image URL': img_url,
                    'Genre': genre,
                    'Year': year,
                    'Rating': rating,
                    'Server Links': server_links
                }
                anime_data.append(movie_info)


        response_data = {
            'anime_data': anime_data,
        }

        return jsonify(response_data)

    else:
        return jsonify({'error': f"Failed to fetch the page. Status code: {response.status_code}"}), 500

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



# GitHub configuration
GITHUB_TOKEN = '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'
REPO_NAME = 'Untitled-Master/Data'
BRANCH = 'main'  # Change this to the branch where you want to commit the changes

# Authenticate to GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the file content
        content = file.read()
        path_in_repo = file.filename

        try:
            # Check if the file exists in the repo
            contents = repo.get_contents(path_in_repo, ref=BRANCH)
            repo.update_file(contents.path, f"Update {file.filename} via API", content, contents.sha, branch=BRANCH)
            return jsonify({"message": f"Updated file {path_in_repo} in the repository."}), 200
        except GithubException as e:
            if e.status == 404:
                # File does not exist, create it
                repo.create_file(path_in_repo, f"Create {file.filename} via API", content, branch=BRANCH)
                return jsonify({"message": f"Created file {path_in_repo} in the repository."}), 201
            else:
                raise

    except GithubException as e:
        return jsonify({"error": f"GitHub exception: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = repo.get_contents('')
        file_list = [file.path for file in files]
        return jsonify({"files": file_list}), 200
    except GithubException as e:
        return jsonify({"error": f"GitHub exception: {e}"}), 500

@app.route('/delete/<path:file_name>', methods=['GET'])
def delete_files(file_name):
    try:
        contents = repo.get_contents(file_name, ref=BRANCH)
        repo.delete_file(contents.path, f"Delete {file_name} via API", contents.sha, branch=BRANCH)
        return jsonify({"message": f"Deleted file {file_name} from the repository."}), 200
    except GithubException as e:
        if e.status == 404:
            return jsonify({"error": f"File {file_name} not found in the repository"}), 404
        else:
            return jsonify({"error": f"GitHub exception: {e}"}), 500

@app.route('/delete', methods=['POST'])
def delete_file():
    file_name = request.json.get('file_name')

    if not file_name:
        return jsonify({"error": "File name not provided"}), 400

    try:
        contents = repo.get_contents(file_name, ref=BRANCH)
        repo.delete_file(contents.path, f"Delete {file_name} via API", contents.sha, branch=BRANCH)
        return jsonify({"message": f"Deleted file {file_name} from the repository."}), 200
    except GithubException as e:
        if e.status == 404:
            return jsonify({"error": f"File {file_name} not found in the repository"}), 404
        else:
            return jsonify({"error": f"GitHub exception: {e}"}), 500

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
    if not anime:
        return jsonify({'error': 'Anime name parameter missing.'}), 400

    url = f'https://xsaniime.com/anime/{anime}/'
    response = requests.get(url)

    def process_episode(episode_li):
        episode_url = episode_li.a['href']
        episode_name = episode_li.a['title']

        episode_response = requests.get(episode_url)
        if episode_response.status_code == 200:
            episode_soup = BeautifulSoup(episode_response.text, 'html.parser')
            data_embed_links = episode_soup.find_all(attrs={"data-embed": True})
            data_embed = [link['data-embed'] for link in data_embed_links]
        else:
            data_embed = []

        return {
            'title': episode_name,
            'urls': data_embed,
        }

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        episodes_div = soup.find('div', id='episodes')

        if episodes_div:
            episodes_list = episodes_div.find_all('li')

            anime_data = []
            with ThreadPoolExecutor() as executor:
                # Process each episode in parallel
                processed_episodes = executor.map(process_episode, episodes_list)
                anime_data.extend(processed_episodes)

            return jsonify(anime_data)
        else:
            return jsonify({'error': 'No episodes found.'}), 404
    else:
        return jsonify({'error': 'Failed to fetch the webpage.'}), 500

@app.route('/anime_data', methods=['GET'])
def get_anime_data():
    url = 'https://x.xsanime.com/episodes/'
    response = requests.get(url)
    
    def process_episode(episode_div):
        episode_link = episode_div.find('a')
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
        
        return {
            'title': title,
            'url': link,
            'img_url': img_url,
            'episode': episode,
            'year': year,
            'urls': episode_servers,
        }
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        episode_divs = soup.find_all('div', class_='block-post')
        
        anime_data = []
        with ThreadPoolExecutor() as executor:
            # Process each episode in parallel
            processed_episodes = executor.map(process_episode, episode_divs)
            anime_data.extend(processed_episodes)
        
        return jsonify(anime_data)
    else:
        return jsonify({'message': 'Nothing was found'})

def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def parse_html(html):
    return BeautifulSoup(html, 'html.parser')

def extract_data(soup, class_name):
    elements = soup.find_all('div', class_=class_name)
    return [element.text.strip() for element in elements]

def scrape_website(search_query):
    url = f"https://www.hdith.com/?s={search_query}"

    html_content = fetch_webpage(url)
    if html_content:
        soup = parse_html(html_content)
        
        valid_data = extract_data(soup, 'hbox faq-item active degree1')
        weak_data = extract_data(soup, 'hbox faq-item active degree2')
        not_valid_data = extract_data(soup, 'hbox faq-item active degree3')
        
        response_data = {
            "Valid": valid_data,
            "Weak": weak_data,
            "Not Valid": not_valid_data
        }
        return response_data
    else:
        return {"error": "Failed to retrieve the webpage."}

@app.route('/scrape2', methods=['GET'])
def scrape2():
    search_query = request.args.get('search')
    if not search_query:
        return jsonify({"error": "Search query is required."}), 400
    
    results = scrape_website(search_query)
    return jsonify(results)


@app.route('/scrape', methods=['GET'])
def scrape_website():
    search_query = request.args.get('search', '')
    url = f"https://www.hdith.com/?s={search_query}"

    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <div> elements with class 'hbox faq-item active degree1'
        valids = soup.find_all('div', class_='hbox faq-item active degree1')
        weaks = soup.find_all('div', class_='hbox faq-item active degree2')
        notValid = soup.find_all('div', class_='hbox faq-item active degree3')

        # Format the data
        valid_data = [valid.text.strip() for valid in valids]
        weak_data = [weak.text.strip() for weak in weaks]
        not_valid_data = [not_valid.text.strip() for not_valid in notValid]

        # Create the response JSON
        response_data = {
            "Valid": valid_data,
            "Weak": weak_data,
            "Not Valid": not_valid_data
        }

        return jsonify(response_data)
    else:
        return jsonify({"error": "Failed to retrieve the webpage."})


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

@app.route('/anime_datavip', methods=['GET'])
def get_anime_datavip():
    url = 'https://xsaniime.com/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        episode_divs = soup.find_all('div', class_='block-post')
        anime_data = []
        
        def process_episode(episode_div):
            episode_link = episode_div.find('a')
            link = episode_link['href']
            title = episode_link['title']
            img_url = episode_link.find('img')['data-img']
            year = episode_link.find('span', class_='year').text.strip()

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
        
        with ThreadPoolExecutor() as executor:
            executor.map(process_episode, episode_divs)
        
        return jsonify(anime_data)
    else:
        return jsonify({'message': 'Nothing was found'})
if __name__ == '__main__':
    create_table()  # Create the 'favorite_animes' table if it doesn't exist
    app.run(host='0.0.0.0', port=5000, debug=False)
