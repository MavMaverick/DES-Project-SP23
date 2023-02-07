from heapq import heappush, heappop
class PriorityQueue:
    def __init__(self):
        self._vehicles = []
    def priority_enqueue(self,priority, value): #takes two parameters, a priority and a value- as a tuple.
        heappush(self._vehicles,(priority,value))
    def dequeue(self):
        return heappop(self._vehicles)

    def isEmpty(self):
        return not self._vehicles