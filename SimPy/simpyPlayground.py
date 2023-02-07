import simpy  # import sim and modeling library
env = simpy.Environment()  # creates new sim environment


class DeliveryTruck:
    def __init__(self, env, name, available_truck_spot, available_workers):
        self.env = env
        self.name = name
        self.available_truck_spot = available_truck_spot
        self.available_workers = available_workers
        self.action = env.process(self.run)


    def run(self):
        pass
    def truck(self, name, available_truck_spot):  # Models the truck
        arrive_time = env.now  # variable takes the current simulation time
        print(arrive_time, 'arip')
        print(f'{name} arriving at {arrive_time}')  # uses f string to print the truck name and current time
        with available_truck_spot.request() as req:  # creates a request for access to the resource and stores the request in the req variable
            yield req  # wait until request is granted
            print(f'{name} is entering loading dock at {env.now}')  # prints truck being loaded and the sim time
            print("speed")


            depart_time = env.now  # stores the current sim time in the variable
            print(depart_time,'dep')
        print(f'{name} loaded, departing at {depart_time} after {arrive_time - depart_time} of waiting and loading')


    def t_loader(self, name, available_workers):
        print(f'{name} is on call for loading')
        with available_workers.request() as req:
            yield req
            print(f'{name} is being loaded')
            yield env.timeout(10)


available_truck_spot = simpy.Resource(env, capacity=1)  # creates a resource, can only handle 1 truck at a time
available_workers = simpy.Resource(env, capacity=1)  # # creates a resource, can only handle 1 truck at a time
truck1 = DeliveryTruck(env, 'truck 1', available_truck_spot, available_workers)
print(truck1.name)
#truck2 = env.process(truck(env, 'truck 2', available_truck_spot))
#truck3 = env.process(truck(env, 'truck 3', available_truck_spot))

env.run(until=30)  # sim runs for 30 time units



