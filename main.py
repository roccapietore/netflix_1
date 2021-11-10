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
    sql_start = "select title, description from netflix where "
    sql_lst = []
    sql = ''
    if type_ := request.args.get('type'):
        sql_lst.append(f" type = '{type_}'")
    if year := request.args.get('year'):
        sql_lst.append(f" release_year = '{year}'")
    if genre := request.args.get('genre'):
        sql_lst.append(f" listed_in like '%{genre}%'")
    if sql_lst:
        sql = sql_start + ' and '.join(sql_lst)
        result = get_data_base(sql)
        return jsonify(json_format('title', 'description', data_base=result))


@app.route("/cast/<actor_1>/<actor_2>")
def get_actors(actor_1: str, actor_2: str):
    actor_list = []
    new_list = []
    sql = f"SELECT `cast` FROM netflix WHERE `cast` LIKE '%{actor_1}%{actor_2}%' or `cast` like '%{actor_2}%{actor_1}%'"
    result = get_data_base(sql)
    for cast in result:
        for actor in cast:
            actor = actor.split(', ')
            actor_list += actor
            if actor_1 in actor_list and actor_2 in actor_list:
                actor_list.remove(actor_1)
                actor_list.remove(actor_2)

    for actor in actor_list:
        if actor_list.count(actor) > 2:
            new_list.append(actor)
            new_list = list(set(new_list))
    return jsonify(new_list)


if __name__ == '__main__':
    app.run(port=5003)
