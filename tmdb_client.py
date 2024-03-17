import requests

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3OTI1MTgwYzQxZjVlZTMzMWNlMThmOGZkOWU4Mzk3MyIsInN1YiI6IjY1Y2I5MmM0ZjkyNTMyMDE2M2MwMzU5YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FHt9fRxVMgWaDpFIAmbUrrcpNwk19gc5nZuO92yQ7dw"

def get_movies_list(list_type='popular'):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

def get_poster_url(poster_api_path, size="w780"):
    base_url = "https://image.tmdb.org/t/p/"
    if poster_api_path.startswith("/"):
        poster_api_path = poster_api_path[1:]
    return f"{base_url}{size}/{poster_api_path}"


def get_movie_by_id(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    movie = response.json()
    cast = get_movie_cast(movie_id)
    movie["cast"] = cast
    return movie

def get_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    cast = response.json()["cast"][:5]  # Ogranicz do pierwszych 5 aktorów
    return cast

def get_movies(how_many=8, list_type='popular'):
    movie_list = get_movies_list(list_type)
    movies = []
    for movie in movie_list["results"][:how_many]:
        poster_url = get_poster_url(movie["poster_path"], "w780")
        backdrop_path = movie["backdrop_path"]
        movie_data = {
            "id": movie["id"],
            "title": movie["title"],
            "description": movie.get("overview", "Brak opisu."),
            "link": f"/movie/{movie['id']}",
            "image": poster_url,
            "backdrop_path": backdrop_path,
        }
        movies.append(movie_data)
    return movies

def get_movie_by_id(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    movie = response.json()
    if "cast" not in movie:
        movie["cast"] = []
    else:
        cast = get_movie_cast(movie_id)
        movie["cast"] = cast
    return movie


def get_available_lists():
    endpoint = "https://api.themoviedb.org/3/discover/movie"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    params = {
        "api_key": API_TOKEN,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": "false",
        "include_video": "false",
        "page": 1
    }

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    lists = response.json().get("results", [])

    # Extract unique list names from the results
    unique_lists = {list_info['original_title']: list_info for list_info in lists}.values()

    return list(unique_lists)


def search(search_query):
   base_url = "https://api.themoviedb.org/3/"
   api_token = API_TOKEN
   headers = {
       "Authorization": f"Bearer {api_token}"
   }
   endpoint = f"{base_url}search/movie?query={search_query}"

   response = requests.get(endpoint, headers=headers)
   response = response.json()
   return response['results']

def get_airing_today():
    endpoint = f"https://api.themoviedb.org/3/tv/airing_today"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    response = response.json()
    return response['results']
