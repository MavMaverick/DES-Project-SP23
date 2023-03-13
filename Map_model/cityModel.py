import random  # For random.choice() which allows random choices from a list
import simpy  # for creating the simulation


# Create simpy environment
env = simpy.Environment()  # Initializes simpy environment as 'env'


class Ramp:  # Ramps are either on or off ramps,
    # pos stands for 'position',it consists of the latitude and longitude as ( , )
    # ramp_type is either true or false, true meaning it's an ON ramp, false meaning it's an OFF ramp
    def __init__(self, name, pos, connections, ramp_type, highway_side, resource_count):
        self.name = name
        self.pos = pos
        self.connections = connections
        self.ramp_type = ramp_type
        self.highway_side = highway_side
        self.resource_count = resource_count
        self.resource = simpy.Resource(env, capacity=resource_count)


class Intersection:  # When a road connects to a road, you need to know what intersection is there.
    # An intersection can have a latitude and longitude and can tell you which roads it’s connected to.
    def __init__(self, name, pos, connections, resource_count):
        self.name = name
        self.pos = pos
        self.connections = connections
        self.resource_count = resource_count
        self.resource = simpy.Resource(env, capacity=resource_count)


class HwyIntersection:  # When a highway connects to a highway, you need to know what highway_intersection is there.
    def __init__(self, name, pos, connections, resource_count):
        self.name = name
        self.pos = pos
        self.connections = connections
        self.resource_count = resource_count
        self.resource = simpy.Resource(env, capacity=resource_count)


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
    def __init__(self, env, name, pos, connections, resource_count):
        self.env = env
        self.name = name
        self.pos = pos
        self.connections = connections
        self.resource_count = resource_count
        self.resource = simpy.Resource(env, capacity=resource_count)

