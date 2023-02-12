import math  # Needed for Haversine formula for calculating distance between intersection cords


class Ramp:  # When a road connects to a highway, you need to know what ramp is there.
    # pos stands for 'position',it consists of the latitude and longitude as ( , )
    def __init__(self, name, pos, connections):
        self.name = name
        self.pos = pos
        self.connections = connections

    def __str__(self):  # Prints object attributes, still figuring this out
        return f"{self.name}, {self.pos}, {self.connections}"


class Intersection:  # When a road connects to a road, you need to know what intersection is there.
    # An intersection can have a latitude and longitude and can tell you which roads it’s connected to.
    def __init__(self, name, pos, connections):
        self.name = name
        self.pos = pos
        self.connections = connections

    def __str__(self):
        return f"{self.name}, {self.pos}, {self.connections}"


class HwyIntersection:  # When a highway connects to a highway, you need to know what highway_intersection is there.
    def __init__(self, name, pos, connections):
        self.name = name
        self.pos = pos
        self.connections = connections

    def __str__(self):
        return f"{self.name}, {self.pos}, {self.connections}"


class Highway:  # Creates the highways
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    def __str__(self):
        return f"{self.name}, {self.connections}"


class Road:  # Creates the major roads
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    def __str__(self):
        return f"{self.name}, {self.connections}"


# distance() checks for same road, then reports distance between the two intersections in km based on long and lat
def distance(intersection1, intersection2):  # You can use Intersection, Ramp, or HwyIntersection class objects
    same_road = False
    road_name = ''
    # Compare both intersections for a shared connection (road)
    for i in intersection1.connections:
        for x in intersection2.connections:
            if i == x:
                same_road = True
                road_name = i
                break

    if same_road:  # Checks if true
        print("{} and {} are on the same road at {}".format(intersection1.name, intersection2.name, road_name.name))
    else:
        print("{} and {} are [NOT] on the same road".format(intersection1.name, intersection2.name))

    # Distance calculation
    lat1, lon1 = intersection1.pos  # tuple unpacking, assigns the values within the 'pos' attribute to lat & lon
    lat2, lon2 = intersection2.pos
    radius = 6371  # Earth's radius in km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    #  This formula for Haversine was taken from We3schools

    return "Distance between the two is {}Km\n".format(d)  # returns the distance in km


def distance_func_test():  # Test distance func between same road and diff road intersections
    #  Same road tests
    print(distance(inter1, inter2), "Expected output: road1\n")
    print(distance(onramp2, inter4), "Expected output: road5\n")
    print(distance(onramp2, offramp3), "Expected output: hwy2\n")
    #  Missing highway intersection test
    #  Diff road tests
    print(distance(inter1, inter3), "Expected output: NOT\n")
    print(distance(onramp1, inter4), "Expected output: NOT\n")
    print(distance(onramp1, offramp3), "Expected output: NOT\n")
    #  Missing highway intersection test


def see_connections(obj):  # Loops through an object's connections and prints them
    print(obj.name, end=" with connections: ")
    for i in obj.connections:
        print(i.name, end=", ")
    print("\n")


def navigate(road):  # work in progress method for traveling objects
    # Take current road, find connections, let user choose location, record choice, update current, loop at new road
    while True:
        choices = []
        print("You are currently at {}".format(road.name))
        print("You can travel to any of these intersections on this road:  ")
        for i in road.connections:
            choices.append(i)
            print(i.name, end=", ")
        print("\n")
        usr_choice = input("    Enter index 0 ... n to select destination\n")
        usr_choice = int(usr_choice)
        print("You have chosen ", choices[usr_choice].name)
        road = choices[usr_choice].name
        print("You can travel to any of these roads from this intersection:  ")
        choices = []

        for x in road.connections:
            choices.append(x)
            print(x.name, end=", ")
        print("\n")
        usr_choice = input("    Enter index 0 ... n to select destination\n")
        usr_choice = int(usr_choice)
        print("You have chosen ", choices[usr_choice].name)


# Highway instantiation (2 highways)
hwy1 = Highway('hwy1', [])
hwy2 = Highway('hwy2', [])
# Road instantiation (6 roads)
road1 = Road('road1', [])
road2 = Road('road2', [])
road3 = Road('road3', [])
road4 = Road('road4', [])
road5 = Road('road5', [])
road6 = Road('road6', [])
# Intersection instantiation (8 intersections)
inter1 = Intersection('inter1', (51.5074, 0.1278), [road1, road2])
inter2 = Intersection('inter2', (40.7128, 74.0060), [road1, road3])
inter3 = Intersection('inter3', (1, 1), [road3, road4])
inter4 = Intersection('inter4', (1, 1), [road4, road5])
inter5 = Intersection('inter5', (1, 1), [road2, road5])
inter6 = Intersection('inter6', (1, 1), [road4, road5])
inter7 = Intersection('inter7', (1, 1), [road4, road6])
inter8 = Intersection('inter8', (1, 1), [road5, road6])
# Ramp instantiation (5 ramps)
onramp1 = Ramp('onramp1', (1, 1), [road1, hwy1])
onramp2 = Ramp('onramp2', (1, 1), [road5, hwy2])
offramp1 = Ramp('offramp1', (1, 1), [hwy1, road6])
offramp2 = Ramp('offramp2', (1, 1), [hwy1, road3])
offramp3 = Ramp('offramp3', (1, 1), [hwy2, road5])
# Highway Intersection instantiation (1 hwy intersect)
hwyinter1 = HwyIntersection("Hw1_Hw2", (1, 1), [hwy1, hwy2])

#  circular dependency created accidentally, append objects to road to prevent error, need to fix this
road1.connections += [inter1, inter2, onramp1]
road2.connections += [inter1, inter4, inter5]
road3.connections += [inter2, inter3, offramp2]
road4.connections += [inter3, inter4, inter6, inter7]
road5.connections += [inter5, inter6, inter8, onramp2, offramp3]
road6.connections += [inter7, inter8, offramp1]
hwy1.connections += [onramp1, offramp1, offramp2, hwyinter1]
hwy2.connections += [onramp2, offramp3, hwyinter1]


see_connections(hwy1)
see_connections(inter1)
see_connections(inter3)
see_connections(road5)
see_connections(offramp3)

distance_func_test()

navigate(road1)

