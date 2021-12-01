from random import uniform
from flask import Flask, request, jsonify
from model import *
from agent import *

num_agents = 0
limit = 5
robotModel = None
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
    global num_agents,width,height,num_boxes,maximum_time,robotModel
    num_agents = int(request.form.get("numAgents"))
    print(f"Recieved num_agents = {num_agents}")
    width = int(request.form.get("gridWidth"))
    print(f"Recieved width = {width}")
    height = int(request.form.get("gridHeight"))
    print(f"Recieved height = {height}")
    num_boxes = int(request.form.get("numBoxes"))
    print(f"Recieved num_boxes = {num_boxes}")
    maximum_time = int(request.form.get("maximumTime"))
    print(f"Recieved maximum_time = {maximum_time}")
    robotModel = RobotModel(num_agents,width,height,num_boxes,maximum_time)
    return jsonify({"OK": num_agents})

@app.route("/update", methods=['GET'])
def updateModel():
    global currentStep, robotModel
    if request.method == 'GET':
        robotModel.step()
        currentStep += 1
        if robotModel.running == False:
            return jsonify({'message':'Finished'})
        else:
            return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

@app.route("/getRobots", methods=['GET'])
def update_points_robots():
    #print(list(robotModel.grid.coord_iter()))
    points = [{"x": x, "y":1, "z":z, "id":b.unique_id} for (a, x, z) in robotModel.grid.coord_iter() for b in a if isinstance(b, Robot)]
    #print(f"Points: {points}")
    points.sort(key=sortByID)
    sorted_points = [{"x": i["x"], "y":1, "z":i["z"]} for i in points]
    print(sorted_points)
    return jsonify({"positions": sorted_points})

@app.route("/getBoxes", methods=['GET'])
def update_points_boxes():
    #print(list(robotModel.grid.coord_iter()))
    points = [{"x": x, "y":1, "z":z} for (a, x, z) in robotModel.grid.coord_iter() for b in a if isinstance(b, Box)]
    #print(f"Points: {points}")
    return jsonify({"positions": points})

app.run()