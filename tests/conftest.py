import pytest
#from datetime import datetime


from main.app import create_app, db as _db
from main.models import Clients, Parking, ClientParking



@pytest.fixture(scope="module")
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        new_client = Clients(id=1,
                    name="Inna",
                    surname="Smirnova",
                    credit_card=12345,
                          car_number='a123aa78')
        parking = Parking(address="city, street",
                          opened=1,
                          count_places=5,
                          count_available_places=5)
        _db.session.add(new_client)
        _db.session.add(parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture(scope="module")
def db(app):
    with app.app_context():
        yield _db
