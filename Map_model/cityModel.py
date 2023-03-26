import random
# For random.choice() which allows random choices from a list
import simpy
# import simpy for discrete simulation use
import pprint
import turtle
turtle.tracer(0)

env = simpy.Environment()
# Initializes discrete simulation environment as 'env' using simpy


class Ramp:
    # Ramps are either on or off ramps,
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


class Intersection:
    # When a road connects to a road, you need to know what intersection is there.
    # An intersection can have a latitude and longitude and can tell you which roads it’s connected to.
    def __init__(self, name, pos, connections, resource_count):
        self.name = name
        self.pos = pos
        self.connections = connections
        self.resource_count = resource_count
        self.resource = simpy.Resource(env, capacity=resource_count)


class HwyIntersection:
    # When a highway connects to a highway, you need to know what highway_intersection is there.
    def __init__(self, name, pos, connections, resource_count):
        self.name = name
        self.pos = pos
        self.connections = connections
        self.resource_count = resource_count
        self.resource = simpy.Resource(env, capacity=resource_count)


class Highway:
    # Creates the highways
    def __init__(self, name, connections, speed):
        self.name = name
        self.connections = connections
        self.speed = speed


class Road:
    # Creates the major roads
    def __init__(self, name, connections, speed):
        self.name = name
        self.connections = connections
        self.speed = speed


class EndPoint:
    # Entrance, exit, or just dead-end points
    def __init__(self, env, name, pos, connections, resource_count):
        self.env = env
        self.name = name
        self.pos = pos
        self.connections = connections
        self.resource_count = resource_count
        self.resource = simpy.Resource(env, capacity=resource_count)


class Truck:
    #  Makes the Truck when passed to an object
    def __init__(self, env, name, occupants, start_from, previous_location, travel_next, finish_at, gps, turt, turt_text):
        self.env = env
        self.name = name
        self.workers = occupants
        self.start_from = start_from
        self.previous_location = previous_location
        self.travel_next = travel_next
        self.finish_at = finish_at
        self.gps = gps
        self.turt = turt
        self.turt_text = turt_text

        self.action = env.process(self.run())

    def enqueue(self):
        #  Lines up trucks at a node and requests a resource as needed
        global interaction_alert
        arrival_time = env.now
        if isinstance(self.start_from, Ramp) or isinstance(self.start_from, EndPoint):
            print("Ramp or endpoint, not waiting")
        else:
            print(f"{self.name} enqueuing at {self.start_from.name} at  {arrival_time}")
            with self.start_from.resource.request() as req:
                yield req

                # do something with resource
                received_resource_time = env.now
                wait_time = received_resource_time - arrival_time
                print(f"{self.name} waited {wait_time} seconds")
                if wait_time > 0:
                    interaction_alert.append(f"{self.name} had to give right of way at "
                                             f"{self.start_from.name} at {arrival_time}")

                yield self.env.timeout(3)  # simulate time it takes for truck to cross road
            print(f"{self.name} has finished crossing {self.start_from.name} at {env.now}")

    def traverse(self):
        global finished_trucks
        trip_count = 0
        # Loop until destination arrived at
        while True:
            destinations = []  # Holds choices generated below
            print(f"\n{self.name}")
            print(f"{self.name} Preparing to move from {self.start_from.name}")
            for i in self.start_from.connections:
                # Passes current location's parent road index to curr_indexroad
                current_index = self.start_from.connections.index(i)
                # passes current i of current_parent_road
                current_parent_road = self.start_from.connections[current_index]
                print(f"[{current_index + 1}/{len(self.start_from.connections)}]")
                # Current road
                print(f"Generating travel options from "
                      f"{self.start_from.name}'s {current_parent_road.name} parent connection")

                print(end=f"{current_parent_road.name}: [")
                for location in current_parent_road.connections:
                    print(location.name, end=", ")
                print(end="]")
                curr_road_index = current_parent_road.connections.index(self.start_from)

                print(f"\nChecking closest travel options for {self.start_from.name},"
                      f" currently index [{curr_road_index}] in its parent {current_parent_road.name}")
                # Check if objects after current index
                if curr_road_index < len(current_parent_road.connections) - 1:
                    # Next potential locale becomes next_place
                    next_place = current_parent_road.connections[curr_road_index + 1]
                    print(f"    ! Right index is {next_place.name}")

                    # if next is same as last place and endpoint, no
                    if next_place == self.previous_location and isinstance(next_place, EndPoint):
                        print(f"    ! {next_place.name} was the last place, not appending")
                    else:
                        print(f"    + Appending right index {next_place.name}")
                        destinations.append(next_place)  # add next_place to11
                        print(current_parent_road.speed)
                else:
                    print("     ? There is no right index")
                if curr_road_index > 0:  # # Check if objects before current index
                    next_place = current_parent_road.connections[curr_road_index - 1]
                    print(f"    ! Left index is {next_place.name}")

                    if next_place == self.previous_location and isinstance(next_place, EndPoint):
                        print(f"    ! {next_place.name} was the last place, not appending")
                        pass
                    else:
                        print(f"    + Appending left index {next_place.name}")
                        destinations.append(next_place)
                        print(current_parent_road.speed)
                else:
                    print("     ? There is no left index")

            print(end=f"Places that {self.name} can travel to: ")
            for i in destinations:
                print(f"{i.name}", end=', ')

            random_choice = random.choice(destinations)
            self.travel_next = random_choice
            self.previous_location = self.start_from
            self.start_from = random_choice
            trip_count += 1

            print(f"\n{self.name} randomly picks {random_choice.name}")
            miles_between, coord_distance = distance(self.previous_location, self.start_from)
            trip_length, trip_speed = travel_time(miles_between, current_parent_road.speed)
            print(current_parent_road.speed)
            print(f"Trip expected to last {trip_length} seconds at {trip_speed}mph")

            yield env.process(self.coordinate_crawl(coord_distance, trip_length))
            #yield env.timeout(trip_length)
            yield env.process(self.enqueue())
            print(f"{trip_count} movements, current time {env.now}")

            if self.start_from == self.finish_at:
                print(f"You have arrived at {self.finish_at.name} after {trip_count} locations")
                finished_trucks.append(f"{self.name} finished after "
                                       f"{convert_seconds(env.now)} or "
                                       f"{env.now} seconds, {trip_count} movements, ")
                return

    # def __init__(self, env, name, occupants, start_from, previous_location, travel_next, finish_at, gps):
    def coordinate_crawl(self, distance, duration):
        global process_locations_per_second
        start = convert_coordinate(self.previous_location.pos)
        current = start
        end = convert_coordinate(self.travel_next.pos)
        #print(f"{self.previous_location.name}, {self.previous_location.pos} start and end is {self.travel_next.name}, {self.travel_next.pos}")
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        delta = distance / duration

        for i in range(duration):
            current = (current[0] + delta * dx / distance, current[1] + delta * dy / distance)
            current = round(current[0], 2), round(current[1], 2)
            # current is now a correct coordinate
            #print(f"Incremented coord is now {current}, started at {self.previous_location.pos}")

            process_locations_per_second[env.now][f"{self.name}"] = current
            #print(f"{self.name} did a coordcrawl")
            yield self.env.timeout(1)  # simulate time spent moving 1 second

        current = convert_coordinate(self.start_from.pos)
        process_locations_per_second[env.now][f"{self.name}"] = current


        return

    #  Suggestion, replace your time increment with env.now for realistic sim time

    def run(self):
        #  Starts the truck object process in the simulation
        global truck_resource_times

        request_resource_time = env.now
        print(f"{self.name} requesting to leave at {request_resource_time}")

        with employees.request() as req:
            yield req
            resource_received_time = env.now
            truck_resource_times.append(f"{self.name} received departure-resource at "
                                        f"{convert_seconds(resource_received_time)} or "
                                        f"{resource_received_time} seconds")
            print(f"\n                                                "
                  f"{self.name} granted resource, leaving at {resource_received_time}")
            # do something with the resource until exiting the with block
            yield env.process(self.traverse())
            print(f"{self.name} has finished, calling it a day")
        # resource released at 'with' exit
        print(f"Releasing employee")





