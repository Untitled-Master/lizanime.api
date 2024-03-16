document.addEventListener('DOMContentLoaded', async function () {
    const loadingContainer = document.getElementById('loading-container');
    const episodesContainer = document.getElementById('episodes');
    loadingContainer.style.display = 'block'; // Show loading container

    try {
        const response = await fetch('https://lizanime-api.onrender.com/anime_data');
        const data = await response.json();

        data.forEach(episode => {
            const episodeCard = document.createElement('div');
            episodeCard.classList.add('episode-card');

            const episodeImg = document.createElement('img');
            episodeImg.src = episode.img_url;
            episodeImg.alt = episode.title;

            const episodeInfo = document.createElement('div');
            episodeInfo.classList.add('episode-info');

            // Remove "إكس إس أنمي" from the episode title
            const titleWithoutXSAnime = episode.title.replace('إكس إس أنمي', '');

            const episodeTitle = document.createElement('h2');
            episodeTitle.classList.add('episode-title');
            episodeTitle.textContent = titleWithoutXSAnime;

            const serverButtons = document.createElement('div');
            serverButtons.classList.add('server-buttons');

            episode.urls.forEach((url, index) => {
                const serverButton = document.createElement('button');
                serverButton.classList.add('server-button');
                serverButton.textContent = `server ${index + 1}`;
                serverButton.addEventListener('click', () => {
                    window.open(url['url' + (index + 1)], '_blank');
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
