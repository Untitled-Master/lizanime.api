document.addEventListener('DOMContentLoaded', async function () {
    const loadingContainer = document.getElementById('loading-container');
    const episodesContainer = document.getElementById('episodes');
    loadingContainer.style.display = 'block'; // Show loading container

    try {
        const response = await fetch('https://lizanime-api.onrender.com/movie_data');
        const responseData = await response.json();
        const animeData = responseData.anime_data;

        animeData.forEach(episode => {
            const episodeCard = document.createElement('div');
            episodeCard.classList.add('episode-card');

            const episodeImg = document.createElement('img');
            episodeImg.src = episode['Image URL'];
            episodeImg.alt = episode['Title'];

            const episodeInfo = document.createElement('div');
            episodeInfo.classList.add('episode-info');

            const episodeTitle = document.createElement('h2');
            episodeTitle.classList.add('episode-title');
            episodeTitle.textContent = episode['Title'];

            const episodeGenre = document.createElement('p');
            episodeGenre.textContent = `Genre: ${episode['Genre']}`;

            const episodeYear = document.createElement('p');
            episodeYear.textContent = `Year: ${episode['Year']}`;

            const episodeRating = document.createElement('p');
            episodeRating.textContent = `Rating: ${episode['Rating']}`;

            const serverLinks = episode['Server Links'];
            if (serverLinks.length > 0) {
                const serverList = document.createElement('ul');
                serverLinks.forEach((link, index) => {
                    const listItem = document.createElement('li');
                    const serverButton = document.createElement('button');
                    serverButton.classList.add('server-button');
                    serverButton.textContent = `Server ${index + 1}`;
                    serverButton.addEventListener('click', () => {
                        window.open(link, '_blank');
                    });
                    listItem.appendChild(serverButton);
                    serverList.appendChild(listItem);
                });
                episodeInfo.appendChild(serverList);
            } else {
                const noServers = document.createElement('p');
                noServers.textContent = 'No servers available.';
                episodeInfo.appendChild(noServers);
            }
            episodeCard.appendChild(episodeTitle);
            episodeInfo.appendChild(episodeGenre);
            episodeInfo.appendChild(episodeYear);
            episodeInfo.appendChild(episodeRating);

            episodeCard.appendChild(episodeImg);
            episodeCard.appendChild(episodeInfo);

            episodesContainer.appendChild(episodeCard);
        });

        loadingContainer.style.display = 'none'; // Hide loading container after data is loaded
    } catch (error) {
        console.error('Error fetching data:', error);
        loadingContainer.textContent = 'Error fetching data. Please try again later.';
    }
});
