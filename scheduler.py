import json
from operator import itemgetter


def schedule(data):
    data = json.loads(data)
    problem = PyCampScheduleProblem(data)
    best_solution = random_restart_hill_climbing(problem)
    return best_solution


class PyCampScheduleProblem:
    def __init__(self, data):
        self.data = data

    def neighboors(self, state):
        ''''Returns the list of neighboors of the state'''
        pass

    def value(self, state):
        '''Returns the objective value of the state'''
        pass

    def generate_random_state(self):
        pass


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
