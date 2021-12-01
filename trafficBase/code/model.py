from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from agent import *
import random
import json

class CarModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N):

        dataDictionary = json.load(open("mapDictionary.txt"))

        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            self.destinations = []
            self.roads = []

            self.grid = MultiGrid(self.width, self.height,torus = False) 
            self.schedule = SimultaneousActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "t", "p", "r", "l"]:
                        agent = Road(f"r{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.roads.append(agent.pos)
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinations.append(agent.pos)

        self.num_agents = N
        self.running = True 
        

        
        for i in range(self.num_agents):
            carDestination = random.choice(self.destinations)
            a = Car(i+1000,self) 
            a.destination = carDestination
            self.schedule.add(a)
            pos = random.choice(self.roads)
            hasCar = False
            for gridAgent in self.grid[pos]:
                if(isinstance(gridAgent, Car)):
                    hasCar = True
            while (hasCar):
                pos = random.choice(self.roads)
                for gridAgent in self.grid[pos]:
                    if(not (isinstance(gridAgent, Car))):
                        hasCar = False
            self.grid.place_agent(a, pos)
    



    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        if self.schedule.steps % 10 == 0:
            for agents, x, y in self.grid.coord_iter():
                for agent in agents:
                    if isinstance(agent, Traffic_Light):
                        agent.state = not agent.state
        counter = 0
        for agent in self.schedule.agents:
            if(isinstance(agent,Car)):
                if agent.condition != "Goal":
                    counter += 1
        if(counter == 0):
            self.running = False