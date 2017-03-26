import json
from operator import itemgetter


def schedule(data):
    data = json.loads(data)
    print(data)


class State:

    def neighboors(self):
        ''''Returns the list of neighboors of the state'''
        pass

    def value(self):
        '''Returns the objective value of the state'''
        pass

    @classmethod
    def generate_random_state(cls):
        pass


def hill_climbing(initial_state):
    current_state = initial_state
    current_value = current_state.value()

    while True:
        neighboors = [(n, n.value()) for n in current_state.neighboors()]
        best_neighbour, best_value = max(neighboors, itemgetter(1))

        if best_value > current_value:
            current_value = best_value
            current_state = best_neighbour
        else:
            return current_state


def random_restart_hill_climbing(max_iters=100):
    best_state = None
    best_value = None

    for iteration in range(max_iters):
        initial_state = State.generate_random_state()
        current_solution = hill_climbing(initial_state)
        current_value = current_solution.value()

        if best_value is None or current_value > best_value:
            best_value = current_value
            best_state = current_solution

    return best_state

if __name__ == '__main__':
    data = open('input_example.json', 'rt').read()
    schedule(data)
