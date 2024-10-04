import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

TMDB_API_KEY = '232e1da47319aca68ffc137913eb23ba'
JIKAN_API_BASE = 'https://api.jikan.moe/v4'

GENRE_MAP = {
    28: 'Action', 12: 'Adventure', 35: 'Comedy', 18: 'Drama',
    14: 'Fantasy', 27: 'Horror', 10749: 'Romance',
    878: 'Science Fiction', 53: 'Thriller'
}

ANIME_GENRE_MAP = {
    1: 'Action', 2: 'Adventure', 3: 'Carrying', 4: 'Comedy',
    5: 'Demon', 6: 'Fantasy', 7: 'Game', 8: 'Horror',
    9: 'Josei', 10: 'Kids', 11: 'Magic', 12: 'Martial Arts',
    13: 'Mecha', 14: 'Music', 15: 'Mystery', 16: 'Psychological',
    17: 'Romance', 18: 'Samurai', 19: 'Sci-Fi', 20: 'Slice of Life',
    21: 'Supernatural', 22: 'Military', 23: 'Historical', 24: 'Sports'
}

def fetch_movie_data(title: str) -> dict:
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}')
    movie_data = response.json()
    return movie_data['results'][0] if movie_data.get('results') else None

def fetch_similar_movies(genre_ids: list[int], num_movies: int = 20) -> list[dict]:
    genre_str = ','.join(map(str, genre_ids))
    response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_str}&sort_by=popularity.desc')
    movie_data = response.json()
    return movie_data['results'][:num_movies] if movie_data.get('results') else []

def fetch_anime_data(title: str) -> dict:
    response = requests.get(f'{JIKAN_API_BASE}/anime?q={title}&limit=1')
    anime_data = response.json()
    return anime_data['data'][0] if anime_data.get('data') else None

def fetch_similar_anime(genre_ids: list[int], num_anime: int = 20) -> list[dict]:
    genre_str = ','.join(map(str, genre_ids))
    response = requests.get(f'{JIKAN_API_BASE}/anime?genres={genre_str}&limit={num_anime}')
    anime_data = response.json()
    return anime_data['data'] if anime_data.get('data') else []

def fetch_manga_data(title: str) -> dict:
    response = requests.get(f'{JIKAN_API_BASE}/manga?q={title}&limit=1')
    manga_data = response.json()
    return manga_data['data'][0] if manga_data.get('data') else None

def fetch_similar_manga(genre_ids: list[int], num_manga: int = 20) -> list[dict]:
    genre_str = ','.join(map(str, genre_ids))
    response = requests.get(f'{JIKAN_API_BASE}/manga?genres={genre_str}&limit={num_manga}')
    manga_data = response.json()
    return manga_data['data'] if manga_data.get('data') else []

