import numpy as np

def control(error_x, error_y, error_z, kp):
    # Kp = 0.1 
    #"เห็น error เท่านี้ จะตอบสนองแรงแค่ไหน" ใหญ่ขึ้นเคลื่อนที่เข้าหา target ได้ไวขึ้น

    command_x = -kp * error_x
    command_y = -kp * error_y
    command_z = -kp * error_z

    return command_x, command_y, command_z

# error = control(0,-50)
# print(error)

#Feedback Loop , Closed Loop
# x = 80
# y = -50
# z = 0.5

# dt = 1.0

# for step in range(20):

    # error_x = x - 0
    # x = 80
    # desired_x = 0
    # error_x = 80 - 0
    #         = 
    error_x = x 
    
    # error_y = y - 0
    error_y = y

    # error_z = z - 1.0
    #เราต้องกำหนดก่อนว่า "จุดที่ต้องการให้ spacecraft ไปหยุด" คือที่ไหน
    #error = current - desired
    error_z = z - 1.0

    command_x, command_y, command_z = control(error_x, error_y, error_z)

    x = x + command_x * dt
    y = y + command_y * dt
    z = z + command_z * dt

    # print(step, x, y, z)