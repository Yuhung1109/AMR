import os, time, eventlet

eventlet.monkey_patch()

#class return_values:
#    def __init__(self, a, b):
#        self.a = a
#        self.b = b

# def set_goal(x, y):
#     res = os.popen("rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped \ '{header: {frame_id: 'base_odom'}, pose: {position: {x: " + x + ", y: " + y + ", z: 0.000 }, orientation: {w: 1.000}}}'")
#     return res

# def get_pose():
#     res = os.popen("rosrun tf tf_echo /base_odom /base_laser")
#     num = 0
#     for read_num in range(3):
#         xy = res.readline()
#         temp = xy[16:29].split('u')[0].split('P')[0]
#         if num % 5 == 1:
#             data = temp.replace(' ', '')
#             for op in range(len(data)):
#                 if data[op] == ',':
#                     break
#             x = data[0:op]
#             y = data[op+1:len(data)]
#         num = num + 1
#     print(X)
#     print(Y)
#     return x

# def set_pose(x, y):
#     res = os.popen("rostopic pub /initialpose geometry_msgs/PointStamped \ '{header: {frame_id: 'base_odom'}, point: {x: " + x + ", y: " + y + ", z: 0.000}}'")
#     return res

#variable
point = 0 #ros location
direction = 0 # ros move direction
pointX = 0
pointY = 0
firstX = 0
firstY = 0

while(1):
    print("1")
    res = os.popen("rosrun tf tf_echo /base_odom /base_laser")
    num = 0
    for read_num in range(3):
        xy = res.readline()
        temp = xy[16:29].split('u')[0].split('P')[0]
        if num % 5 == 1:
            data = temp.replace(' ', '')
            for op in range(len(data)):
                if data[op] == ',':
                    break
            x = float(data[0:op])
            y = float(data[op+1:len(data)-1])
        num = num + 1
    print(x)
    print(y)
    # print("rostopic pub /initialpose geometry_msgs/PointStamped \ '{header: {frame_id: 'base_odom'}, point: {x: " + x + ", y: " + y + ", z: 0.000}}'")
    # with eventlet.Timeout(1, False):
    #     print("setpose")
    #     os.popen("rostopic pub /initialpose geometry_msgs/PointStamped \ '{header: {frame_id: 'base_odom'}, point: {x: " + str(x) + ", y: " + str(y) + ", z: 0.000}}'")
    # print("0")
    if (point == 5):
        point = 0
        direction = direction + 1
        print("wall")
    if (abs(pointX - x) < 0.1 and abs(pointY - y < 0.1)):
        point = point + 1
        print(point)
    else :
        point = 0
    if (direction == 0):
        print("direction0")
        x = x + 0.1
    elif (direction == 1):
        y = y + 0.1
    elif (direction == 2):
        x = x - 0.1
    else:
        y = y - 0.1
    #print("rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped \ '{header: {frame_id: 'base_odom'}, pose: {position: {x: " + str(x) + ", y: " + str(y) + ", z: 0.000 }, orientation: {w: 1.000}}}'")
    while 1:
        iscontinue = 0
        with eventlet.Timeout(1, False):
            print("setgoal")
            time.sleep(1)
            os.popen("rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped \ '{header: {frame_id: 'base_odom'}, pose: {position: {x: " + str(x) + ", y: " + str(y) + ", z: 0.000 }, orientation: {w: 1.000}}}'")
            iscontinue = 1
        if iscontinue == 0:
            break
    # print(res)
    print("end")
    if (firstX == x and firstY == y):
        break
    pointX = x
    pointY = y
    time.sleep(1)