import math

def calculate_point_on_circle(center_x, center_y, radius, angle_in_degrees):
    # 将角度转换为弧度
    angle_in_radians = angle_in_degrees * (math.pi / 180)

    # 计算圆上的点的坐标
    point_x = center_x + radius * math.cos(angle_in_radians)
    point_y = center_y + radius * math.sin(angle_in_radians)

    return {'x': point_x, 'y': point_y}

def dir_to_angle(dir, keys = {}):
    if dir == 'up':
        if 'right' in keys:
            return -45
        if 'left' in keys:
            return 225
        return -90
    if dir == 'right':
        if 'down' in keys:
            return 45
        if 'up' in keys:
            return -45
        return 0
    if dir == 'down':
        if 'left' in keys:
            return 135
        if 'right' in keys:
            return 45
        return 90
    if dir == 'left':
        if 'up' in keys:
            return 225
        if 'down' in keys:
            return 135
        return 180