def build_content_filtering(content_data: list[dict]) -> tuple[pd.DataFrame, list[list[float]]]:
    df = pd.DataFrame(content_data)
    if 'genre_ids' in df.columns:
        df['genre_str'] = df['genre_ids'].apply(lambda ids: ' '.join(GENRE_MAP.get(genre_id, '') for genre_id in ids))
    count_vectorizer = CountVectorizer(stop_words='english')
    count_matrix = count_vectorizer.fit_transform(df['genre_str'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    return df, cosine_sim

def get_genre_choices(genres_map: dict) -> list[int]:
    print("Select your favorite genres from the list below (separate choices with commas):")
    for genre_id, genre_name in genres_map.items():
        print(f"{genre_id}. {genre_name}")
    genres_input = input("Enter the numbers corresponding to your preferred genres (e.g., 1,3): ")
    return [int(genre.strip()) for genre in genres_input.split(',')]

def get_recommendations(df: pd.DataFrame, cosine_sim: list[list[float]], idx: int, num_recommendations: int = 3, user_movie_ids: list[int] = []) -> list[str]:
    sim_scores = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)
    recommendations = []
    for i in range(1, len(sim_scores)):
        movie_idx = sim_scores[i][0]
        movie_id = df.iloc[movie_idx]['id']
        if movie_id not in user_movie_ids:
            recommendations.append(df.iloc[movie_idx]['title'])
            if len(recommendations) == num_recommendations:
                break
    return recommendations

def main():
    content_type = input("What type of content do you want recommendations for?\nEnter 'movie', 'anime', or 'manga': ").strip().lower()
    
    content_data = []
    user_movie_titles = []
    user_movie_ids = []
    
    num_entries = int(input(f"Enter the desired number of {content_type}(s) you want to input: "))
    
    for i in range(num_entries):
        title = input(f"{content_type.capitalize()} {i + 1}: ").strip()
        if content_type == 'movie':
            movie_info = fetch_movie_data(title)
            if movie_info:
                print(f"Movie data for {title}: {movie_info}")
                user_movie_titles.append(title)
                user_movie_ids.append(movie_info['id'])
                content_data.append({
                    'id': movie_info['id'],
                    'title': movie_info['title'],
                    'genre_ids': movie_info['genre_ids'],
                    'overview': movie_info.get('overview', ''),
                    'release_date': movie_info.get('release_date', ''),
                    'vote_average': movie_info.get('vote_average', 0),
                    'vote_count': movie_info.get('vote_count', 0)
                })
            else:
                print(f"No data found for {title}")
        elif content_type == 'anime':
            anime_info = fetch_anime_data(title)
            if anime_info:
                print(f"Anime data for {title}: {anime_info}")
                user_movie_titles.append(title)
                user_movie_ids.append(anime_info['mal_id'])
                content_data.append({
                    'id': anime_info['mal_id'],
                    'title': anime_info['title'],
                    'genre_ids': [genre['mal_id'] for genre in anime_info.get('genres', [])],
                    'overview': anime_info.get('synopsis', ''),
                    'release_date': anime_info.get('aired', {}).get('string', ''),
                    'vote_average': anime_info.get('score', 0),
                    'vote_count': anime_info.get('scored', 0)
                })
            else:
                print(f"No data found for {title}")
        elif content_type == 'manga':
            manga_info = fetch_manga_data(title)
            if manga_info:
                print(f"Manga data for {title}: {manga_info}")
                user_movie_titles.append(title)
                user_movie_ids.append(manga_info['mal_id'])
                content_data.append({
                    'id': manga_info['mal_id'],
                    'title': manga_info['title'],
                    'genre_ids': [genre['mal_id'] for genre in manga_info.get('genres', [])],
                    'overview': manga_info.get('synopsis', ''),
                    'release_date': manga_info.get('published', {}).get('string', ''),
                    'vote_average': manga_info.get('score', 0),
                    'vote_count': manga_info.get('scored', 0)
                })
            else:
                print(f"No data found for {title}")

    if content_type == 'movie':
        genres_selected = get_genre_choices(GENRE_MAP)
        additional_movies = fetch_similar_movies(genres_selected)
        for movie in additional_movies:
            if movie['id'] not in user_movie_ids:
                content_data.append({
                    'id': movie['id'],
                    'title': movie['title'],
                    'genre_ids': movie['genre_ids'],
                    'overview': movie.get('overview', ''),
                    'release_date': movie.get('release_date', ''),
                    'vote_average': movie.get('vote_average', 0),
                    'vote_count': movie.get('vote_count', 0)
                })
    elif content_type == 'anime':
        genres_selected = get_genre_choices(ANIME_GENRE_MAP)
        additional_anime = fetch_similar_anime(genres_selected)
        for anime in additional_anime:
            if anime['mal_id'] not in user_movie_ids:
                content_data.append({
                    'id': anime['mal_id'],
                    'title': anime['title'],
                    'genre_ids': [genre['mal_id'] for genre in anime.get('genres', [])],
                    'overview': anime.get('synopsis', ''),
                    'release_date': anime.get('aired', {}).get('string', ''),
                    'vote_average': anime.get('score', 0),
                    'vote_count': anime.get('scored', 0)
                })
    elif content_type == 'manga':
        genres_selected = get_genre_choices(ANIME_GENRE_MAP)
        additional_manga = fetch_similar_manga(genres_selected)
        for manga in additional_manga:
            if manga['mal_id'] not in user_movie_ids:
                content_data.append({
                    'id': manga['mal_id'],
                    'title': manga['title'],
                    'genre_ids': [genre['mal_id'] for genre in manga.get('genres', [])],
                    'overview': manga.get('synopsis', ''),
                    'release_date': manga.get('published', {}).get('string', ''),
                    'vote_average': manga.get('score', 0),
                    'vote_count': manga.get('scored', 0)
                })

    df, cosine_sim = build_content_filtering(content_data)

    if df is not None and cosine_sim is not None:
        print("Content DataFrame:\n", df)
        recommendations = get_recommendations(df, cosine_sim, 0, num_recommendations=5, user_movie_ids=user_movie_ids)
        print("Recommendations:", recommendations)

if __name__ == "__main__":
    main()
