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
            print(selection)
            lightController.requests.append(selection)
            # print(lightController.requests)
        return lightController.status


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':

    LED_PIN = 18
    LED_BRIGHTNESS = 255


    lightController = Controller(LED_PIN, LED_BRIGHTNESS)
    lightController.switchTo(0)

    x = threading.Thread(target=lightController.run)
    x.start()
    try:
        app.run(host='0.0.0.0', port=5050)
    except:
        pass

