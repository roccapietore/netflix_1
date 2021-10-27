import sqlite3

file = "netflix.db"


def get_data_base(sql):
    with sqlite3.connect(file) as con:
        cur = con.cursor()
        result = cur.execute(sql).fetchall()
        return result


def json_format(*categories, data_base):
    json_list = []
    for data in data_base:
        json_dict = {}
        for i, category in enumerate(categories):
            json_dict[category] = data[i]
        json_list.append(json_dict)
    return json_list


