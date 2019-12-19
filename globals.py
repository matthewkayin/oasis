def point_in_rect(x, y, rect):
    return x >= rect[0] and x <= rect[0] + rect[2] and y >= rect[1] and y <= rect[1] + rect[3]
