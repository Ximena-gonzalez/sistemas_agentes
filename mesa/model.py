import time
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from agent import Robot, Box



class RobotModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height, B, maximum_time):
        self.num_agents = N
        self.num_boxes = B
        self.boxCounter = 1
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 
        self.destination = (0,0)
        self.maximum_time = maximum_time
        self.start_time = time.time()
        self.elapsed_time = 0


        self.datacollector = DataCollector(
            {
                "Static": lambda m: self.count_type(m, "Static"),
                "Clean": lambda m: self.count_type(m, "Clean")
            }
        )

        # Randomly add cell agents

        for i in range(self.num_boxes):
            a = Box(i+1000,self) 
            self.schedule.add(a)
            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)
        
        for i in range(self.num_agents):
            a = Robot(i+2000, self) 
            self.schedule.add(a)
            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)

    def createBox(self):
        a = Box(self.boxCounter+3000, self)
        self.boxCounter += 1
        a.condition = "Goal"
        self.schedule.add(a)
        pos = self.destination
        self.grid.place_agent(a,pos)

    def step(self):
        '''Advance the model by one step.'''
        self.elapsed_time = time.time() - self.start_time
        self.schedule.step()
        self.datacollector.collect(self)
        hasBoxCount = 0
        boxCount = 0
        for agent in self.schedule.agents:
            if agent.condition == "HasBox":
                hasBoxCount += 1
            elif agent.condition == "Static":
                boxCount += 1

        
        if ((boxCount == 0 and hasBoxCount == 0) or self.maximum_time < self.elapsed_time):
            print("Amount of moves made by Robot[s]: " + str(self.moves_made(self)))
            self.running = False
            print("Time on run finish: " + str(round(self.elapsed_time, 2)) + " seconds.")

    @staticmethod
    def count_type(model, Box_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for Box in model.schedule.agents:
            if Box.condition == Box_condition:
                count += 1
        return count

    @staticmethod
    def clean_percentage(model):
        BoxCount = 0
        cleanCount = 0
        for Box in model.schedule.agents:
            if Box.condition == "Clean":
                cleanCount+=1
                BoxCount+=1
            elif Box.condition == "Static":
                BoxCount+=1
        return (cleanCount/BoxCount)*100

    @staticmethod
    def moves_made(model):
        totalMoves = 0
        for Agent in model.schedule.agents:
            if(isinstance(Agent, Robot)):
                totalMoves += Agent.moves
        return totalMoves

