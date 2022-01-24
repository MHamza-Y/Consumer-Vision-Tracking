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
            objects_on_point['x_gaze_point'] = int(x)
            objects_on_point['y_gaze_point'] = int(y)
            last_dist_from_center = distance_from_center

    return objects_on_point


def get_gazed_object(gaze_points, objects):
    gaze_objs = []
    for gaze_point in gaze_points:
        x, y = gaze_point['x'], gaze_point['y']
        obj = get_object_on_xy(x=x, y=y, objects=objects)
        print('a',obj)
        if obj:
            gaze_objs.append(obj)

    return gaze_objs
