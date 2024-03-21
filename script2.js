document.addEventListener('DOMContentLoaded', async function () {
    const loadingContainer = document.getElementById('loading-container');
    const episodesContainer = document.getElementById('episodes');
    loadingContainer.style.display = 'block'; // Show loading container

    try {
        const response = await fetch('https://your-flask-api-url/anime_data');
        const data = await response.json();

        data.forEach(episode => {
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

            const serverButtons = document.createElement('div');
            serverButtons.classList.add('server-buttons');

            episode['Server Links'].forEach((url, index) => {
                const serverButton = document.createElement('button');
                serverButton.classList.add('server-button');
                serverButton.textContent = `Server ${index + 1}`;
                serverButton.addEventListener('click', () => {
                    window.open(url, '_blank');
                });
                serverButtons.appendChild(serverButton);
            });

            episodeInfo.appendChild(episodeTitle);
            episodeInfo.appendChild(serverButtons);

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
