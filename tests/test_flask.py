import pytest
from datetime import datetime


@pytest.mark.parametrize("route", ["/test", "/clients/1", "/clients"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


def test_client_id(client) -> None:
    resp = client.get("/clients/1")
    assert resp.json == {"id": 1, "name": "In", "surname": "Smirnova",
                         "credit_card": 12345, "car_number": "a123aa78"}


def test_create_client(client) -> None:
    client_data = {"name": "Джеки", "surname": "Чан",
                 "credit_card": 23456, "car_number": "a321sd98"}
    resp = client.post("/client", data=client_data)

    assert resp.status_code == 201


@pytest.mark.parking
def test_create_client_parking(client) -> None:
    client_data = {"client_id": 1, "parking_id": 1,
                 "time_on": datetime.now()}
    resp = client.post("/client_parking", data=client_data)

    assert resp.status_code == 201


@pytest.mark.parking
def test_delete_client_parking(client) -> None:
    client_data = {"client_id": 1, "parking_id": 1}

    parking = client.get("/parking/1").json
    count_places = parking['count_available_places']

    resp = client.post("/delete_client_parking", data=client_data)

    up_parking = client.get("/parking/1").json
    up_count_places = up_parking['count_available_places']

    assert resp.status_code == 200
    assert (count_places + 1) == up_count_places



def test_len_clients(client) -> None:
    resp = client.get("/clients")
    assert len(resp.json) == 2

