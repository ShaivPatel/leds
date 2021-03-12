from flask import Flask, request
from flask_restful import Resource, Api
from controller import Controller
import threading

app = Flask(__name__)
api = Api(app)

lightController = None

class HelloWorld(Resource):
    def get(self):
        selection = request.args.get('selection')
        if selection:
            lightController.requests.append(selection)
        return lightController.status


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':

    LED_PIN = 18
    LED_BRIGHTNESS = 255


    lightController = Controller(LED_PIN, LED_BRIGHTNESS)

    x = threading.Thread(target=app.run, kwargs={'debug':True})
    x.start()
    lightController.run()