class Truck:
    def __init__(self, env, name, occupants, start_from, last_location, travel_next, finish_at, gps):
        self.env = env
        self.name = name
        self.workers = occupants
        self.start_from = start_from
        self.last_location = last_location
        self.travel_next = travel_next
        self.finish_at = finish_at
        self.gps = gps
        self.action = env.process(self.run())

    def enqueue(self):
        global interaction_alert
        arrival_time = env.now
        if isinstance(self.start_from, Ramp) or isinstance(self.start_from, EndPoint):
            print("Ramp or endpoint, not waiting")
        else:
            print(f"{self.name} enqueing at {self.start_from.name} at  {arrival_time}")
            with self.start_from.resource.request() as req:
                yield req
                # do something with resource
                received_resource_time = env.now
                wait_time = received_resource_time - arrival_time
                print(f"{self.name} waited {wait_time} seconds")
                if wait_time > 0:
                    interaction_alert.append(f"{self.name} had to give right of way at {self.start_from.name} at {arrival_time}")

                yield self.env.timeout(1)  # simulate time it takes for truck to cross road
            print(f"{self.name} has finished crossing {self.start_from.name} at {env.now}")

    def traverse(self):
        global finished_trucks
        trip_count = 0

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


        while True:  # Loop until destination arrived at
            destinations = []  # Holds choices generated below
            print(f"\n{self.name}")
            print(f"{self.name} Preparing to move from {self.start_from.name}")
            for i in self.start_from.connections:

                current_index = self.start_from.connections.index(i)  # Passes current location's parent road index to curr_indexroad
                current_parent_road = self.start_from.connections[current_index]  # passes current i'th  to current_parent_road
                print(f"[{current_index + 1}/{len(self.start_from.connections)}]")
                print(f"Generating travel options from {self.start_from.name}'s {current_parent_road.name} parent connection")  # Current roadd

                print(end=f"{current_parent_road.name}: [")
                for location in current_parent_road.connections:
                    print(location.name, end=", ")
                print(end="]")
                curr_roadindex = current_parent_road.connections.index(self.start_from)






                print(f"\nChecking closest travel options for {self.start_from.name}, currently index [{curr_roadindex}] in its parent {current_parent_road.name}")
                if curr_roadindex < len(current_parent_road.connections) - 1:  # Check if objects after current index
                    next_place = current_parent_road.connections[curr_roadindex + 1]  # Next potential locale becomes next_place
                    print(f"    ! Right index is {next_place.name}")

                    # if next is same as last place and endpoint, no
                    if next_place == self.last_location and isinstance(next_place, EndPoint):
                        print(f"    ! {next_place.name} was the last place, not appending")

                    # elif is Ramp and offramp and last is intersection
                    elif isinstance(next_place, Ramp) and next_place.ramp_type == False and isinstance(self.last_location, Intersection):
                        print("    ! Can't go to an offramp from intersection, checking if another right index...")
                        #  Increment current index within parent road list
                        curr_roadindex += 1
                        if curr_roadindex < len(current_parent_road.connections) - 1:  # Check if objects after current index
                            next_place = current_parent_road.connections[curr_roadindex + 1]  # Next potential locale becomes next_place
                            print(f"        ! Right index is {next_place.name}")
                            print("        !! Ruh-roh, better code a method if you plan to loop these checks// error")
                        else:
                            print("         !No more right index")
                    elif isinstance(next_place, Ramp) and next_place.ramp_type == True and isinstance(self.last_location, Ramp) and self.last_location.ramp_type == True:
                        print("     ! Can't go from an on-ramp to an on-ramp, checking if another right index...")
                    else:
                        print(f"    + Appending right index {next_place.name}")
                        destinations.append(next_place)  # add next_place to
                else:
                    print("     ? There is no right index")





                if curr_roadindex > 0:  # # Check if objects before current index
                    next_place = current_parent_road.connections[curr_roadindex - 1]
                    print(f"    ! Left index is {next_place.name}")

                    if next_place == self.last_location and isinstance(next_place, EndPoint):
                        print(f"    ! {next_place.name} was the last place, not appending")
                        pass
                    else:
                        print(f"    + Appending left index {next_place.name}")
                        destinations.append(next_place)
                else:
                    print("     ? There is no left index")



            print(end=f"Places that {self.name} can travel to: ")
            for i in destinations:
                print(f"{i.name}", end=', ')

            random_choice = random.choice(destinations)
            self.last_location = self.start_from
            self.start_from = random_choice
            trip_count += 1


            print(f"\n{self.name} randomly picks {random_choice.name}")
            miles_between = distance(self.last_location, self.start_from)
            trip_length, trip_speed = travel_time(miles_between, current_parent_road.speed)
            print(f"Trip expected to last {trip_length} seconds at {trip_speed}mph")

            yield env.timeout(trip_length)
            yield env.process(self.enqueue())
            print(f"{trip_count} movements, current time {env.now}")
            #input("continue?\n ")

            if self.start_from == self.finish_at:
                print(f"You have arrived at {self.finish_at.name} after {trip_count} locations")
                finished_trucks.append(f"\n{self.name} finished after {convert_seconds(env.now)} or {env.now} seconds, {trip_count} movements, ")
                return


    def run(self):
        global truck_resource_times

        request_resource_time = env.now
        print(f"{self.name} requesting to leave at {request_resource_time}")

        with employees.request() as req:
            yield req
            resource_received_time = env.now
            truck_resource_times.append(f"{self.name} received departure-resource at {convert_seconds(resource_received_time)} or {resource_received_time} seconds")
            print(f"\n                                                {self.name} granted resource, leaving at {resource_received_time}")
            # do something with the resource until exiting the with block
            yield env.process(self.traverse())
            print(f"{self.name} has finished, calling it a day")
        # resource released at 'with' exit
        print(f"Releasing employee")




def distance(intersection1, intersection2):  # You can use on any object with a pos attribute
    x1, y1 = intersection1.pos  # take parameter 1, pass x and y coordinate to x1, y1
    x2, y2 = intersection2.pos

    dist = round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 2)  # Distance formula between two x,y points
    feet_per_increment = 500  # ft. Hardcode how many feet per increment on the road network diagram
    feet = dist * feet_per_increment
    miles = round(feet * 0.0001894, 2)  # feet converted to miles, rounded to 2 places
    print(f"{miles} miles between {intersection1.name} and {intersection2.name}")
    return miles


def travel_time(miles, speed):
    time_hours = miles / speed  # calculates hours to travel x miles at y speed
    time_seconds = round(time_hours * 3600)  # convert to seconds and round up
    return time_seconds, speed

def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

#  # x = 2.285, y = 2.72
def convert_coordinate(coord):
    x, y = coord
    if x != 0:
        new_x = -20.6 + (x * 2.285)
    else:
        new_x = -20.6
    if y != 0:
        new_y = -27.6 + (y * 2.72)
    else:
        new_y = -27.6
    return round(new_x, 3), round(new_y, 3)




# Highway instantiation (2 highways)
hwy1 = Highway('hwy1', [], 45)
hwy2 = Highway('hwy2', [], 45)

# Highway Intersection instantiation (1 hwy intersect)
hwyinter1 = HwyIntersection("Hw1_Hw2", (10.5, 14.4), [hwy1, hwy2], 1)

# Road instantiation (6 roads)
road1 = Road('road1', [], 25)
road2 = Road('road2', [], 25)
road3 = Road('road3', [], 25)
road4 = Road('road4', [], 25)
road5 = Road('road5', [], 25)
road6 = Road('road6', [], 25)

