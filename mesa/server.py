from model import RobotModel, Box, Robot
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer

BoxColors = {"Static": "brown", "Clean": "blue"}
Time = {"Time": "black"}

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}
    if (isinstance,(agent, Robot)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.4
    if (isinstance(agent, Box) and agent.condition == "Static"):
        portrayal["Color"] = "brown"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2
    elif (isinstance(agent, Box) and agent.condition == "Clean"):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2


    return portrayal

model_params = {"N":1, "width":10, "height":10, "B":2}
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(RobotModel, [grid], "Robot Sim", model_params)
                       
server.port = 8521 # The default
server.launch()


