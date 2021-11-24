from mesa import Agent
import random

boxCounter = 1
test_list = [0,1,2,3]

class Box(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = "Static"

    

class Robot(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.condition = "NoBox"
        self.moves = 0
        self.box = None

    def boxNeighbor(self):
        possible_steps = self.model.grid.get_neighbors(
            self.pos,
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False)
        for agent in possible_steps:
            if(isinstance(agent, Box)):
                if(agent.condition != "Goal"):
                    return agent.pos
            else:
                return False

    def canGrab(self):
        possible_steps = self.model.grid.get_neighbors(
            self.pos,
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False)
        for agent in possible_steps:
            if(isinstance(agent, Box)):
                if(agent.condition != "Goal"):
                    return True
        return False


    def robotN(self):
        posList = []
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False)
        for neighbor in possible_steps:
            if(isinstance(neighbor, Robot)):
                posList.append(neighbor.pos)
            else:
                return False

    def noObst(self):
        freeSpaces = []
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False)
        for tile in possible_steps:
            if(len(self.model.grid[tile]) <= 0):
                print(tile)
                freeSpaces.append(tuple(tile))
        if(len(freeSpaces) == 4):
            return True
        return False
            

    def randomMove(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False) 
        

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        if len(possible_steps) <= self.direction:
            pass
        else:
            self.model.grid.move_agent(self, possible_steps[self.direction])
            

    def randomMoveObst(self):
        freeSpaces = []
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False) 

        for tile in possible_steps:
            if(len(self.model.grid[tile]) <= 0):
                freeSpaces.append(tuple(tile))

        space = random.choice(freeSpaces)
        self.model.grid.move_agent(self, space)
        if(self.box != None and self.box.condition != "Goal"):
            self.model.grid.move_agent(self.box, space)
        

        
    def destMove(self, xOY, dist):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        newPos = [self.pos[0],self.pos[1]]
        if(xOY == "x"):
            if(dist > 0):
                newPos[0] += 1
            else:
                newPos[0] -= 1
        else:
            if(dist > 0):
                newPos[1] += 1
            else:
                newPos[1] -= 1

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        if len(possible_steps) <= self.direction:
            pass
        else:
            self.model.grid.move_agent(self, tuple(newPos))
            if(self.box.condition != "Goal"):
                self.model.grid.move_agent(self.box, tuple(newPos))

    def grab(self):
        self.condition = "HasBox"
        self.box = self.model.grid[self.boxNeighbor()][0]
        self.model.grid.move_agent(self.box, self.pos)
        self.box.condition = "Dynamic"

    def dropBox(self):
        self.condition = "NoBox"
        self.box.condition = "Goal"
        self.model.grid.move_agent(self.box, self.model.destination)
     

    def step(self):
        list = self.model.grid[self.pos]
        #calcula cual cosa hacer basado en la jerarquia
        distX = self.model.destination[0] - self.pos[0]
        distY = self.model.destination[1] - self.pos[1]
        self.direction = self.random.randrange(0,4)
        if(self.condition == "HasBox" and (self.pos == (0,1) or self.pos == (1,0))):
            print("Tengo caja y la voy a dejar en dest")
            self.dropBox()
        elif(self.condition == "HasBox" and self.noObst()): #Si tienes caja y no hay obstaculos
            print("Tengo caja y no hay obstaculo")
            if(abs(distX) > abs(distY)):
                self.destMove("x",distX)
            else:
                self.destMove("y",distY)
        elif(self.condition != "HasBox" and self.boxNeighbor() and self.canGrab()): #Si no tienes caja y hay caja cerca de ti
            print("No tengo caja y si puedo agarrar una")
            self.grab()
        elif(self.condition != "HasBox" and (not self.noObst())): #Si no tienes caja y si hay obstaculos en tu camino
            print("No tengo caja y si hay obstaculo")
            self.randomMoveObst()
        elif(not self.noObst()): #Si tienes caja y si hay obstaculos en tu camino
            self.randomMoveObst()
            print("Tengo caja y si hay obstaculo")
        else:  #Si algo llega a pasar de la jerarquia
            print("Reached else")
            self.randomMove()
        self.moves += 1



