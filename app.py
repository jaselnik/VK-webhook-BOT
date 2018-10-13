from flask import Flask, request, json
from settings import *
import messageHandler

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello from Flask!"


@app.route(f"/{config['access_token']}", methods=["POST"])
def processing():
    data = json.loads(request.data)
    if "type" not in data.keys():
        return "not vk"
    if data["type"] == "confirmation":
        return config['confirmation_token']
    elif data["type"] == "message_new":
        messageHandler.create_answer(data["object"], config['token'])
        return "ok"
    print(config)
    return "nothing"


app.run(config['app']['host'], config['app']['port'])
