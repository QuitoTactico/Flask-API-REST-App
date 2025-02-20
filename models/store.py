from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # it won't query all the items each time you use the Store, they will be queried only when you need the items
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )
    # también podrías poner delete-orphan, si quieres que se borren los items que sean quitados de la lista y queden sin store.
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
