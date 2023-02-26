import random  # For random.choice() which allows random choices from a list


class Ramp:  # Ramps are either on or off ramps,
    # pos stands for 'position',it consists of the latitude and longitude as ( , )
    # r_type is either true or false, true meaning it's an ON ramp, false meaning it's an OFF ramp
    def __init__(self, name, pos, connections, r_type):
        self.name = name
        self.pos = pos
        self.connections = connections
        self.r_type = r_type


class Intersection:  # When a road connects to a road, you need to know what intersection is there.
    # An intersection can have a latitude and longitude and can tell you which roads it’s connected to.
    def __init__(self, name, pos, connections):
        self.name = name
        self.pos = pos
        self.connections = connections


class HwyIntersection:  # When a highway connects to a highway, you need to know what highway_intersection is there.
    def __init__(self, name, pos, connections):
        self.name = name
        self.pos = pos
        self.connections = connections


class Highway:  # Creates the highways
    def __init__(self, name, connections, speed):
        self.name = name
        self.connections = connections
        self.speed = speed


class Road:  # Creates the major roads
    def __init__(self, name, connections, speed):
        self.name = name
        self.connections = connections
        self.speed = speed


class EndPoint:  # Entrance and exit points for the simPy trucks
    def __init__(self, name, pos, connections):
        self.name = name
        self.pos = pos
        self.connections = connections


def distance(intersection1, intersection2):  # You can use on any object with a pos attribute
    x1, y1 = intersection1.pos  # take parameter 1, pass x and y coordinate to x1, y1
    x2, y2 = intersection2.pos

    dist = round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 2)  # Distance formula between two x,y points
    feet = dist * 500  # ft. Hardcode how many feet per increment on the road network diagram
    miles = round(feet * 0.0001894, 2)  # feet converted to miles, rounded to 2 places
    print(f"[Dist.] {miles} miles between {intersection1.name} and {intersection1.name}")
    return miles


def travel_time(miles, speed):  # Time = distance / speed
    time = miles / speed  # calculates hours to travel x miles at y speed
    minutes = round(time * 60, 2)  # minutes
    '# seconds = round(minutes * 60, 0)  # seconds, rounded'
    return minutes  # or seconds


# Highway instantiation (2 highways)
hwy1 = Highway('hwy1', [], 45)
hwy2 = Highway('hwy2', [], 45)

# Highway Intersection instantiation (1 hwy intersect)
hwyinter1 = HwyIntersection("Hw1_Hw2", (10.5, 14.4), [hwy1, hwy2])

# Road instantiation (6 roads)
road1 = Road('road1', [], 25)
road2 = Road('road2', [], 25)
road3 = Road('road3', [], 25)
road4 = Road('road4', [], 25)
road5 = Road('road5', [], 25)
road6 = Road('road6', [], 25)

# Ramp instantiation (5 ramps)
onramp1 = Ramp('onramp1', (4.5, 5.7), [road1, hwy1], True)
onramp2 = Ramp('onramp2', (8.2, 14.3), [road5, hwy2], True)
offramp1 = Ramp('offramp1', (3.8, 6.3), [hwy1, road6], False)
offramp2 = Ramp('offramp2', (11.7, 16.2), [hwy1, road3], False)
offramp3 = Ramp('offramp3', (8.7, 14.8), [hwy2, road5], False)

# Intersection instantiation (8 intersections)
inter1 = Intersection('inter1', (10.2, 6), [road1, road2])
inter2 = Intersection('inter2', (12, 6), [road1, road3])
inter3 = Intersection('inter3', (11.8, 12.2), [road3, road4])
inter4 = Intersection('inter4', (10, 12), [road2, road4])
inter5 = Intersection('inter5', (10, 16.3), [road2, road5])
inter6 = Intersection('inter6', (6, 11.7), [road4, road5])
inter7 = Intersection('inter7', (3.6, 11.6), [road4, road6])
inter8 = Intersection('inter8', (3.7, 9.3), [road5, road6])

#  Endpoint instantiation (13 endpoints)
endpoint1 = EndPoint('endpoint1', (12, 3.5), [road3])
endpoint2 = EndPoint('endpoint2', (10.2, 3.7), [road2])
endpoint3 = EndPoint('endpoint3', (13.7, 6.1), [road1])
endpoint4 = EndPoint('endpoint4', (13.7, 12.2), [road4])
endpoint5 = EndPoint('endpoint5', (10.7, 17.1), [road5])
endpoint6 = EndPoint('endpoint6', (10, 17.9), [road2])
endpoint7 = EndPoint('endpoint7', (3.4, 17.6), [road6])
endpoint8 = EndPoint('endpoint8', (2.5, 11.5), [road4])
endpoint9 = EndPoint('endpoint9', (3, 8.5), [road5])
endpoint10 = EndPoint('endpoint10', (12.5, 20), [hwy1])
endpoint11 = EndPoint('endpoint11', (1, 17.5), [hwy2])
endpoint12 = EndPoint('endpoint12', (5.5, 1), [hwy1])
endpoint13 = EndPoint('endpoint13', (16, 15.5), [hwy2])

