from priorityQueue import PriorityQueue

truck_queue = PriorityQueue()

for i in range (1,11):# just 10 truck sample assumed the traffic light is red.
    truck_queue.priority_enqueue(i, " truck queued at a stop light.")

#just dequeing
while not truck_queue.isEmpty():
    print(truck_queue.dequeue())
