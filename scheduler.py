import json
import random
from operator import itemgetter

from munch import munchify


def schedule(data):
    data = json.loads(data)
    problem = PyCampScheduleProblem(data)
    best_solution = random_restart_hill_climbing(problem)
    return best_solution


class PyCampScheduleProblem:
    def __init__(self, data):
        self.data = munchify(data)
        self.project_list = list(self.data.projects.keys())

    def neighboors(self, state):
        ''''Returns the list of neighboors of the state'''
        neighboors = []
        for project in self.project_list:
            for slot in self.data.available_slots:
                d = dict(state)
                current_slot = d[project]
                if current_slot != slot:
                    d[project] = slot
                    new_state = list(d.items())
                    neighboors.append(new_state)
        return neighboors

    def value(self, state):
        '''Returns the objective value of the state'''
        pass

    def generate_random_state(self):
        res = []
        for project in self.project_list:
            random_slot = random.choice(self.data.available_slots)
            res.append((project, random_slot))
        return res


def hill_climbing(problem, initial_state):
    current_state = initial_state
    current_value = problem.value(initial_state)

    while True:
        neighboors = [(n, problem.value(n)) for n in problem.neighboors(current_state)]
        best_neighbour, best_value = max(neighboors, itemgetter(1))

        if best_value > current_value:
            current_value = best_value
            current_state = best_neighbour
        else:
            return current_state


def random_restart_hill_climbing(problem, max_iters=100):
    best_state = None
    best_value = None

    for iteration in range(max_iters):
        initial_state = problem.generate_random_state()
        current_solution = hill_climbing(problem, initial_state)
        current_value = problem.value(current_solution)

        if best_value is None or current_value > best_value:
            best_value = current_value
            best_state = current_solution

    return best_state

if __name__ == '__main__':
    data = open('input_example.json', 'rt').read()
    schedule(data)
