document.addEventListener('DOMContentLoaded', async function () {
    const loadingContainer = document.getElementById('loading-container');
    const episodesContainer = document.getElementById('episodes');
    const moviesContainer = document.getElementById('movies');
  
    loadingContainer.style.display = 'block'; // Show loading container
  
    try {
      const response = await fetch('https://lizanime-api.onrender.com/anime_datavip');
      const data = await response.json();
  
      if (data.length === 0) {
        console.warn("No data received from API");
        // Display message to user or take other actions
      } else {
        data.forEach(episode => {
          if (episode.tag) { // Check for existence of 'tag' property
  
            const episodeCard = document.createElement('div');
            episodeCard.classList.add('episode-card');
  
            const episodeImg = document.createElement('img');
            // Handle cases where img_url might be missing
            episodeImg.src = episode.img_url || ""; // Set empty string if img_url is absent
            episodeImg.alt = episode.title || ""; // Set empty string if title is absent
  
            const episodeInfo = document.createElement('div');
            episodeInfo.classList.add('episode-info');
  
            const episodeTitle = document.createElement('h2');
            episodeTitle.classList.add('episode-title');
  
            // Remove "إكس إس أنمي" from the episode title using regular expression
            const titleWithoutXSAnime = episode.title.replace(/إكس إس أنمي/g, '');
            episodeTitle.textContent = titleWithoutXSAnime;
  
            const serverButtons = document.createElement('div');
            serverButtons.classList.add('server-buttons');
  
            // Check for existence of 'urls' property before iterating
            if (episode.urls) {
              episode.urls.forEach((url, index) => {
                const serverButton = document.createElement('button');
                serverButton.classList.add('server-button');
                serverButton.textContent = `server ${index + 1}`;
                serverButton.addEventListener('click', () => {
                  window.open(url['url' + (index + 1)], '_blank');
                });
                serverButtons.appendChild(serverButton);
              });
            }
  
            episodeInfo.appendChild(episodeTitle);
            if (serverButtons.hasChildNodes()) { // Only append server buttons if there are any
              episodeInfo.appendChild(serverButtons);
            }
  
            episodeCard.appendChild(episodeImg);
            episodeCard.appendChild(episodeInfo);
  
            if (episode.tag === 'movie') {
              moviesContainer.appendChild(episodeCard);
            } else if (episode.tag === 'episode') {
              episodesContainer.appendChild(episodeCard);
            } else {
              console.warn(`Unknown episode tag: ${episode.tag}`); // Handle unexpected tags
            }
          }
        });
      }
  
      loadingContainer.style.display = 'none'; // Hide loading container after data is loaded
    } catch (error) {
      console.error('Error fetching data:', error);
      loadingContainer.textContent = 'Error fetching data. Please try again later.';
    }
  });
  
