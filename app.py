from flask import Flask, request
from flask_restplus import Api, Resource
import matplotlib.pyplot as plt

import os
import json
import numpy as np
import random

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='FB Hackathon',
          description="Let's get ready to rumble!")

ROOT_PATH = "/Users/elfsong/PycharmProjects/FB"
RESOURCE_PATH = os.path.join(ROOT_PATH, "resource")
twitter_data = os.path.join(RESOURCE_PATH, "twitterdata.json")
p_l_data = os.path.join(RESOURCE_PATH, "p_l.json")


def create_grid(tb_boundary, lr_boundary):
    point_matrix = list()
    node_id = 0

    for x in np.arange(lr_boundary[0], lr_boundary[1], 0.0008):
        co_line = list()
        for y in np.arange(tb_boundary[0], tb_boundary[1], 0.0008):
            point_coordinate = (x, y, 2 + random.random() * 3)
            co_line += [point_coordinate]
            node_id += 1
        point_matrix += [co_line]
    point_matrix = np.array(point_matrix)
    return point_matrix


def get_index_by_coordinate(point_matrix, x, y):
    for i, line in enumerate(point_matrix):
        if line[0][0] >= y:
            y_index = i
            for j, item in enumerate(line):
                if item[1] >= x:
                    x_index = j
                    return y_index, x_index
    raise ValueError

def show_matrix_2(matrix, tb_boundary, lr_boundary):
    point_x = list()
    point_y = list()
    point_c = list()
    print(matrix)

    for index_x, line in enumerate(matrix):
        for index_y, value in enumerate(line):
            point_x += [index_x]
            point_y += [index_y]
            point_c += [value]
            print(value)

    plt.scatter(point_x, point_y, c=point_c, s=20, cmap='Greys')
    # plt.axis([lr_boundary[0], lr_boundary[1], tb_boundary[0], tb_boundary[1]])
    plt.show()

@api.route('/')
class FindPath(Resource):
    @api.response(200, "Success to get the matrix.")
    @api.response(404, "The input parameters may be incorrect!")
    @api.doc(params={'mode': 'The layer of matrixs'})
    def post(self):
        return "Test", 200


if __name__ == "__main__":
    tb_boundary = [-37.820984280171785, -37.803273851858656]
    lr_boundary = [144.90155334472656, 144.98303232321211]

    print("Generating Map Matrix...")
    point_matrix = create_grid(tb_boundary, lr_boundary)
    print("Map Matrix Finished!")

    light_score_matrix = np.zeros(shape=(len(point_matrix), len(point_matrix[0])))
    peds_score_matrix = np.zeros(shape=(len(point_matrix), len(point_matrix[0])))
    tweets_score_matrix = np.zeros(shape=(len(point_matrix), len(point_matrix[0])))



    with open(p_l_data, encoding="utf-8") as fd:
        info = json.loads(fd.readline())
    len_info = len(info)

    count = 0
    for item in info:
        co_x = item[0][0]
        co_y = item[0][1]
        value = item[1]
        type = item[2]
        count += 1
        print("Process: ", "%.2f" % (count / len_info * 100), "%")
        if type in ["lights1", "lights2", "lights3"]:
            try:
                x, y = get_index_by_coordinate(point_matrix, float(co_x), float(co_y))
                light_score_matrix[x][y] += float(value)
            except ValueError:
                pass
        elif type in ["pedestrians"]:
            try:
                x, y = get_index_by_coordinate(point_matrix, float(co_x), float(co_y))
                peds_score_matrix[x][y] += float(value)
            except ValueError:
                pass



    for index_x in range(len(point_matrix)):
        for index_y in range(len(point_matrix[0])):
            tcx, tcy, ts = point_matrix[index_x][index_y]
            ls = light_score_matrix[index_x][index_y]
            ps = peds_score_matrix[index_x][index_y]
            sc = ps + ls
            if sc >= 50:
                sc = 50
            point_matrix[index_x][index_y] = tcx, tcy, sc + ts


    show_matrix_2(peds_score_matrix, tb_boundary, lr_boundary)

    app.run(host='0.0.0.0', port=5000)
