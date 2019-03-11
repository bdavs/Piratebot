import json

def write_json_file():
    with open("ship_file.json", "w") as write_file:
        json.dump(ships, write_file)


def update(ship, is_new=False):
    if is_new:
        ships.append(ship.to_dict())
    else:
        ships[ship.position] = ship.to_dict()
    write_json_file()

def find_ship(captain):
    """returns the ship based on captain from ships variable"""
    index = 0
    for s in ships:
        if s['captain'] == captain:
            s['position'] = index
            temp_ship = Ship(captain)
            temp_ship.from_dict(s)
            return temp_ship
        index += 1
    return None



class Ship:
    """defines a single instance of a ship"""
    def __init__(self, user):
        self.captain = user
        self.cannons = 1
        self.crew = 1
        self.armor = 1
        self.sails = 1
        self.hull = 110

        self.gold = 0

        self.position = 0

        #self.parts_amt = [self.cannons, self.crew, self.armor, self.sails]
    def info(self):
        """returns a str with basic parameters of the ship"""

        infostr = '\n'.join([str(self.cannons), str(self.crew), str(self.armor), str(self.sails)])
        """
                infostr = "This level {6} ship is captained by {4} \nIt has {0} cannons, {1} crew, {2} armor, and {3} sails \n"\
                  "Its coffers are holding {5} gold".\
            format(self.cannons, self.crew, self.armor, self.sails, self.captain, self.gold, self.level())
            """
        return infostr

    def level(self):
        """returns level of ship based on its primary features"""
        ship_level = int((self.cannons + self.crew + self.armor + self.sails) / 1) - 3
        return int(ship_level)

    def upgrade(self, parameter, amount, cost=0):
        """updates the parameters of the ship and subtracts the cost"""
        if parameter == "cannons":
            self.cannons += amount
        elif parameter == "crew":
            self.crew += amount
        elif parameter == "armor":
            self.armor += amount
        elif parameter == "sails":
            self.sails += amount
        else:
            return False

        self.gold -= cost
        super().update(self)
#        update(self)
        return True

    def upgrade_costs(self):
        info = []
        for part in [self.cannons, self.crew, self.armor, self.sails]:
            info.append(str(int(100 + float((part**1.2) * 20))))
        infostr = '\n'.join(info)
        return infostr

    def repair_hull(self):
        self.hull = 100 + self.armor * 5 + self.sails * 5

    def damage_hull(self, damage):
        self.hull -= damage

    def to_dict(self):
        """creates a dict from ship params"""
        return {
            'captain': self.captain,
            'cannons': self.cannons,
            'crew': self.crew,
            'armor': self.armor,
            'sails': self.sails,
            'gold': self.gold
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

        # should this be here?
        self.position = json_data['position']

"""reading the ship file to add all the users ships to the dataspace"""
with open("ship_file.json", "r") as read_file:
    first = read_file.read(1)
    global ships
    ships = []
    if first:
        read_file.seek(0)
        json_data = json.load(read_file)
        for s in json_data:
            ships.append(s)
