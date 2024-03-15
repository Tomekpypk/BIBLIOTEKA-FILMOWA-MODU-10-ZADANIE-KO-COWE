import pytest
from unittest.mock import Mock, patch
import tmdb_client

def test_get_movies_list(monkeypatch):
    
    mock_response = {'results': [{'title': 'Movie 1'}, {'title': 'Movie 2'}]}
    requests_mock = Mock()
    requests_mock.return_value.json.return_value = mock_response
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    
    movies = tmdb_client.get_movies_list()

   
    assert movies == mock_response

def test_get_poster_url():
    
    poster_path = "/example_path.jpg"
    expected_url = f"https://image.tmdb.org/t/p/w780{poster_path}"

    
    url = tmdb_client.get_poster_url(poster_path)

    
    assert url == expected_url

def test_get_movie_by_id(monkeypatch):
    
    mock_movie_id = 123
    mock_movie_response = {'title': 'Mock Movie', 'id': mock_movie_id}
    requests_mock = Mock()
    requests_mock.return_value.json.return_value = mock_movie_response
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    
    movie = tmdb_client.get_movie_by_id(mock_movie_id)

    
    assert movie == mock_movie_response

def test_get_movie_cast(monkeypatch):
    
    mock_movie_id = 123
    mock_cast_response = {'cast': [{'name': 'Actor 1'}, {'name': 'Actor 2'}]}
    requests_mock = Mock()
    requests_mock.return_value.json.return_value = mock_cast_response
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    
    cast = tmdb_client.get_movie_cast(mock_movie_id)

    
    assert cast == mock_cast_response['cast']



if __name__ == "__main__":
    pytest.main()
