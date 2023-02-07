import heapq  # imports package heapq, which is a built-in Priority Queue package

# NOTE: simPy is a simulation framework, heapq is a package tool. Both work well together (i think)

stopSignQueue = []  # initialize queue
# Or
# stopSignQueue = [(1, 'Truck A', 'High Priority')]


heapq.heappush(stopSignQueue, (3, 'Truck C', 'Low Priority'))  # first index has priority over the next index
heapq.heappush(stopSignQueue, (1, 'Truck A', 'High Priority'))  # notice you can have more than just 2
heapq.heappush(stopSignQueue, (2, 'Truck B', 'Medium Priority'))
# so heapq maintains the heap property for the smallest value, 1 comes first.
# but notice that 3 and 2 aren't ordered. That's because smallest is always
# first (cuz heap), but everything else maintains order based on push order. Cool

stopSignQueueCopy = list(stopSignQueue)  # So for loop isn't affected by dequeue and prints 3, not 2

for i in stopSignQueueCopy:
    print(heapq.heappop(stopSignQueue), " can go.")  # dequeues the highest priority (first) element