#  circular dependency, append objects to road to prevent error
road1.connections += [endpoint3, inter2, inter1, onramp1]
road2.connections += [endpoint2, inter1, inter4, inter5, endpoint6]
road3.connections += [endpoint1, inter2, inter3, offramp2]
road4.connections += [endpoint4, inter3, inter4, inter6, inter7, endpoint8]
road5.connections += [endpoint5, inter5, offramp3, onramp2, inter6, inter8, endpoint9]
road6.connections += [endpoint7, inter7, inter8, offramp1]

#  circular dependency, append objects to highways to prevent error
hwy1.connections += [endpoint10, offramp2, hwyinter1, offramp1, onramp1, endpoint12]
hwy2.connections += [endpoint11, onramp2, offramp3, hwyinter1, endpoint13]


def traverse(current, end_location):
    """
    :param current: Current location within road network
    :param end_location: Desired location to end travel at
    :Output: Doesn't return anything at the moment, prints a lot for understanding how objects are being traversed in
    the road network. Once the code is finalized, unneeded printing can be commented out.

    Currently, every road and highway object has an attribute called connections which is an ordered list of all the
    connected objects. The objects are ordered as they occur in the diagram of the road network:
    road1.connections ----> [endpoint3, inter2, inter1, onRamp1]

    The code uses the roads and highways to find the connections of objects, finds the next and previous index, and
    appends them to a list choices IF they are not a recent location unless they are and endpoint, at which point to
    leave the previous location must be traveled. The objects in the list will be randomly picked from, as no route
    algorithm exists yet.

        Issues:
    1. Traverse function could have a new function made from the existing code used for generating the travel
    choices for connected roads at a location.
    2. Illegal movements are made right now. Traveling from Road objects to offRamp Ramp objects isn't allowed.
    Traveling from an onRamp to another offRamp immediately across a highway shouldn't be possible, this would
    require adding attributes to highway like lanes.
    3. Fixing the illegal ramp movements would also require changing the choice generation code in traverse, because
    not all Ramp objects are the end of a road (e.g. offRamp3, onRamp2) and so if they are not a legal move and
    shouldn't be traveled to, instead of NOT appending them, the code should loop back and decrement or increment
    to whichever index in the next direction, should it exist, to find something else to travel to. Otherwise, you can
    not pass beyond that point.
    4. The parent road used to calculate the speed to travel between locations doesn't seem to always match the
    road that is actually being traveled. I don't know if this is true, but I have feeling. Need testing.
    """

    last_place = []
    trip_count = 0
    while True:  # Loop until destination arrived at
        destinations = []  # Holds choices generated below
        for i in current.connections:
            print(f"\n[T] Starting at {current.name}")
            current_index = current.connections.index(i)  # Passes current location's parent road index to curr_index
            current_parent_road = current.connections[current_index]  # passes current i'th road to current_parent_road
            print(f"[T] Generating travel options from {current_parent_road.name}")  # Current roadd
            print(f"[T] {current_parent_road.name} is index [{current_index}] in parented road list of {len(current.connections) - 1}")

            print(end=f"{current_parent_road.name}: [")
            for location in current_parent_road.connections:
                print(location.name, end=", ")
            print(end="]")
            print(f"\n[T] Location is currently {current.name}, index [{current_index}] in {current_parent_road.name}")

            curr_roadindex = current_parent_road.connections.index(current)

            if curr_roadindex < len(current_parent_road.connections) - 1:  # Check if objects after current index
                next_place = current_parent_road.connections[curr_roadindex + 1]  # Next potential locale becomes next_place
                print(f"    Right index is {next_place.name}")

                if next_place == last_place and isinstance(next_place, EndPoint):  # if next is same as last place and endpoint, no
                    print(f"    {next_place.name} was the last place, not appending")
                else:
                    print(f"    Appending right index {next_place.name}")
                    destinations.append(next_place)  # add next_place to

            if curr_roadindex > 0:  # # Check if objects before current index
                next_place = current_parent_road.connections[curr_roadindex - 1]
                print(f"    Left index location is {next_place.name}")
                if next_place == last_place and isinstance(next_place, EndPoint):
                    print(f"    {next_place.name} was the last place, not appending")
                else:
                    print(f"    Appending left index {next_place.name}")
                    destinations.append(next_place)

            print(end=f"[random.choices]: ")
            for i in destinations:
                print(f"{i.name}", end=', ')
        # input("continue?\n ")

        random_choice = random.choice(destinations)
        last_place = current
        current = random_choice
        trip_count += 1

        print(f"\n[random]: {random_choice.name} selected")
        t_time = travel_time(distance(current, end_location), current_parent_road.speed)
        print(f"[Time] {t_time} to get from {current.name} to {end_location.name} at {current_parent_road.speed}mph")

        if current == end_location:
            print(f"\n\nYou have arrived at {end_location.name} after {trip_count} locations")
            break


traverse(endpoint3, endpoint9)

