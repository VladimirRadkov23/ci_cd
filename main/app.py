from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List
from datetime import datetime


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///parking.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # конфиг чтобы не писались варнинги
    db.init_app(app)

    from .models import Clients, Parking, ClientParking

    with app.app_context():
        db.create_all()
        print("oki Ok")


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()


    @app.route("/test")
    def route_test():
        return 'Test'


    @app.route("/clients", methods=['GET'])
    def get_clients():
        """Получение списка клиентов"""

        clients: List[Clients] = db.session.query(Clients).all()
        clients_list = [u.to_json() for u in clients]
        return jsonify(clients_list), 200


    @app.route("/clients/<int:client_id>", methods=['GET'])
    def get_client_id(client_id: int):
        """Получение информации о клиенте по id"""

        client: Clients = db.session.query(Clients).get(client_id)
        return jsonify(client.to_json()), 200


    @app.route("/parking/<int:parking_id>", methods=['GET'])
    def get_parking_id(parking_id: int):
        """Получение информации о паркинге по id"""

        parking: Parking = db.session.query(Parking).get(parking_id)
        return parking.to_json(), 200


    @app.route("/parking", methods=['POST'])
    def create_parking():
        """Создание нового паркинга"""

        address = request.form.get('address', type=str)
        opened = request.form.get('opened', type=bool)
        count_places = request.form.get('count_places', type=int)
        count_available_places = request.form.get('count_available_places', type=int)

        new_product = Parking(address=address,
                              opened=opened,
                              count_places=count_places,
                              count_available_places=count_available_places)

        db.session.add(new_product)
        db.session.commit()
        return 'Парковка создана', 201


    @app.route("/client", methods=['POST'])
    def create_client():
        """Создание нового клиента"""

        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        credit_card = request.form.get('credit_card', type=int)
        car_number = request.form.get('car_number', type=str)

        new_client = Clients(name=name,
                        surname=surname,
                        credit_card=credit_card,
                        car_number=car_number)
        db.session.add(new_client)
        db.session.commit()
        return 'Клиент создан', 201


    @app.post('/client_parking')
    def create_client_parking():
        """ Заезд на парковку """

        parking_id = request.form.get('parking_id', type=str)
        parking = db.session.get(Parking, parking_id)
        if parking.opened:    # Проверяем открыта ли парковка
            client_id = request.form.get('client_id', type=str)
            client = db.session.get(Clients, client_id)
            if client.credit_card:   # Проверка наличия кредитной карты
                client_parking = db.session.query(ClientParking).filter(ClientParking.client_id == client_id,
                                                                        ClientParking.parking_id == parking_id).one_or_none()
                if client_parking:
                    print('ok delete 1')

                    if client_parking.time_out: # проверка, есть ли закрытый парковочный талон. Если да - удаляем
                        db.session.delete(client_parking)
                        db.session.commit()
                        print('ok delete 2')
                new_client_parking = ClientParking(client_id=client_id,
                                  parking_id=parking_id,
                                  time_on=datetime.now())
                db.session.add(new_client_parking)
                parking.count_available_places -= 1
                if parking.count_available_places <= 0: # закрываем парковку, если мест не осталось
                    parking.opened = False
                db.session.commit()
                return parking.to_json(), 201
            else:
                return " У вас нет кредитной карты для оплаты"
        else:
            return 'Нет свободных мест'


    @app.route('/delete_client_parking', methods=['POST'])
    def delete_client_parking():
        """ Закрытие парковочного талона """

        client_id = request.form.get('client_id', type=str)
        parking_id = request.form.get('parking_id', type=str)
        parking = db.session.get(Parking, parking_id)
        client_parking = db.session.query(ClientParking).filter(ClientParking.client_id == client_id, ClientParking.parking_id == parking_id).one_or_none()

        if client_parking:
            parking.count_available_places += 1
            client_parking.time_out = datetime.now()

            if not parking.opened:
                parking.opened = True
            db.session.commit()
            return client_parking.to_json(), 200
        else:
            return 'Такого клиента нет'

    return app
