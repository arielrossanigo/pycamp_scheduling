import json
import random
from collections import OrderedDict
from itertools import combinations
from operator import itemgetter

from munch import munchify

IMPOSIBLE_COST = 1000000


def schedule(data):
    data = json.loads(data)
    problem = PyCampScheduleProblem(data)
    best_solution = random_restart_hill_climbing(problem)
    return best_solution


class PyCampScheduleProblem:
    def __init__(self, data):
        self.data = munchify(data)
        self.project_list = list(self.data.projects.keys())
        self.total_participants = len(set([vote
                                           for pr in self.data.projects.values()
                                           for vote in pr.votes]))

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
        responsables_collisions_cost = 0
        participant_collisions_cost = 0
        responsable_not_available_cost = 0
        most_voted_cost = 0
        slot_population_cost = 0
        project_not_in_priority_slot_cost = 0

        slots_and_projects = OrderedDict()
        for slot in self.data.available_slots:
            slots_and_projects[slot] = [proj for proj, proj_slot in state if proj_slot == slot]

        for slot_number, (slot, slot_projects) in enumerate(slots_and_projects.items()):
            for proj1, proj2 in combinations(slot_projects, 2):
                set_resp_1 = set(self.data.projects[proj1].responsables)
                set_resp_2 = set(self.data.projects[proj2].responsables)

                # Cost for having responsables collisions
                if len(set_resp_1.intersection(set_resp_2)) > 0:
                    responsables_collisions_cost += IMPOSIBLE_COST

                # Cost for having voters collisions
                set_vot_1 = set(self.data.projects[proj1].votes)
                set_vot_2 = set(self.data.projects[proj2].votes)
                votes_collisions = len(set_vot_1.intersection(set_vot_2))
                participant_collisions_cost += votes_collisions

            # Cost for having multiple projects in the same slot and preference
            # for more occupadied slots at the begining
            project_quantity = len(slot_projects)
            slot_population_cost += (3 ** project_quantity) + (slot_number * project_quantity)

            # Cost according to the quantity of votes. It's prefered that most voted projects
            # were at the begining
            vote_quantity = sum([len(self.data.projects[project]) for project in slot_projects])
            most_voted_cost += (slot_number * vote_quantity) / self.total_participants

        for project, slot in state:
            project_data = self.data.projects[project]
            # Cost for having projects in slots where responsables are not available
            responsables = project_data.responsables
            for resp in responsables:
                if slot not in self.data.responsable_available_slots[resp]:
                    responsable_not_available_cost += IMPOSIBLE_COST

            # Cost for having a project outside priority slots
            priority_slots = project_data.priority_slots
            if len(priority_slots) > 0 and slot not in priority_slots:
                project_not_in_priority_slot_cost += 10

        return -1 * (
            responsables_collisions_cost +
            participant_collisions_cost +
            responsable_not_available_cost +
            most_voted_cost +
            slot_population_cost +
            project_not_in_priority_slot_cost
        )

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
            lines.append('+{:-<6s}+{:-<32s}+{:-<32s}+{:-<4s}+'.format('', '', '', ''))
            slot_project_lines = []
            for project, project_slot in sorted_by_slot:
                if project_slot == slot:
                    responsables = ', '.join(problem.data.projects[project].responsables)
                    number_of_votes = len(problem.data.projects[project].votes)
                    slot_project_lines.append(
                        '|{:^6s}| {:30s} | {:30s} | {:2d} |'.format(
                            slot, project, responsables, number_of_votes)
                    )

            if len(slot_project_lines) > 0:
                lines.extend(slot_project_lines)
            else:
                lines.append('|{:^6s}|{:32s}|{:32s}|{:4s}|'.format(slot, '', '', ''))
        lines.append('+{:-<6s}+{:-<32s}+{:-<32s}+{:-<4s}+'.format('', '', '', ''))
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


def random_restart_hill_climbing(problem, max_iters=100, max_iters_without_improvement=10):
    best_state = None
    best_value = None

    number_of_iterations_without_improvement = 0
    for iteration in range(max_iters):
        print('Iteration {} # Best value {}'.format(iteration, best_value))
        initial_state = problem.generate_random_state()
        current_solution = hill_climbing(problem, initial_state)
        current_value = problem.value(current_solution)

        if best_value is None or current_value > best_value:
            best_value = current_value
            best_state = current_solution

            number_of_iterations_without_improvement = 0
        else:
            number_of_iterations_without_improvement += 1
            if number_of_iterations_without_improvement == max_iters_without_improvement:
                break

    return best_state

if __name__ == '__main__':
    data = open('input_example.json', 'rt').read()

    data = json.loads(data)
    problem = PyCampScheduleProblem(data)
    best_solution = random_restart_hill_climbing(problem,
                                                 max_iters=10000,
                                                 max_iters_without_improvement=5)
    problem.print_state(best_solution)
