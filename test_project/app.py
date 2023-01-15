from flask import Flask, request, abort
from flask_httpauth import HTTPTokenAuth
from werkzeug.http import HTTP_STATUS_CODES
from json import dumps
from methods import plates_autoincrement, PlatesViewer
from uuid import UUID
from re import match


HTTP_STATUS_CODES[406] = 'Invalid data in the request'

app = Flask('app')
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {'token': 'token'}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.get('/plate/generate')
@auth.login_required
def generate_plate():
    amount = request.args.get('amount')
    try:
        plates_autoincrement(int(amount) if amount else 1)
    except ValueError:
        return abort(406)


@app.get('/plate/get')
@auth.login_required
def get_plates():
    plate_id = request.args.get('id')
    if not plate_id:
        return abort(406)
    try:
        UUID(plate_id)
    except ValueError:
        return abort(406)
    plate_info = PlatesViewer.get_plates(['id', 'plate'],
                                         f"WHERE id = '{plate_id}'")

    plate_info_json = dumps({'id': plate_info[0][0], 'plate': plate_info[0][1]})
    response = app.response_class(response=plate_info_json,
                                  status=200,
                                  mimetype='application/json'
                                  )
    return response


@app.post('/plate/add')
@auth.login_required
def post_plate():
    plate = request.form.get('plate')

    if match(pattern=plate_pattern, string=plate):
        PlatesViewer.update_database(plate.lower())
        response = app.response_class(response='OK',
                                      status=200)
        return response
    return abort(406)


PLATE_LETTERS = ['а', 'в', 'с', 'е', 'н', 'к', 'м', 'о', 'р', 'т', 'х', 'у',
                 'a', 'b', 'c', 'e', 'h', 'k', 'm', 'o', 'p', 't', 'x', 'y']
REPLACEMENT_LETTERS = {k: v for k, v in zip(PLATE_LETTERS[:12], PLATE_LETTERS[12:])}


plate_pattern = fr'{PLATE_LETTERS}\d{{3}}{PLATE_LETTERS}{{2}}\d{{2,3}}'


app.run(host='localhost', port=8000)
