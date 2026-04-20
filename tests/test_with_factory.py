from factories import ClientFactory, ParkingFactory
from module_2.hw_29.parking.main.models import Clients, Parking



def test_create_client(app, db):
    client = ClientFactory()
    db.session.commit()
    assert client.name is not None
    assert len(db.session.query(Clients).all()) == 1



def test_create_parking(client, db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.address is not None
    assert parking.count_places is not None
    assert len(db.session.query(Parking).all()) == 1
