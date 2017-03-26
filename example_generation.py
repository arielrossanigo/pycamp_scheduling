import json
import random

input_example = {
    "available_slots": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
    "responsable_available_slots": {
        "Matias": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "David": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Ariel": ["A3", "A4", "A5", "B2", "B3", "B4", "B5"],
        "Fisa": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Gilgamezh": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Facu": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Diego": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Agustin": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Manuq": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Litox": ["B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Mario": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Zoe": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"],
        "Luri": ["A3", "A4", "A5", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4"]
    },
    "projects": {
        "Programar, que es eso?": {"responsables": ["Matias", "David"], "priority_slots": ['A3']},
        "Vis de redes neuronales": {"responsables": ["Ariel"]},
        "Mirror Pypi": {"responsables": ["Fisa", "Gilgamezh"]},
        "Linkode": {"responsables": ["Facu", "Matias"]},
        "Recordium": {"responsables": ["Facu"]},
        "Radio to podcast": {"responsables": ["Diego"]},
        "Choppycamp": {"responsables": ["Fisa"]},
        "LabJM": {"responsables": ["Agustin"]},
        "Pilas": {"responsables": ["Manuq"]},
        "Cuentos a epub": {"responsables": ["Diego"]},
        "Web PyAr": {"responsables": ["Litox"]},
        "Moravec": {"responsables": ["Mario"]},
        "Raspi": {"responsables": ["David"]},
        "Fades": {"responsables": ["Facu", "Gilgamezh"]},
        "PyCamp voting manager": {"responsables": ["Zoe"]},
        "Easy Camp": {"responsables": ["Matias", "Luri"]},
        "Metaprogramacion": {"responsables": ["David"]},
        "Encajonar apps": {"responsables": ["Manuq"]},
        },
}

attendes = (list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") +
            list(set(input_example["responsable_available_slots"].keys())))
themes = ['web', 'desktop', 'mobile', 'ia', 'hardware', 'comunity', '']
difficult_levels = [1, 2, 3]

output_example = {}
slots = input_example['available_slots']
for i, (project_name, project) in enumerate(input_example["projects"].items()):
    project['votes'] = random.sample(attendes, random.randint(1, len(attendes)))
    project['difficult_level'] = random.choice(difficult_levels)
    project['theme'] = random.choice(themes)
    if "priority_slots" not in project:
        project["priority_slots"] = []

    output_example[project_name] = slots[i % len(slots)]

json.dump(input_example, open('input_example.json', 'wt'), indent=2)
json.dump(output_example, open('output_example.json', 'wt'), indent=2)
