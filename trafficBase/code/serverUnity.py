from random import uniform
from flask import Flask, request, jsonify
from model import *
from agent import *
import logging, json, os

num_agents = 0
limit = 5
carModel = None
currentStep = 0


def sortByID(e):
    return e['id']

app = Flask("Test Server")

@app.route("/")
def default():
    print("Request recieved")
    return "Hello there!"

@app.route("/config", methods=['POST'])
def configure():
    global num_agents,carModel
    num_agents = int(request.form.get("numAgents"))
    print(f"Recieved num_agents = {num_agents}")
    carModel = CarModel(num_agents)
    print(carModel)
    return jsonify({"OK": num_agents})

@app.route("/update", methods=['GET'])
def updateModel():
    global currentStep
    if request.method == 'GET':
        carModel.step()
        currentStep += 1
        if carModel.running == False:
            return jsonify({'message':'Finished'})
        else:
            return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

@app.route("/getCars", methods=['GET'])
def update_points_cars():
    #print(list(robotModel.grid.coord_iter()))
    points = [{"x": x, "y":1, "z":z, "id":b.unique_id} for (a, x, z) in carModel.grid.coord_iter() for b in a if isinstance(b, Car)]
    #print(f"Points: {points}")
    points.sort(key=sortByID)
    sorted_points = [{"x": i["x"], "y":1, "z":i["z"]} for i in points]
    print(sorted_points)
    return jsonify({"positions": sorted_points})

@app.route("/getSemaforos", methods=['GET'])
def update_traffic_light():
    #print(list(robotModel.grid.coord_iter()))
    states = [{"x":x, "y":1, "z":z,"state":b.state, "id":b.unique_id} for (a, x, z) in carModel.grid.coord_iter() for b in a if isinstance(b, Traffic_Light)]
    #print(f"Points: {points}")
    states.sort(key=sortByID)
    sorted_points = [{"x": i["x"], "y":1, "z":i["z"]} for i in states]
    sorted_states = [i["state"] for i in states]
    print(sorted_states)
    return jsonify({"positions": sorted_points, "states": sorted_states})

port = int(os.getenv('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=True)