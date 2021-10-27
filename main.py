from flask import Flask, jsonify, request
from functions import get_data_base, json_format

app = Flask(__name__)


@app.route("/movie")
def get_movie_by_title():
    title = request.args.get('title')
    if title:
        sql = f"SELECT title, country, release_year, description FROM netflix WHERE lower(title) LIKE '%{title.lower()}%'" \
              f"ORDER BY release_year DESC LIMIT 1"

        result = get_data_base(sql)
        return jsonify(json_format('title', 'country', 'release_year', 'description', data_base=result))


@app.route("/movie/year/<year_1>/<year_2>")
def get_movies_by_years(year_1: int, year_2: int):
    sql = f"SELECT title, release_year FROM netflix WHERE release_year BETWEEN {year_1} AND {year_2}" \
          f" LIMIT 100"
    result = get_data_base(sql)
    return jsonify(json_format('title', 'release_year', data_base=result))


@app.route("/rating/children")
def children_movies():
    sql = f"SELECT title, rating, description FROM netflix WHERE rating = 'G' LIMIT 100"
    result = get_data_base(sql)
    return jsonify(json_format('title', 'rating', 'description', data_base=result))


@app.route("/rating/family")
def family_movies():
    sql = f"SELECT title, rating, description FROM netflix WHERE rating = 'PG' OR rating = ' PG-13' LIMIT 100"
    result = get_data_base(sql)
    return jsonify(json_format('title', 'rating', 'description', data_base=result))


@app.route("/rating/adult")
def adult_movies():
    sql = f"SELECT title, rating, description FROM netflix WHERE rating = 'R' OR rating = 'NC-17' LIMIT 100"
    result = get_data_base(sql)
    return jsonify(json_format('title', 'rating', 'description', data_base=result))


@app.route("/genre")
def get_movies_by_genre():
    genre = request.args.get('genre')
    if genre:
        sql = f"SELECT title, description FROM netflix WHERE lower(listed_in) LIKE '%{genre.lower()}%' ORDER BY release_year DESC LIMIT 10"
        result = get_data_base(sql)
        return jsonify(json_format('title', 'description', data_base=result))


@app.route("/search")
def search_by_parameters():
    sql = f"SELECT title, description FROM netflix WHERE type =  '', release_year = '', listed_in = '' LIMIT 10"
    result = get_data_base(sql)
    return jsonify(json_format('title', 'description', data_base=result))


if __name__ == '__main__':
    app.run()
