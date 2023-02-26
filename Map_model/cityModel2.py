import math  # Needed for Haversine formula for calculating distance between intersection cords
import simpy  # for creating the simulation
import random  # For random.choice() which allows random choices from a list

# Create simpy environment
env = simpy.Environment()  # Initializes simpy environment as 'env'

class Ramp:  # Ramps are either on or off ramps, you can take off ramps to exit highways,and on ramps to enter them from roads
    # pos stands for 'position',it consists of the latitude and longitude as ( , )
    # r_type is either true or false, true meaning it's an ON ramp, false meaning it's an OFF ramp
    def __init__(self, name, pos, connections, r_type):
        self.name = name
        self.pos = pos
        self.connections = connections
        self.r_type = r_type

    def __str__(self):  # Prints object attributes, still figuring this out
        return f"{self.name}"


class Intersection:  # When a road connects to a road, you need to know what intersection is there.
    # An intersection can have a latitude and longitude and can tell you which roads it’s connected to.
    def __init__(self, name, pos, connections):
        self.name = name
        self.pos = pos
        self.connections = connections

    def __str__(self):
        return f"{self.name}"


class HwyIntersection:  # When a highway connects to a highway, you need to know what highway_intersection is there.
    def __init__(self, name, pos, connections):
        self.name = name
        self.pos = pos
        self.connections = connections

    def __str__(self):
        return f"{self.name}"


class Highway:  # Creates the highways
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    def __str__(self):
        return f"{self.name}"


class Road:  # Creates the major roads
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    def __str__(self):
        return f"{self.name}"


class EndPoint:  # Entrance and exit points for the simPy trucks
    def __init__(self, name, pos, connections, resource_count):
        self.name = name
        self.pos = pos
        self.connections = connections
        self.resource_count = resource_count
        self.resource = simpy.Resource(env, capacity=resource_count)



    def __str__(self):
        return f"{self.name}"


class Truck:
    def __init__(self, env, name, workers, endpoint, prev_road, manifest):
        self.env = env
        self.name = name
        self.action = env.process(self.run())
        self.workers = workers
        self.endpoint = endpoint
        self.prev_road = prev_road
        self.manifest = manifest

    def endpoint_queue(self):
        print(f"{self.name} is queued at {self.endpoint} at:  {env.now}")
        arrival_time = env.now
        with self.endpoint.resource.request() as req:
            yield req
            depart_time = env.now
            print(f"{self.name} got resource for {self.endpoint} after:  {depart_time - arrival_time}")

            if not self.prev_road:  # If prev_road is not true (Is empty) then
                print("No prev road, enter road network")
                self.prev_road = self.endpoint

                return True

            else:
                print(f"{self.name} has reached {self.endpoint} at {env.now} ")
                return False


    def traverse(self):
        while True:
            choices = []  # stores list
            self.manifest.append(self.endpoint.name)
            print(f"{self.name} is currently at {self.endpoint.name},", "travel to any of these connections:  ")
            for i in self.endpoint.connections:  # creates a list of options based on connected objects
                if isinstance(i, Ramp) and i.r_type == True and isinstance(self.prev_road, HwyIntersection):
                    # if i is a ramp AND an ONRamp AND previous road is a highway intersect; then PASS
                    pass
                elif isinstance(i, Ramp) and i.r_type == False and isinstance(self.prev_road, Highway):
                    # if i is a ramp AND an offRamp AND previous road is a highway; then append
                    choices.append(i)  # add object to choice list
                    print(i.name, end=", ")  # print same line
                elif i == self.prev_road:  # check if i is the connection you were last on
                    pass  # skip appending to the choice list
                else:
                    choices.append(i)  # add object to choice list
                    print(i)
            usr_choice = random.choice(choices)
            print("------> Traveling to", usr_choice)
            self.prev_road = self.endpoint # current becomes previous
            self.endpoint = usr_choice  # current becomes user choice
            print("\nTime elapsed: ", env.now)
            yield env.timeout(1)
            print("workers currently left are", workers.capacity)
            #yield self.env.timeout(travel_time(distance(self.prev_road, self.endpoint), 15))


    def run(self):

        #  print(f'{self.name} is trucking, time now is {env.now}')
        yield env.process(self.endpoint_queue())
        yield env.process(self.traverse())


