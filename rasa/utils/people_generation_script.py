import json
import random


def main():
    # number of people to generate
    n_of_people = 30

    # possible values for gender
    _gender = ["male", "female"]

    # possible values for colors
    _colors = [
        "blue",
        "white",
        "black",
        "red",
        "green",
        "yellow",
        "orange",
        "purple",
        "pink",
        "brown",
        "gray"
    ]

    # possible values for hat and bag
    _bool = ["true", "false"]
    # possible values for passages, from 0 to X
    _passages = 10
    # possible values for persistence, from 1 to X
    _persistence = 120

    output = dict()
    output["people"] = []

    for i in range(1, n_of_people + 1):
        person = dict()

        person["id"] = i
        person["gender"] = random.choice(_gender)
        person["bag"] = random.choice(_bool)
        person["hat"] = random.choice(_bool)
        person["upper_color"] = random.choice(_colors)
        person["lower_color"] = random.choice(_colors)

        passages = random.choice(range(0, _passages))
        person["roi1_passages"] = passages
        if passages > 0:
            person["roi1_persistence_time"] = random.choice(range(1, _persistence))
        else:
            person["roi1_persistence_time"] = 0

        passages = random.choice(range(0, _passages))
        person["roi2_passages"] = passages
        if passages > 0:
            person["roi2_persistence_time"] = random.choice(range(1, _persistence))
        else:
            person["roi2_persistence_time"] = 0

        output["people"].append(person)

    # saving file
    filename = "../output.json"
    with open(filename, "w") as outfile:
        outfile.write(json.dumps(output, indent=4))


if __name__ == '__main__':
    main()
