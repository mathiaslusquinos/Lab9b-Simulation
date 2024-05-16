
# Name: Mathias Lusquinos (CNet ID: MLusquinos)
# Name in Canvas (and Gradescope): Mathias Lusquinos
# Name in Github: mathiaslusquinos

###To construct the simulation, I consulted:
###https://agentpy.readthedocs.io/en/latest/agentpy_segregation.html

import agentpy as ap

###Establishing parameters
params = {'same_pref': 0.5, 
          'ethnic_groups': 3, 
          'density': 0.8, 
          'world_size': 50, 
          'steps': 50}

###Establishing conditions of the model
class Agent(ap.Agent):
    def setup(self):
        self.grid = self.model.grid
        self.random = self.model.random
        self.group = self.random.choice(range(self.p.ethnic_groups))
        self.share_similar = 0
        self.happy = False
    def happiness(self):
        neighbors = self.grid.neighbors(self)
        similar = len([n for n in neighbors if n.group == self.group])
        ln = len(neighbors)
        self.share_similar = similar / ln if ln > 0 else 0
        self.happy = self.share_similar >= self.p.same_pref
    def search(self):
        new_spot = self.random.choice(self.model.grid.empty)
        self.grid.move_to(self, new_spot)
        
###Defining the model      
class World(ap.Model):
    def setup(self):
        s = self.p.world_size
        n = self.n = int(self.p.density * (s ** 2))
        self.grid = ap.Grid(self, (s, s), track_empty=True)
        self.agents = ap.AgentList(self, n, Agent)
        self.grid.add_agents(self.agents, random=True, empty=True)
    def update(self):
        self.agents.happiness()
        self.unhappy = self.agents.select(self.agents.happy == False)
        if len(self.unhappy) == 0:
            self.stop()
    def step(self):
        self.unhappy.search()
    def segregation(self):
        return round(sum(self.agents.share_similar) / self.n, 3)
    def end(self):
        self.report('agent_model_segregation', self.segregation())
        
###Setting the simulation to work        
model = World(params)
result_segregation = model.run()
print(result_segregation)
result_segregation['reporters']['agent_model_segregation']
