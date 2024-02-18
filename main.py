from flask import Flask, render_template, request, url_for, abort
import tmdb_client

app = Flask(__name__)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route('/')
def homepage():
    selected_list = request.args.get('list_type', 'popular')
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list)

@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    movie = tmdb_client.get_movie_by_id(movie_id)
    if not movie:
        abort(404)  # Wygeneruj błąd 404, jeśli film nie istnieje

    return render_template("movie_details.html", movie=movie)


if __name__ == '__main__':
    app.run(debug=True)
