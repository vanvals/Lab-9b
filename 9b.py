"""
Created on Thu May 16 16:03:18 2024

@author: saravanvalkenburgh
"""
# Lab 9b
# Sara Van Valkenburgh

import random

params = {
    'world_size': (10, 10),  
    'num_agents': 50,        
    'same_pref': 0.3,        
    'max_iter': 10           
}

class Agent:
    def __init__(self, world, kind, same_pref):
        self.world = world
        self.kind = kind
        self.same_pref = same_pref
        self.location = None

    def move(self):
        if not self.is_happy():
            vacant_patches = self.world.find_vacant_patches()
            random.shuffle(vacant_patches)
            for patch in vacant_patches:
                if self.is_happy(patch):
                    self.world.grid[self.location] = None
                    self.location = patch
                    self.world.grid[patch] = self
                    return
                  
    def is_happy(self, loc=None):
        if loc is None:
            loc = self.location
        neighbors = self.world.get_neighbors(loc)
        similar_neighbors = sum(1 for neighbor in neighbors if neighbor and neighbor.kind == self.kind)
        total_neighbors = len(neighbors)
        if total_neighbors == 0:
            return False
        return (similar_neighbors / total_neighbors) >= self.same_pref

class World:
    def __init__(self, params):
        self.params = params
        self.grid = self.create_grid(params['world_size'])
        self.agents = self.create_agents(params['num_agents'], params['same_pref'])
        self.initialize_agents()

    def create_grid(self, world_size):
        return {(x, y): None for x in range(world_size[0]) for y in range(world_size[1])}

    def create_agents(self, num_agents, same_pref):
        kinds = ['red'] * (num_agents // 2) + ['blue'] * (num_agents // 2)
        random.shuffle(kinds)
        return [Agent(self, kind, same_pref) for kind in kinds]

    def initialize_agents(self):
        vacant_patches = list(self.grid.keys())
        random.shuffle(vacant_patches)
        for agent, patch in zip(self.agents, vacant_patches):
            self.grid[patch] = agent
            agent.location = patch

    def find_vacant_patches(self):
        return [loc for loc, occupant in self.grid.items() if occupant is None]

    def get_neighbors(self, loc):
        x, y = loc
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = []
        for dx, dy in directions:
            neighbor_loc = ((x + dx) % self.params['world_size'][0], (y + dy) % self.params['world_size'][1])
            neighbors.append(self.grid[neighbor_loc])
        return neighbors

    def simulate(self):
        for iteration in range(self.params['max_iter']):
            random.shuffle(self.agents)
            for agent in self.agents:
                agent.move()
            if all(agent.is_happy() for agent in self.agents):
                print(f'All agents are happy after {iteration + 1} iterations.')
                return
        print(f'Simulation ended after {self.params["max_iter"]} iterations.')

if __name__ == "__main__":
    world = World(params)
    world.simulate()
