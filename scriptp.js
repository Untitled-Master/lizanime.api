const base_url = "https://lizanime-api.onrender.com";

function addFavoriteAnime() {
  const name = document.getElementById("animeName").value.trim();
  const rating = document.getElementById("animeRating").value.trim();

  if (!name || !rating) {
    alert("Please enter both anime name and rating.");
    return;
  }

  const data = { name, rating };
  fetch(`${base_url}/add_anime`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (response.ok) {
      document.getElementById("animeName").value = '';
      document.getElementById("animeRating").value = '';
      fetchFavoriteAnimes(); // Corrected function name
    } else {
      throw new Error('Failed to add favorite anime.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to add favorite anime. Please try again.');
  });
}

function fetchFavoriteAnimes() { // Corrected function name
  fetch(`${base_url}/get_animes`)
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to fetch favorite animes.');
    }
    return response.json();
  })
  .then(animes => {
    const favoriteAnimes = document.getElementById("favoriteAnimes");
    favoriteAnimes.innerHTML = '';
    animes.forEach(anime => {
      const p = document.createElement('p');
      p.textContent = `- ${anime.name} (Rating: ${anime.rating})`;
      favoriteAnimes.appendChild(p);
    });
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to fetch favorite animes. Please try again.');
  });
}

// Fetch favorite animes when the page loads
window.onload = fetchFavoriteAnimes;
