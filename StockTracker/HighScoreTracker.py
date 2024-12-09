import json


def save_high_scores(high_scores, file_path="high_scores.json"):
    # Convert each high_score object in the list to a dictionary
    high_scores_dict = [score.to_dict() for score in high_scores]

    # Write the list of dictionaries to a file as JSON
    with open(file_path, "w") as file:
        json.dump(high_scores_dict, file)


def load_high_scores(filename="high_scores.json"):
    try:
        with open(filename, "r") as file:
            file_to_load = json.load(file)
            return [high_score.from_dict(data) for data in file_to_load]
    except FileNotFoundError:
        return []  # No high scores yet


def update_high_scores(new_high_score, high_scores, max_scores=5):
    high_scores.append(new_high_score)
    high_scores.sort(key=lambda x: x.score, reverse=True)
    return high_scores[:max_scores]


class high_score:
    def __init__(self, name="", score=0):
        self.name = name
        self.score = score

    def set_score(self, new_score):
        self.score = new_score

    def set_name(self, new_name):
        self.name = new_name

    def get_name_and_score(self):
        return [self.name, self.score]

    # Convert to a dictionary for JSON serialization
    def to_dict(self):
        return {"name": self.name, "score": self.score}

    # Create a high_score object from a dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(name=data.get("name", ""), score=data.get("score", 0))