def second_key_maker(env):
    global process_locations_per_second

    while True:
        process_locations_per_second[env.now] = {}
        #print(f"executed key maker at {env.now}")
        yield env.timeout(1)


def distance(location1, location2):
    # You can use on any object with a pos attribute
    x1, y1 = location1.pos  # take parameter 1, pass x and y coordinate to x1, y1
    x2, y2 = location2.pos
    # Distance formula between two x,y points
    dist = round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 2)
    # ft. Hardcode how many feet per increment on the road network diagram
    feet_per_increment = 500
    feet = dist * feet_per_increment
    # feet converted to miles, rounded to 2 places
    miles = round(feet * 0.0001894, 2)
    print(f"{miles} miles between {location1.name} and {location2.name}")
    return miles, dist


def travel_time(miles, speed):
    # calculates hours to travel x miles at y speed
    time_hours = miles / speed
    # convert to seconds and round up
    time_seconds = round(time_hours * 3600)
    return time_seconds, speed


def convert_seconds(seconds):
    # Easily represent seconds in hours, minutes, seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def convert_coordinate(coord):

    # Convert coordinates to diagram compatible coordinates from its unique origin
    # x = 2.285, y = 2.72, for each square increment on diagram
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


def global_print(global1, global2, global3):
    # Prints global variable lists
    for i in global1:
        print(i)
    for i in global2:
        if len(global2) == 0:
            break
        else:
            print(i)
    for i in global3:
        print(i)


def turtle_commander(truck, pos):
    if pos == None:
        return
    else:
        truck.turt.setpos(pos)
        truck.turt_text.setpos(truck.turt.position())
        truck.turt_text.write(f"{truck.name}")


