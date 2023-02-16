from plates_viewer import app, db
from flask import request, abort, jsonify
from flask_httpauth import HTTPTokenAuth
from werkzeug.http import HTTP_STATUS_CODES
from .models import PlatesDatabase
from .utils import is_uuid, Plate, generate_plate


HTTP_STATUS_CODES[406] = 'Invalid data in the request'

auth = HTTPTokenAuth(scheme='Bearer')

tokens = {'token': 'token'}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.get('/plate/generate')
@auth.login_required
def generate():
    try:
        amount = int(request.args.get('amount')) if request.args.get('amount') else 1
    except ValueError:
        return abort(406)
    last_plate = PlatesDatabase.query.order_by(PlatesDatabase.pk.desc()).limit(1).first()
    generate_plate(last_plate.plate if last_plate else Plate.start_plate_value, amount)
    new_plates = PlatesDatabase.query.order_by(PlatesDatabase.pk.desc()).limit(amount).all()
    return [plate.plate for plate in new_plates][::-1]


@app.get('/plate/get')
@auth.login_required
def get_plates():
    plate_id = request.args.get('id')
    print(plate_id)
    if not (plate_id or is_uuid(plate_id)):
        return abort(406)
    plate_info = PlatesDatabase.query.filter_by(plate=plate_id).first_or_404()

    return jsonify({'id': plate_info.id, 'plate': plate_info.plate})


@app.post('/plate/add')
@auth.login_required
def post_plate():
    plate_to_add = request.form.get('plate')
    if Plate.check(plate_to_add):
        db.session.add(PlatesDatabase(plate_to_add))
        db.session.commit()
        return 'OK'
    return abort(406)
