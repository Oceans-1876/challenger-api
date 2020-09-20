from api.db import db


class Stations(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def serialize(self):
        return {"id": self.id}
