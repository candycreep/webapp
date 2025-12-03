import pika
import json
from functools import wraps

class EventDecorator:
    def __init__(self, rabbitmq_host='localhost', exchange='cars_events_exchange'):
        self.rabbitmq_host = rabbitmq_host
        self.exchange = exchange

    def send_event(self, event_type, car_data):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type='fanout')

        message = json.dumps({
            "eventType": event_type,
            "car": car_data
        })

        channel.basic_publish(exchange=self.exchange, routing_key='', body=message)
        connection.close()

    def decorate_create(self, func):
        @wraps(func)
        def wrapper(db, car):
            result = func(db, car)
            if result:
                car_data = {
                    "firm": result.firm,
                    "model": result.model,
                    "year": result.year,
                    "power": result.power,
                    "color": result.color,
                    "price": result.price
                }
                self.send_event("CREATE", car_data)
            return result
        return wrapper

    def decorate_update(self, func):
        @wraps(func)
        def wrapper(db, car_id, car):
            result = func(db, car_id, car)
            if result:
                car_data = {
                    "firm": result.firm,
                    "model": result.model,
                    "year": result.year,
                    "power": result.power,
                    "color": result.color,
                    "price": result.price
                }
                self.send_event("UPDATE", car_data)
            return result
        return wrapper

    def decorate_delete(self, func):
        @wraps(func)
        def wrapper(db, car_id):
            from crud import get_car
            car = get_car(db, car_id)
            if car:
                car_data = {
                    "firm": car.firm,
                    "model": car.model,
                    "year": car.year,
                    "power": car.power,
                    "color": car.color,
                    "price": car.price
                }
                self.send_event("DELETE", car_data)
            result = func(db, car_id)
            return result
        return wrapper