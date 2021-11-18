from random import uniform
from flask import Flask, request, jsonify

num_agents = 0
limit = 5

app = Flask("Test Server")

def random_point():
    return {"x": uniform(-limit, limit),
            "y": uniform(-limit, limit),
            "z": uniform(-limit, limit)}

@app.route("/")
def default():
    print("Request recieved")
    return "Hello there!"

@app.route("/config", methods=['POST'])
def configure():
    global num_agents
    num_agents = int(request.form.get("numAgents"))
    print(f"Recieved num_agents = {num_agents}")
    return jsonify({"OK": num_agents})

@app.route("/update", methods=['GET'])
def update_points():
    points = [random_point() for _ in range(num_agents)]
    print(f"Points: {points}")
    return jsonify({"positions": points})

app.run()