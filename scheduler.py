import json
import random
from itertools import combinations
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
        cost = 0

        # Cost for having responsables collisions
        state_as_dict = dict(state)
        for proj1, proj2 in combinations(self.project_list, 2):
            if state_as_dict[proj1] == state_as_dict[proj2]:
                set_resp_1 = set(self.data.projects[proj1].responsables)
                set_resp_2 = set(self.data.projects[proj2].responsables)
                if len(set_resp_1.intersection(set_resp_2)) > 0:
                    cost += 1000

        return -1 * cost

    def generate_random_state(self):
        res = []
        for project in self.project_list:
            random_slot = random.choice(self.data.available_slots)
            res.append((project, random_slot))
        return res

    def print_state(self, state):
        sorted_by_slot = sorted(state, key=itemgetter(1))
        lines = []
        for slot in self.data.available_slots:
            lines.append('+{:-<6s}+{:-<32s}+{:-<32s}+'.format('', '', ''))
            slot_project_lines = []
            for project, project_slot in sorted_by_slot:
                if project_slot == slot:
                    responsables = ', '.join(problem.data.projects[project].responsables)
                    slot_project_lines.append(
                        '|{:^6s}| {:30s} | {:30s} |'.format(slot, project, responsables)
                    )

            if len(slot_project_lines) > 0:
                lines.extend(slot_project_lines)
            else:
                lines.append('|{:^6s}|{:32s}|{:32s}|'.format(slot, '', ''))
        lines.append('+{:-<6s}+{:-<32s}+{:-<32s}+'.format('', '', ''))
        print('\n'.join(lines))


def hill_climbing(problem, initial_state):
    current_state = initial_state
    current_value = problem.value(initial_state)

    while True:
        neighboors = [(n, problem.value(n)) for n in problem.neighboors(current_state)]
        best_neighbour, best_value = max(neighboors, key=itemgetter(1))

        if best_value > current_value:
            current_value = best_value
            current_state = best_neighbour
        else:
            return current_state


def random_restart_hill_climbing(problem, max_iters=100):
    best_state = None
    best_value = None

    for iteration in range(max_iters):
        print('Iteration {} # Best value {}'.format(iteration, best_value))
        initial_state = problem.generate_random_state()
        current_solution = hill_climbing(problem, initial_state)
        current_value = problem.value(current_solution)

        if best_value is None or current_value > best_value:
            best_value = current_value
            best_state = current_solution

        if best_value == 0:
            break

    return best_state

if __name__ == '__main__':
    data = open('input_example.json', 'rt').read()

    data = json.loads(data)
    problem = PyCampScheduleProblem(data)
    best_solution = random_restart_hill_climbing(problem)
