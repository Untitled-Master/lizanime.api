from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/anime_episodes', methods=['GET'])
def get_anime_episodes():
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

            # Combine the data into a single dictionary and append to anime_data list
            anime_data.append({
                'title': title,
                'url': link,
                'img_url': img_url,
                'episode': episode,
                'year': year
            })

        return jsonify(anime_data)

    else:
        return jsonify({'error': 'Nothing was found'})

if __name__ == '__main__':
    app.run(debug=True)
