# 18 roads, (accidentally wrote 2 road16's
# 8 intersections
# 5 ramps
# 1 Highway intersection

class Highways:
    def __init__(self, name):
        self.name = name


class OnRamp:
    def __init__(self, name, connected_road):
        self.name = name
        self.connected_road = connected_road


class Intersections:
    def __init__(self, name, roads):
        self.name = name
        self.roads = roads

    def __str__(self):
        return '{} with connected roads {}'.format(self.name, [Road.name for Road in self.roads])


class Roads:

    def __init__(self, name, length):
        self.name = name
        self.length = length

    def __str__(self):  # lets you print the object

        return f'{self.name}, length {self.length}'

        pass

    pass


SH_52 = Highways('SH_52')
CR_347 = Highways('CR_347')

Intersection52_347 = Intersections('52_347', [SH_52, CR_347])

OnRampRoad = Roads('OnRampRoad', 3)
OnRampRoad2 = Roads('OnRampRoad2', 3)
OffRampRoad = Roads('OffRampRoad', 3)
OffRampRoad2 = Roads('OffRampRoad2', 3)
OffRampRoad3 = Roads('OffRampRoad3', 3)

OnRamp_347 = OnRamp('OnRamp_347', OnRampRoad)
OffRamp_347 = OnRamp('OffRamp_347', OffRampRoad)
OffRamp2_347 = OnRamp('OffRamp2_347', OffRampRoad2)
OnRamp_51 = OnRamp('OnRamp_51', OnRampRoad2)
OffRamp_51 = OnRamp('OffRamp_51', OffRampRoad3)


Road1 = Roads('Road1', 10)
Road2 = Roads('Road2', 10)
Road3 = Roads('Road3', 10)
Road4 = Roads('Road4', 10)
Road5 = Roads('Road5', 10)
Road6 = Roads('Road6', 10)
Road7 = Roads('Road7', 10)
Road8 = Roads('Road8', 10)
Road9 = Roads('Road9', 10)
Road10 = Roads('Road10', 10)
Road11 = Roads('Road11', 10)
Road12 = Roads('Road12', 10)
Road13 = Roads('Road13', 10)
Road14 = Roads('Road14', 10)
Road15 = Roads('Road15', 10)
Road16 = Roads('Road16', 10)
Road17 = Roads('Road17', 10)
Road18 = Roads('Road18', 10)

Intersection1 = Intersections('Intersection1', [Road1, Road2, Road3, Road4])
Intersection2 = Intersections('Intersection2', [Road4, Road5, Road6, Road7])

'''
cityModelDict = {'Int1': [Road1, Road2, Road3, Road4],
                 'Int2': [Road1, Road2, Road3, Road4]
                  }
'''


def find_intersections_for_road(road_name, intersections_list):
    intersections = []
    for intersection in intersections_list:
        if road_name in [r.name for r in intersection.roads]:
            intersections.append(intersection.name)
    return intersections

intersections_list = [Intersection1, Intersection2, Intersection52_347]

road_name = 'Road4'
intersections = find_intersections_for_road(road_name, intersections_list)
print(f"Road {road_name} is in intersections: {intersections}")

def find_roads_for_intersection(intersection_name, intersections_list):
    for intersection in intersections_list:
        if intersection.name == intersection_name:
            return [road.name for road in intersection.roads]

intersections_list = [Intersection1, Intersection2, Intersection52_347]

intersection_name = 'Intersection1'
roads = find_roads_for_intersection(intersection_name, intersections_list)
print(f"Intersection {intersection_name} has roads: {roads}")