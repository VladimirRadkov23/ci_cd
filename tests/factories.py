# import factory
# #import factory.fuzzy as fuzzy
# import random
# #from datetime import datetime
#
# from module_2.hw_29.parking.main.models import Clients, Parking
# from module_2.hw_29.parking.main.app import db
#
#
#
# class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = Clients
#         sqlalchemy_session = db.session
#
#     name = factory.Faker('first_name')
#     surname = factory.Faker('last_name')
#     credit_card = factory.Faker("boolean")
#     car_number = factory.Faker('license_plate', locale='ru_RU')
#
#
#
# class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = Parking
#         sqlalchemy_session = db.session
#
#     address = factory.Faker("address")
#     opened = factory.Faker("boolean")
#     count_places = factory.Faker('random_int', min=20, max=50)
#     count_available_places = factory.LazyAttribute(lambda x: random.randrange(1, 20))
