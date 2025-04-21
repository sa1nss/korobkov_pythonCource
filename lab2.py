import requests
from datetime import datetime, timedelta
import csv

class MovieDataPreparationTool:
    BASE_URL = "https://api.themoviedb.org/3/discover/movie"
    GENRE_URL = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    HEADERS = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
    }

    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.data = []
        self.genres = {}
        self.fetch_data()

    def fetch_data(self):
        # Fetch genres
        genre_response = requests.get(self.GENRE_URL, headers=self.HEADERS)
        if genre_response.status_code == 200:
            self.genres = {genre['id']: genre['name'] for genre in genre_response.json().get('genres', [])}

        # Fetch movie data
        for page in range(1, self.num_pages + 1):
            url = f"{self.BASE_URL}?include_adult=false&include_video=false&sort_by=popularity.desc&page={page}"
            response = requests.get(url, headers=self.HEADERS)
            if response.status_code == 200:
                self.data.extend(response.json().get('results', []))

    def get_all_data(self):
        return self.data

    def get_filtered_data(self):
        return self.data[3:20:4]

    def get_most_popular_title(self):
        return max(self.data, key=lambda x: x.get('popularity', 0)).get('title', "Unknown")

    def get_titles_with_keywords(self, keywords):
        keywords = set(keywords.lower().split())
        return [movie['title'] for movie in self.data if keywords.intersection(movie.get('overview', '').lower().split())]

    def get_unique_genres(self):
        return frozenset(self.genres.values())

    def delete_movies_with_genre(self, genre_name):
        genre_id = next((k for k, v in self.genres.items() if v.lower() == genre_name.lower()), None)
        if genre_id:
            self.data = [movie for movie in self.data if genre_id not in movie.get('genre_ids', [])]

    def get_most_popular_genres(self):
        genre_count = {}
        for movie in self.data:
            for genre_id in movie.get('genre_ids', []):
                genre_name = self.genres.get(genre_id, "Unknown")
                genre_count[genre_name] = genre_count.get(genre_name, 0) + 1
        return sorted(genre_count.items(), key=lambda x: x[1], reverse=True)

    def group_titles_by_common_genres(self):
        genre_groups = {}
        for movie in self.data:
            for genre_id in movie.get('genre_ids', []):
                genre_name = self.genres.get(genre_id, "Unknown")
                if genre_name not in genre_groups:
                    genre_groups[genre_name] = frozenset()
                genre_groups[genre_name] = genre_groups[genre_name].union({movie['title']})
        return genre_groups

    def replace_first_genre_id(self):
        modified_data = []
        for movie in self.data:
            new_movie = movie.copy()
            if new_movie.get('genre_ids'):
                new_movie['genre_ids'][0] = 22
            modified_data.append(new_movie)
        return self.data, modified_data

    def prepare_custom_collection(self):
        def calculate_last_day_in_cinema(release_date):
            release_date = datetime.strptime(release_date, "%Y-%m-%d")
            return (release_date + timedelta(days=70)).strftime("%Y-%m-%d")

        custom_data = [
            {
                "Title": movie['title'],
                "Popularity": round(movie['popularity'], 1),
                "Score": int(movie['vote_average']),
                "Last_day_in_cinema": calculate_last_day_in_cinema(movie['release_date'])
            }
            for movie in self.data if 'release_date' in movie
        ]
        return sorted(custom_data, key=lambda x: (x['Score'], x['Popularity']), reverse=True)

    def write_to_csv(self, file_path):
        custom_data = self.prepare_custom_collection()
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Popularity", "Score", "Last_day_in_cinema"])
            writer.writeheader()
            writer.writerows(custom_data)


# Example usage:
tool = MovieDataPreparationTool(num_pages=3)

# Access methods
print(tool.get_all_data())
print(tool.get_filtered_data())
print(tool.get_most_popular_title())
print(tool.get_titles_with_keywords("action"))
print(tool.get_unique_genres())
tool.delete_movies_with_genre("Action")
print(tool.get_most_popular_genres())
print(tool.group_titles_by_common_genres())
original_data, modified_data = tool.replace_first_genre_id()
print(modified_data)
tool.write_to_csv("movies.csv")