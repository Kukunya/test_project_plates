from plates_viewer import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class PlatesDatabase(db.Model):
    __tablename__ = 'plates'
    pk = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(UUID(as_uuid=True))
    plate = db.Column(db.Text(10))

    def __init__(self, plate):
        self.plate = plate
        self.id = uuid.uuid4()


def add(self, plate_to_add):
    db.session.add(PlatesDatabase(plate_to_add))
    db.session.commit()


def get(self, uuid):
    return PlatesDatabase.query.filter_by(plate=uuid).first()