# Ramp instantiation (5 ramps)
onramp1 = Ramp('onramp1', (4.5, 5.7), [road1, hwy1], True, 'right', 1)
onramp2 = Ramp('onramp2', (8.2, 14.3), [road5, hwy2], True, 'left', 1)
offramp1 = Ramp('offramp1', (3.8, 6.3), [hwy1, road6], False, 'left', 1)
offramp2 = Ramp('offramp2', (11.7, 16.2), [hwy1, road3], False, 'right', 1)
offramp3 = Ramp('offramp3', (8.7, 14.8), [hwy2, road5], False, 'right', 1)

# Intersection instantiation (8 intersections)
intersection1 = Intersection('intersection1', (10.2, 6), [road1, road2], 1)
intersection2 = Intersection('intersection2', (12, 6), [road1, road3], 1)
intersection3 = Intersection('intersection3', (11.8, 12.2), [road3, road4], 1)
intersection4 = Intersection('intersection4', (10, 12), [road2, road4], 1)
intersection5 = Intersection('intersection5', (10, 16.3), [road2, road5], 1)
intersection6 = Intersection('intersection6', (6, 11.7), [road4, road5], 1)
intersection7 = Intersection('intersection7', (3.6, 11.6), [road4, road6], 1)
intersection8 = Intersection('intersection8', (3.7, 9.3), [road5, road6], 1)

#  Endpoint instantiation (13 endpoints)
endpoint1 = EndPoint(env, 'endpoint1', (12, 3.5), [road3], 1)
endpoint2 = EndPoint(env, 'endpoint2', (10.2, 3.7), [road2], 1)
endpoint3 = EndPoint(env, 'endpoint3', (13.7, 6.1), [road1], 1)
endpoint4 = EndPoint(env, 'endpoint4', (13.7, 12.2), [road4], 1)
endpoint5 = EndPoint(env, 'endpoint5', (10.7, 17.1), [road5], 1)
endpoint6 = EndPoint(env, 'endpoint6', (10, 17.9), [road2], 1)
endpoint7 = EndPoint(env, 'endpoint7', (3.4, 17.6), [road6], 1)
endpoint8 = EndPoint(env, 'endpoint8', (2.5, 11.5), [road4], 1)
endpoint9 = EndPoint(env, 'endpoint9', (3, 8.5), [road5], 1)
endpoint10 = EndPoint(env, 'endpoint10', (12.5, 20), [hwy1], 1)
endpoint11 = EndPoint(env, 'endpoint11', (1, 17.5), [hwy2], 1)
endpoint12 = EndPoint(env, 'endpoint12', (5.5, 1), [hwy1], 1)
endpoint13 = EndPoint(env, 'endpoint13', (16, 15.5), [hwy2], 1)

#  circular dependency, append objects to road to prevent error
road1.connections += [endpoint3, intersection2, intersection1, onramp1]
road2.connections += [endpoint2, intersection1, intersection4, intersection5, endpoint6]
road3.connections += [endpoint1, intersection2, intersection3, offramp2]
road4.connections += [endpoint4, intersection3, intersection4, intersection6, intersection7, endpoint8]
road5.connections += [endpoint5, intersection5, offramp3, onramp2, intersection6, intersection8, endpoint9]
road6.connections += [endpoint7, intersection7, intersection8, offramp1]

#  circular dependency, append objects to highways to prevent error
hwy1.connections += [endpoint10, offramp2, hwyinter1, offramp1, onramp1, endpoint12]
hwy2.connections += [endpoint11, onramp2, offramp3, hwyinter1, endpoint13]


#  def __init__(self, env, name, occupants, start_from, last_location, travel_next, finish_at, gps):
Truck1 = Truck(env, 'Truck1', 2, endpoint3, [], [], endpoint9, [])
'''
Truck2 = Truck(env, 'Truck2', 2, endpoint3, [], [], endpoint9, [])
Truck3 = Truck(env, 'Truck3', 2, endpoint3, [], [], endpoint9, [])
Truck4 = Truck(env, 'Truck4', 2, endpoint3, [], [], endpoint9, [])
Truck5 = Truck(env, 'Truck5', 2, endpoint3, [], [], endpoint9, [])
'''
finished_trucks = []
truck_resource_times = []
interaction_alert = []

if __name__ == '__main__':  # Main guard, prevents running sim on module import to unittest absoluTest.py
    employees = simpy.Resource(env, capacity=20)

    env.run(until=300)

    print("\n")
    for i in truck_resource_times:
        print(i)

    for i in finished_trucks:
        if len(finished_trucks) == 0:
            break
        else:
            print(i)

    for i in interaction_alert:
        print(i)

