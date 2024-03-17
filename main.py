from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
                tag = 'episode'
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
    app.run(host='0.0.0.0', port=5000, debug=False)
