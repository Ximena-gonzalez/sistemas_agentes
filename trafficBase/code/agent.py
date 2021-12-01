from mesa import Agent

class Car(Agent):
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
        self.condition = "NoGoal"
        self.destination = ()
        self.inter = False
        self.moves = 0
        self.distX = 0
        self.distY = 0
        self.waited = 0
        self.interPassed = []
    '''
    def currentCarril(self):
        newPos = [self.pos[0],self.pos[1]]
        list = self.model.grid[self.pos]
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False)
        if(len(possible_steps) == 3):
            return 0
        for agent in list:
            if(isinstance(agent,Road)):
                if(agent.direction == "Down" or agent.direction == "Up"):
                    
                elif(agent.direction == "Right" or agent.direction == "Left"):
                    newPos[0] += 1
    '''
    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        
        # Checks which grid cells are empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
       
        next_move = self.random.choice(next_moves)
        # Now move:
        if self.random.random() < 0.1:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken+=1

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        # if freeSpaces[self.direction]:
        #     self.model.grid.move_agent(self, possible_steps[self.direction])
        #     print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        # else:
        #     print(f"No se puede mover de {self.pos} en esa direccion.")

    def whichLight(self):
        newPos = [self.pos[0],self.pos[1]]
        list = self.model.grid[self.pos]
        for agent in list:
            if(isinstance(agent,Road)):
                if(agent.direction == "Down"):
                    newPos[1] -= 1
                elif(agent.direction == "Up"):
                    newPos[1] += 1
                elif(agent.direction == "Right"):
                    newPos[0] += 1
                elif(agent.direction == "Left"):
                    newPos[0] -= 1
        newList = self.model.grid[tuple(newPos)]
        for agent in newList:
            if(isinstance(agent,Traffic_Light)):
                if(agent.state == False):
                    return "Red"
                elif(agent.state == True):
                    return "Green"
        return "None"

    def interCheck(self):
        newPos = [self.pos[0],self.pos[1]]
        list = self.model.grid[self.pos]
        direction = "Down"
        for agent in list:
            if(isinstance(agent,Road)):
                if(agent.direction == "Down" or direction == "RightDown" or direction == "LeftDown"):
                    direction = "Down"
                elif(agent.direction == "Up" or direction == "RightUp" or direction == "LeftUp"):
                    direction = "Up"
                elif(agent.direction == "Right" or direction == "RightDown" or direction == "RightUp"):
                    direction = "Right"
                elif(agent.direction == "Left" or direction == "LeftUp" or direction == "LeftDown"):
                    direction = "Left"
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False)
        for cell in possible_steps:
            for agent in self.model.grid[cell]:
                if(isinstance(agent, Car)):
                    if(direction == "Down"):
                        if(agent.pos[1] < self.pos[1] and agent.inter):
                            return True
                    if(direction == "Up"):
                        if(agent.pos[1] > self.pos[1] and agent.inter):
                            return True    
                    if(direction == "Left"):
                        if(agent.pos[0] < self.pos[0] and agent.inter):
                            return True  
                    if(direction == "Right"):
                        if(agent.pos[0] > self.pos[0] and agent.inter):
                            return True  
        return False

    def carCheck(self):
        newPos = [self.pos[0],self.pos[1]]
        list = self.model.grid[self.pos]
        direction = "Down"
        for agent in list:
            if(isinstance(agent,Road)):
                direction = agent.direction
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False)
        for cell in possible_steps:
            for agent in self.model.grid[cell]:
                if(isinstance(agent, Car) and agent.condition != "Goal"):
                    if(self.distY > self.distX and self.distY < 0 and direction == "Down"):
                        if(agent.pos[1] < self.pos[1]):
                            return True
                    if(self.distY > self.distX and self.distY > 0 and direction == "Up"):
                        if(agent.pos[1] > self.pos[1]):
                            return True    
                    if(self.distY < self.distX and self.distY < 0 and direction == "Left"):
                        if(agent.pos[0] < self.pos[0]):
                            return True  
                    if(self.distY < self.distX and self.distY > 0 and direction == "Right"):
                        if(agent.pos[0] > self.pos[0]):
                            return True 

        return False

    def destRange(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False)
        for cell in possible_steps:
            if(cell == self.destination):
                return True
        return False

    def straightMove(self):
        newPos = [self.pos[0],self.pos[1]]
        list = self.model.grid[self.pos] 
        direction = ""
        for agent in list:
            if(isinstance(agent,Road)):
                if(agent.direction == "Down"):
                    direction = "Down"
                elif(agent.direction == "Up"):
                    direction = "Up"
                elif(agent.direction == "Right"):
                    direction = "Right"
                elif(agent.direction == "Left"):
                    direction = "Left"
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False)
        for cell in possible_steps:
            for agent in self.model.grid[cell]:
                if(isinstance(agent, Road)):
                    if(direction == "Down"):
                        if(agent.pos[1] < self.pos[1] and (agent.direction == "RightDown" or agent.direction == "LeftDown")):
                            self.model.grid.move_agent(self, agent.pos)
                        elif(agent.pos[1] < self.pos[1]):
                            self.model.grid.move_agent(self, agent.pos)
                    elif(direction == "Up"):
                        if(agent.pos[1] > self.pos[1] and (agent.direction == "RightUp" or agent.direction == "LeftUp")):
                            self.model.grid.move_agent(self, agent.pos)
                        elif(agent.pos[1] > self.pos[1]):
                            self.model.grid.move_agent(self, agent.pos)
                    elif(direction == "Right"):
                        if(agent.pos[0] > self.pos[0] and (agent.direction == "RightDown" or agent.direction == "RightUp")):
                            self.model.grid.move_agent(self, agent.pos)
                        elif(agent.pos[0] > self.pos[0]):
                            self.model.grid.move_agent(self, agent.pos)
                    elif(direction == "Left"):
                        if(agent.pos[0] < self.pos[0] and (agent.direction == "LeftDown" or agent.direction == "LeftUp")):
                            self.model.grid.move_agent(self, agent.pos)
                        elif(agent.pos[0] < self.pos[0]):
                            self.model.grid.move_agent(self, agent.pos)
                    else:
                        print("reached else.")
        
        
    def isInter(self):
        newPos = [self.pos[0],self.pos[1]]
        list = self.model.grid[self.pos] 
        direction = "Double"
        for agent in list:
            if(isinstance(agent,Road)):
                if(agent.direction == "Down"):
                    direction = "Down"
                elif(agent.direction == "Up"):
                    direction = "Up"
                elif(agent.direction == "Right"):
                    direction = "Right"
                elif(agent.direction == "Left"):
                    direction = "Left"
        if(direction == "Double"):
            return True
        return False

    def diagMove(self):
        newPos = [self.pos[0],self.pos[1]]
        if(self.distX > 0):
            newPos[0] += 1
        else:
            newPos[0] -= 1
        if(self.distY > 0):
            newPos[1] += 1
        else:
            newPos[1] -= 1
        for agent in self.model.grid[tuple(newPos)]:
            if(isinstance(agent,Road)):
                self.model.grid.move_agent(self, tuple(newPos))
        self.straightMove()



    def destMove(self):
        loop = False
        for cell in self.interPassed:
            if(cell == self.pos):
                loop = True
        self.interPassed.append(self.pos)
        newPos = [self.pos[0],self.pos[1]]
        list = self.model.grid[self.pos] 
        direction = ""
        for agent in list:
            if(isinstance(agent,Road)):
                if(agent.direction == "RightDown"):
                    direction = "RightDown"
                elif(agent.direction == "RightUp"):
                    direction = "RightUp"
                elif(agent.direction == "LeftDown"):
                    direction = "LeftDown"
                elif(agent.direction == "LeftUp"):
                    direction = "LeftUp"  
    
        
        if(loop):
            if(abs(self.distX) > abs(self.distY)):
                self.lastInter = direction
                if(self.distX > 0):
                    if(direction == "RightDown"):
                        newPos[1] -= 2
                    elif(direction == "RightUp"):
                        newPos[1] += 2
                    elif(direction == "LeftUp"): #posible cambio
                        newPos[1] += 2
                    else:
                        newPos[1] -= 2
                else:
                    if(direction == "LeftDown"):
                        newPos[1] -= 2
                    elif(direction == "LeftUp"):
                        newPos[1] += 2
                    elif(direction == "RightUp"):
                        newPos[1] += 2
                    else:
                        newPos[0] += 2
            else:
                if(self.distY > 0):
                    if(direction == "RightUp"): 
                        newPos[0] += 2
                    elif(direction == "LeftUp"):
                        newPos[0] -= 2
                    elif(direction == "RightDown"):
                        newPos[0] += 2
                    else:
                        newPos[0] -= 2
                else:
                    if(direction == "RightDown"):
                        newPos[0] += 2
                    elif(direction == "LeftDown"):
                        newPos[0] -= 2
                    elif(direction == "RightUp"):
                        newPos[0] += 2
                    else:
                        newPos[0] -= 2
        elif(not loop):
            if(abs(self.distX) > abs(self.distY)):
                if(self.distX > 0):
                    if(direction == "RightDown" or direction == "RightUp"):
                        newPos[0] += 1
                    elif(direction == "LeftUp"):
                        newPos[1] += 1
                    else:
                        newPos[1] -= 1
                else:
                    if(direction == "LeftDown" or direction == "LeftUp"):
                        newPos[0] -= 1
                    elif(direction == "RightUp"):
                        newPos[1] += 1
                    else:
                        newPos[1] -= 1
            else:
                if(self.distY > 0):
                    if(direction == "RightUp" or direction == "LeftUp"):
                        newPos[1] += 1
                    elif(direction == "RightDown"):
                        newPos[0] += 1
                    else:
                        newPos[0] -= 1
                else:
                    if(direction == "RightDown" or direction == "LeftDown"):
                        newPos[1] -= 1
                    elif(direction == "RightUp"):
                        newPos[0] += 1
                    else:
                        newPos[0] -= 1
        self.model.grid.move_agent(self, tuple(newPos))

    def semMove(self):
        newPos = [self.pos[0],self.pos[1]]
        list = self.model.grid[self.pos] 
        for agent in list:
            if(isinstance(agent,Road)):
                if(agent.direction == "Down"):
                    newPos[1] -= 2
                elif(agent.direction == "Up"):
                    newPos[1] += 2
                elif(agent.direction == "Right"):
                    newPos[0] += 2
                elif(agent.direction == "Left"):
                    newPos[0] -= 2
        self.model.grid.move_agent(self, tuple(newPos))
        
    
    def step(self):
        if(self.condition != "Goal"):
            print("El destino es: " + str(self.destination))
            self.distY = self.destination[1] - self.pos[1]
            self.distX = self.destination[0] - self.pos[0]
            if(self.whichLight() == "Red"):
                print("Mini: redLight")
                self.inter = True
            elif(self.whichLight() == "Green" and self.inter) or (self.inter and not self.interCheck()):
                print("Mini: greenLight and inter on or inter on no inter neighbors")
                self.inter = False
            elif(self.interCheck()):
                print("Mini: inter neighbor on")
                self.inter = True

    def advance(self):
        if(self.condition != "Goal"):
            if(self.interCheck()):
                print("Inter in range")
                pass
            elif(self.destRange()):
                print("destination in range")
                self.model.grid.move_agent(self, self.destination)
                self.condition = "Goal"
            elif(self.whichLight() == "Green"):
                print("greenLight")
                self.semMove()
            elif(self.whichLight() == "Red"):
                print("redLight")
                pass
            elif((not self.carCheck() or self.waited >= 2) and self.isInter()):
                print("no car obst and intersection")
                self.destMove()
                self.waited = 0
            elif(abs(self.distX) == 2 and abs(self.distY) == 2):
                self.diagMove()
            elif(not self.carCheck()):
                print("no car obst")
                self.straightMove()
            elif(self.carCheck()):
                print("car obst")
                self.waited += 1
                pass
            else:
                print("else.")
                self.straightMove()

class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass

class Destination(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
