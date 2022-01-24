from math import inf, hypot


def get_object_on_xy(x, y, objects):
    objects_on_point = {}
    last_dist_from_center = inf
    for obj in objects:
        xmin, ymin, xmax, ymax = obj['xmin'], obj['ymin'], obj['xmax'], obj['ymax']
        center_x, center_y = (xmin + xmax) / 2, (ymin + ymax) / 2
        distance_from_center = hypot(x - center_x, y - center_y)

        if xmin <= x <= xmax and ymin <= y <= ymax and distance_from_center < last_dist_from_center:
            objects_on_point = obj
            last_dist_from_center = distance_from_center

    return objects_on_point


def get_gazed_object(gaze_points, objects):
    gaze_objs = []
    for gaze_point in gaze_points:
        x, y = gaze_point['x'], gaze_point['y']
        gaze_objs.append(get_object_on_xy(x=x, y=y, objects=objects))

    return gaze_objs
