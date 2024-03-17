document.addEventListener('DOMContentLoaded', async function () {
    const loadingContainer = document.getElementById('loading-container');
    const newEpisodesGrid = document.getElementById('new-episodes-grid');
    const animeGrid = document.getElementById('anime-grid');
    const moviesGrid = document.getElementById('movies-grid');
    loadingContainer.style.display = 'block'; // Show loading container

    try {
        const response = await fetch('https://lizanime-api.onrender.com/anime_datapro');
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

            episode.servers.forEach((server, index) => {
                const serverButton = document.createElement('button');
                serverButton.classList.add('server-button');
                serverButton.textContent = `Server ${index + 1}`;
                serverButton.addEventListener('click', () => {
                    window.open(server, '_blank');
                });

                serverButtons.appendChild(serverButton);
            });

            episodeInfo.appendChild(episodeTitle);
            episodeInfo.appendChild(serverButtons);

            episodeCard.appendChild(episodeImg);
            episodeCard.appendChild(episodeInfo);

            if (episode.tag === 'anime') {
                animeGrid.appendChild(episodeCard);
            } else if (episode.tag === 'movie') {
                moviesGrid.appendChild(episodeCard);
            } else {
                newEpisodesGrid.appendChild(episodeCard);
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }

    loadingContainer.style.display = 'none'; // Hide loading container after data is loaded
});