class HeavyTruck(Truck):
    def __init__(self, env, name, workers, endpoint, prev_road, manifest, idle_consumption):
        super().__init__(env, name, workers, endpoint, prev_road, manifest)
        self.idle_consumption = idle_consumption


class LiteTruck(Truck):
    def __init__(self, env, name, workers, endpoint, prev_road, manifest, idle_consumption):
        super().__init__(env, name, workers, endpoint, prev_road, manifest)
        self.idle_consumption = idle_consumption


def distance(intersection1, intersection2):  # You can use Intersection, Ramp, or HwyIntersection class objects
    # distance() checks for same road, then reports distance between the two intersections in km based on long and lat
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
    else:\
        print("{} and {} are [NOT] on the same road".format(intersection1.name, intersection2.name))

    # Distance calculation
    lat1, lon1 = intersection1.pos  # tuple unpacking, assigns the values within the 'pos' attribute to lat & lon
    lat2, lon2 = intersection2.pos
    radius = 6371  # Earth's radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    #  This formula for Haversine was taken from We3schools
    miles = d * 0.621371  # converts km to miles
    miles = round(miles, 2)  # rounds to 2 digits
    return miles  # returns the distance in km


def travel_time(miles, speed):
    time = miles / speed  # calculates hours to travel x miles at y speed
    time = time * 60  #hours
    time = round(time * 60, 0)  # seconds, rounded
    return time

def update_coordinates():  # for coding the diagram posistions qiuickly
    while True:
        # Initial values of lat and long
        lat = 37.7749
        long = -122.4227


        x = float(input("Enter X parameter: "))
        y = float(input("Enter Y parameter: "))


        lat += y * 0.001373
        long += x * 0.001373

        # Print the new values of lat and long
        print("New coordinates: ({}, {})".format(lat, long))
def navigate(road):  # Lets you manually traverse connected road network objects
    # Take current road, find connections, let user choose location, record choice, update current, loop at new road
    curr = road  # stores object passed by parameter
    prev_rd = curr  # stores last traveled road
    while True:
        choices = []  # stores list
        print("You are currently at {}".format(curr.name), "You can travel to any of these connections:  ")
        for i in curr.connections:  # creates a list of user options based on connected objects
            if isinstance(i, Ramp) and i.r_type == True and isinstance(prev_rd, HwyIntersection):
                # if i is a ramp AND an ONRamp AND previous road is a highway intersect; then PASS
                pass
            elif isinstance(i, Ramp) and i.r_type == False and isinstance(prev_rd, Highway):
                # if i is a ramp AND an offRamp AND previous road is a highway; then append
                choices.append(i)  # add object to choice list
                print(i.name, end=", ")  # print same line
            elif i == prev_rd:  # check if i is the connection you were last on
                pass  # skip appending to the choice list
            else:
                choices.append(i)  # add object to choice list
                print(i.name, end=", ")  # print same line
        usr_choice = int(input("    `Enter index 0 ... n to select destination\n"))
        print("You have chosen ", choices[usr_choice].name)
        prev_rd = curr  # current becomes previous
        curr = choices[usr_choice]  # current becomes user choice


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
inter1 = Intersection('inter1', (37.783138, -122.4088327), [road1, road2])
inter2 = Intersection('inter2', (37.783138, -122.40622400000001), [road1, road3])
inter3 = Intersection('inter3', (37.791513300000005, -122.40787160000001), [road3, road4])
inter4 = Intersection('inter4', (37.791376, -122.40897000000001), [road4, road5])
inter5 = Intersection('inter5', (37.7972799, -122.40897000000001), [road2, road5])
inter6 = Intersection('inter6', (37.790964100000004, -122.4145993), [road4, road5])
inter7 = Intersection('inter7', (37.792199800000006, -122.41775720000001), [road4, road6])
inter8 = Intersection('inter8', (37.783549900000004, -122.4176199), [road5, road6])
# Ramp instantiation (5 ramps)
onramp1 = Ramp('onramp1', (37.784236400000005, -122.4165215), [road1, hwy1], True)
onramp2 = Ramp('onramp2', (37.7943966, -122.4128144), [road5, hwy2], True)
offramp1 = Ramp('offramp1', (37.783412600000005, -122.4174826), [hwy1, road6], False)
offramp2 = Ramp('offramp2', (37.7972799, -122.40663590000001), [hwy1, road3], False)
offramp3 = Ramp('offramp3', (37.795220400000005, -122.4107549), [hwy2, road5], False)
# Highway Intersection instantiation (1 hwy intersect)
hwyinter1 = HwyIntersection("Hw1_Hw2", (37.7946712, -122.4081462), [hwy1, hwy2])

