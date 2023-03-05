import turtle
turtle.setworldcoordinates(-20, -20, 20, 20)

# create a screen object
screen = turtle.Screen()

# set the background image
screen.bgpic("C:\\Users\\kjpre\\PycharmProjects\\DES-Project-SP23\\Map_model\\diagram.png")

# create a turtle object

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




class turtleMake:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

def turtle_update(turtle_obj, list):
    t = turtle_obj
    print("Starting turtle move")
    t.pensize(5)
    t.penup()
    t.goto(list[0])
    t.pendown()
    for i in list:
        t.goto(i)



# x = 2.285, y = 2.72

object1 = (-20.6, -27.6)
object2 = (10.704, -11.008)
object3 = (6.820, -11.280)
object4 = (2.707, -11.280)
object5 = (-10.318, -12.096)
object6 = (3.392, 11.568)
object7 = (-0.721, 12.656)
object8 = (-6.890, 4.224)
object9 = (-13.745, -4.480)

obj_list = []

obj_list.append(object2)
obj_list.append(object3)
obj_list.append(object4)
obj_list.append(object5)
obj_list.append(object6)
obj_list.append(object7)
obj_list.append(object8)
obj_list.append(object9)

turtl1 = turtleMake("blue", 2)

cord = (3, 8.5)
print(convert_coordinate(cord))

turtle_update(turtle, obj_list)

turtle.mainloop()  #you need this or main code pauses