def dict_looper(nested_dict):
    global stored_turtles

    turtle.setworldcoordinates(-20, -20, 20, 20)
    # create a screen object
    screen = turtle.Screen()
    # set the background image
    screen.bgpic("C:\\Users\\kjpre\\PycharmProjects\\DES-Project-SP23\\Map_model\\diagram.png")
    screen.title("Road Network, Subvectio MN")

    level = 0

    while True:
        t1_text.clear()
        t2_text.clear()
        t3_text.clear()
        t4_text.clear()
        t5_text.clear()

        print(f"{level} at {nested_dict[level].items()}")
        for i in truck_list:
            turtle_commander(i, nested_dict[level].get(f"{i.name}"))

        turtle.update()
        user_input = input("enter continue, '\\' back")
        if user_input == '\\':
            level -= 1
        else:
            level += 1


# Highway instantiation (2 highways)
hwy1 = Highway('highway1', [], 45)
hwy2 = Highway('highway2', [], 45)

# Highway Intersection instantiation (1 hwy intersect)
highwayIntersection1 = HwyIntersection("Hw1_Hw2", (10.5, 14.4), [hwy1, hwy2], 1)

# Road instantiation (6 roads)
road1 = Road('road1', [], 25)
road2 = Road('road2', [], 25)
road3 = Road('road3', [], 25)
road4 = Road('road4', [], 25)
road5 = Road('road5', [], 25)
road6 = Road('road6', [], 25)

# Ramp instantiation (5 ramps)
onRamp1 = Ramp('onRamp1', (4.5, 5.7), [road1, hwy1], True, 'right', 1)
onRamp2 = Ramp('onRamp2', (8.2, 14.3), [road5, hwy2], True, 'left', 1)
offRamp1 = Ramp('offRamp1', (3.8, 6.3), [hwy1, road6], False, 'left', 1)
offRamp2 = Ramp('offRamp2', (11.7, 16.2), [hwy1, road3], False, 'right', 1)
offRamp3 = Ramp('offRamp3', (8.7, 14.8), [hwy2, road5], False, 'right', 1)

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
road1.connections += [endpoint3, intersection2, intersection1, onRamp1]
road2.connections += [endpoint2, intersection1, intersection4, intersection5, endpoint6]
road3.connections += [endpoint1, intersection2, intersection3, offRamp2]
road4.connections += [endpoint4, intersection3, intersection4, intersection6, intersection7, endpoint8]
road5.connections += [endpoint5, intersection5, offRamp3, onRamp2, intersection6, intersection8, endpoint9]
road6.connections += [endpoint7, intersection7, intersection8, offRamp1]

#  circular dependency, append objects to highways to prevent error
hwy1.connections += [endpoint10, offRamp2, highwayIntersection1, offRamp1, onRamp1, endpoint12]
hwy2.connections += [endpoint11, onRamp2, offRamp3, highwayIntersection1, endpoint13]

t1 = turtle.Turtle()
t1.pencolor("red")
t1_text = turtle.Turtle()
t1_text.ht()

t2 = turtle.Turtle()
t2.pencolor("blue")
t2_text = turtle.Turtle()
t2_text.ht()

t3 = turtle.Turtle()
t3.pencolor("green")
t3_text = turtle.Turtle()
t3_text.ht()

t4 = turtle.Turtle()
t4.pencolor("purple")
t4_text = turtle.Turtle()
t4_text.ht()

t5 = turtle.Turtle()
t5_text = turtle.Turtle()
t5_text.ht()

stored_turtles = []
stored_turtles.append(t1)
stored_turtles.append(t2)
stored_turtles.append(t3)
stored_turtles.append(t4)
stored_turtles.append(t5)

env.process(second_key_maker(env))
# Have this before truck objects to ensure it runs first

#  def __init__(self, env, name, occupants, start_from, previous_location, travel_next, finish_at, gps):
Truck1 = Truck(env, 'Truck1', 2, endpoint3, [], [], endpoint9, [], t1, t1_text)
Truck2 = Truck(env, 'Truck2', 2, endpoint3, [], [], endpoint9, [], t2, t2_text)
Truck3 = Truck(env, 'Truck3', 2, endpoint3, [], [], endpoint9, [], t3, t3_text)
Truck4 = Truck(env, 'Truck4', 2, endpoint3, [], [], endpoint9, [], t4, t4_text)
Truck5 = Truck(env, 'Truck5', 2, endpoint3, [], [], endpoint9, [], t5, t5_text)

truck_list = []
truck_list.append(Truck1)
truck_list.append(Truck2)
truck_list.append(Truck3)
truck_list.append(Truck4)
truck_list.append(Truck5)

finished_trucks = []
truck_resource_times = []
interaction_alert = []
process_locations_per_second = {}



if __name__ == '__main__':  # Main guard, prevents running sim on module import to unittest tester.py

    sim_time = 3600
    employees = simpy.Resource(env, capacity=20)
    env.run(until=sim_time)
    print("\n\n")

    global_print(finished_trucks, truck_resource_times, interaction_alert)

    #pprint.pprint(process_locations_per_second)
    dict_looper(process_locations_per_second)

    turtle.mainloop()