#  instantiate the road network endpoints of highways and roads
endpoint1 = EndPoint('endpoint1', (37.779705500000006, -122.40622400000001), [road3], 3)
endpoint2 = EndPoint('endpoint2', (37.7799801, -122.40897000000001), [road2], 3)
endpoint3 = EndPoint('endpoint3', (37.783138, -122.4037526), [road1], 1)
endpoint4 = EndPoint('endpoint4', (37.791650600000004, -122.4037526), [road4], 3)
endpoint5 = EndPoint('endpoint5', (37.798241000000004, -122.40787160000001), [road5], 3)
endpoint6 = EndPoint('endpoint6', (37.7994767, -122.40897000000001), [road2], 3)
endpoint7 = EndPoint('endpoint7', (37.799064800000004, -122.4181691), [road6], 3)
endpoint8 = EndPoint('endpoint8', (37.7906895, -122.4192675), [road4], 3)
endpoint9 = EndPoint('endpoint9', (37.786433200000005, -122.418581), [road5], 3)
endpoint10 = EndPoint('endpoint10', (37.80236, -122.40553750000001), [hwy1], 12)
endpoint11 = EndPoint('endpoint11', (37.798927500000005, -122.421327), [hwy2], 12)
endpoint12 = EndPoint('endpoint12', (37.776273, -122.4148739), [hwy1], 12)
endpoint13 = EndPoint('endpoint13', (37.7964561, -122.400732), [hwy2], 12)

#  circular dependency created accidentally, append objects to road to prevent error, need to fix this
road1.connections += [inter1, inter2, onramp1]
road2.connections += [inter1, inter4, inter5]
road3.connections += [inter2, inter3, offramp2]
road4.connections += [inter3, inter4, inter6, inter7]
road5.connections += [inter5, inter6, inter8, onramp2, offramp3]
road6.connections += [inter7, inter8, offramp1]
hwy1.connections += [onramp1, offramp1, offramp2, hwyinter1]
hwy2.connections += [onramp2, offramp3, hwyinter1]
inter8.connections += [endpoint9]
inter2.connections += [endpoint3]


# Create the simpy 'workers' resource and give it a capacity of 10
# Workers per truck are 2 per HeavyTruck, 1 per LiteTruck.
workers = simpy.Resource(env, capacity=12)

heavyTruck1 = HeavyTruck(env, 'heavyTruck1', 2, endpoint3, [], [], 1.7)
heavyTruck2 = HeavyTruck(env, 'heavyTruck2', 2, endpoint3, [], [], 1.7)
heavyTruck3 = HeavyTruck(env, 'heavyTruck3', 2, endpoint3, [], [], 1.7)
liteTruck1 = HeavyTruck(env, 'liteTruck1', 1, endpoint3, [], [], .5)
liteTruck2 = HeavyTruck(env, 'liteTruck2', 1, endpoint3, [], [], .5)
liteTruck3 = HeavyTruck(env, 'liteTruck3', 1, endpoint3, [], [], .5)
liteTruck4 = HeavyTruck(env, 'liteTruck4', 1, endpoint3, [], [], .5)

print("workers currently left are", workers.capacity)
#  Run simulation for 10 units,
env.run(until=10)

print("heavyTruck1's manifest is: ", heavyTruck1.manifest)

