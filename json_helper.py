import json
"""reading the ship file to add all the users ships to the dataspace"""


def to_dict(self):
    """creates a dict from ship params"""
    return {
        'captain': self.captain,
        'cannons': self.cannons,
        'crew': self.crew,
        'armor': self.armor,
        'sails': self.sails,
        'gold': self.gold,
        'win': self.win,
        'loss': self.loss,
        'x': self.x,
        'y': self.y
    }


def from_dict(self, json_data=None):
    """creates a ship based on a dict"""
    if json_data is None:
        return None

    self.captain = json_data['captain']
    self.cannons = json_data['cannons']
    self.crew = json_data['crew']
    self.armor = json_data['armor']
    self.sails = json_data['sails']
    self.gold = json_data['gold']
    self.win = json_data['win']
    self.loss = json_data['loss']
    self.x = json_data['x']
    self.y = json_data['y']

    # should this be here?
    self.position = json_data['position']

    return True


def write_ships(ship):
    ships[ship.position] = ship


with open("ship_file.json", "r") as read_file:
    first = read_file.read(1)
    global ships
    ships = []
    if first:
        read_file.seek(0)
        json_data = json.load(read_file)
        for s in json_data:
            ships.append(s)

index = 0
for ship in ships:
    ship["ship_name"] = ship["captain"] + "\'s ship"
    ship["win"] = 0
    ship["loss"] = 0
    ship["x"] = 0
    ship["y"] = 0
    ships[index] = ship
    index += 1
with open("ship_file.json", "w") as write_file:
    json.dump(ships, write_file)
