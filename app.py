from flask import Flask, request
from flask_restplus import Api, Resource

import json
import numpy as np
import random

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='FB Hackathon',
          description="Let's get ready to rumble!")


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

    app.run(host='0.0.0.0', port=5000)
