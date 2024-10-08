# Personalised Recommendation System

## Overview
This project is a content recommendation system that provides personalized suggestions for movies, anime, and manga based on user input. It leverages the TMDB (The Movie Database) API for movie data and the Jikan API for anime and manga information.

## Features
- **Multi-Content Type Support**: Request recommendations for movies, anime, or manga.
- **Genre-Based Recommendations**: Select favorite genres to filter personalized recommendations.
- **Detailed Data Fetching**: Retrieve comprehensive details about each title, including genres, release dates, and ratings.
- **Cosine Similarity**: Compute recommendations based on genre similarities among selected titles.

## Tech Stack
- **Programming Language**: Python
- **Libraries**:
  - `requests`: For HTTP requests to APIs.
  - `pandas`: For data manipulation and analysis.
  - `sklearn`: For machine learning functionalities like cosine similarity.

## APIs Used
- **TMDB API**: Provides data about movies, including titles, genres, and ratings.
- **Jikan API**: Offers information about anime and manga, including genres, descriptions, and user ratings.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/repository-name.git
   cd repository-name
   pip install requests pandas scikit-learn
## Configuration

### Update API Keys
Before running the script, update the API keys in the script:
- Replace `TMDB_API_KEY` with your own TMDB API key.

## Usage

### Running the Script
To run the recommendation system, use the following command in your terminal:

`bash
python recommendation_system.py

### Example
Enter the desired number of movies you want to input: 2
Movie 1: Inception
Movie 2: The Matrix
`Select Preferred Genres: Choose your favorite genres from the list provided (separate choices with commas).
## Example Interaction 
What type of content do you want recommendations for?
Enter 'movie', 'anime', or 'manga': movie
Enter the desired number of movies you want to input: 2
Movie 1: Inception
Movie 2: The Matrix
Select your favorite genres from the list below (separate choices with commas): 
...
Recommendations: ['Interstellar', 'The Prestige', 'Fight Club']


## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## Acknowledgements
TMDB for the movie API.
Jikan API for the anime and manga API.

