const API_URL = 'http://127.0.0.1:8000/predict';

const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const statusMessage = document.getElementById('statusMessage');

const cityNameEl = document.getElementById('cityName');
const rainChanceEl = document.getElementById('rainChance');
const rainForecastStatusEl = document.getElementById('rainForecastStatus');
const rainBadgeEl = document.getElementById('rainBadge');
const heroWeatherIconEl = document.getElementById('heroWeatherIcon');

const detailCityEl = document.getElementById('detailCity');
const detailDateEl = document.getElementById('detailDate');
const detailRainEl = document.getElementById('detailRain');
const detailProbEl = document.getElementById('detailProb');

async function fetchWeather(city) {
  if (!city || city.trim() === '') return;

  // Show loading state
  statusMessage.className = 'status-message loading';
  statusMessage.textContent = `Fetching rain prediction for ${city}...`;

  try {
    const response = await fetch(`${API_URL}?city=${encodeURIComponent(city.trim())}`);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to fetch weather prediction' }));
      throw new Error(errorData.detail || 'City not found or server error.');
    }

    const data = await response.json();
    
    // Hide status message on success
    statusMessage.className = 'status-message hidden';
    
    updateUI(data);
  } catch (err) {
    statusMessage.className = 'status-message error';
    statusMessage.textContent = err.message || 'Error connecting to backend service.';
  }
}

function updateUI(data) {
  // data format: { city: "Madrid, Spain", date: "2026-08-27", rain_tomorrow: "NO", rain_probability: "0.00%" }
  cityNameEl.textContent = data.city;
  rainChanceEl.textContent = data.rain_probability;
  
  const willRain = data.rain_tomorrow === 'YES';

  if (willRain) {
    rainForecastStatusEl.textContent = 'RAIN EXPECTED';
    rainBadgeEl.textContent = 'Rain Tomorrow: YES';
    rainBadgeEl.className = 'prediction-badge yes-rain';
    heroWeatherIconEl.textContent = '🌧️';
  } else {
    rainForecastStatusEl.textContent = 'NO RAIN';
    rainBadgeEl.textContent = 'Rain Tomorrow: NO';
    rainBadgeEl.className = 'prediction-badge no-rain';
    heroWeatherIconEl.textContent = '☀️';
  }

  detailCityEl.textContent = data.city;
  detailDateEl.textContent = data.date;
  detailRainEl.textContent = data.rain_tomorrow;
  detailProbEl.textContent = data.rain_probability;
}

function searchCity(cityName) {
  cityInput.value = cityName;
  fetchWeather(cityName);
}

searchBtn.addEventListener('click', () => {
  fetchWeather(cityInput.value);
});

cityInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    fetchWeather(cityInput.value);
  }
});

// Initial load for default city
window.addEventListener('DOMContentLoaded', () => {
  fetchWeather('Madrid');
});
