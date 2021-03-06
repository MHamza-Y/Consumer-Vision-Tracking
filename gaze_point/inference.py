import sys

import torch
from torch.autograd import Variable
from torch.nn import DataParallel
from gazenet import GazeNet
import numpy as np
import cv2
from PIL import Image, ImageOps

import operator

from utilss import data_transforms
from utilss import get_paste_kernel, kernel_map
import pupil_detection
from pre_processing import detect_face, get_face_rect_xy, get_eye_coordinates, normalized_xy


def generate_data_field(eye_point):
    """eye_point is (x, y) and between 0 and 1"""
    height, width = 224, 224
    x_grid = np.array(range(width)).reshape([1, width]).repeat(height, axis=0)
    y_grid = np.array(range(height)).reshape([height, 1]).repeat(width, axis=1)
    grid = np.stack((x_grid, y_grid)).astype(np.float32)

    x, y = eye_point
    x, y = x * width, y * height

    grid -= np.array([x, y]).reshape([2, 1, 1]).astype(np.float32)
    norm = np.sqrt(np.sum(grid ** 2, axis=0)).reshape([1, height, width])
    # avoid zero norm
    norm = np.maximum(norm, 0.1)
    grid /= norm
    return grid


def preprocess_image(image_path, eye):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # crop face
    x_c, y_c = eye
    x_0 = x_c - 0.15
    y_0 = y_c - 0.15
    x_1 = x_c + 0.15
    y_1 = y_c + 0.15
    if x_0 < 0:
        x_0 = 0
    if y_0 < 0:
        y_0 = 0
    if x_1 > 1:
        x_1 = 1
    if y_1 > 1:
        y_1 = 1

    h, w = image.shape[:2]
    face_image = image[int(y_0 * h):int(y_1 * h), int(x_0 * w):int(x_1 * w), :]
    # process face_image for face net
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    face_image = Image.fromarray(face_image)
    face_image = data_transforms['test'](face_image)
    # process image for saliency net
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = data_transforms['test'](image)

    # generate gaze field
    gaze_field = generate_data_field(eye_point=eye)
    sample = {'image': image,
              'face_image': face_image,
              'eye_position': torch.FloatTensor(eye),
              'gaze_field': torch.from_numpy(gaze_field)}

    return sample


def preprocess_image_dlib(image, eye, face):
    x_0, y_0 = face[0]
    x_1, y_1 = face[1]

    h, w = image.shape[:2]
    face_image = image[int(y_0):int(y_1), int(x_0):int(x_1), :]
    # process face_image for face net
    # face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    face_image = Image.fromarray(face_image)
    face_image = data_transforms['test'](face_image)
    # process image for saliency net
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = data_transforms['test'](image)

    # generate gaze field
    gaze_field = generate_data_field(eye_point=eye)
    sample = {'image': image,
              'face_image': face_image,
              'eye_position': torch.FloatTensor(eye),
              'gaze_field': torch.from_numpy(gaze_field)}

    return sample


def test(net, test_image_path, eye):
    net.eval()
    heatmaps = []

    data = preprocess_image(test_image_path, eye)

    image, face_image, gaze_field, eye_position = data['image'], data['face_image'], data['gaze_field'], data[
        'eye_position']
    image, face_image, gaze_field, eye_position = map(lambda x: Variable(x.unsqueeze(0).cuda(), volatile=True),
                                                      [image, face_image, gaze_field, eye_position])

    _, predict_heatmap = net([image, face_image, gaze_field, eye_position])

    final_output = predict_heatmap.cpu().data.numpy()

    heatmap = final_output.reshape([224 // 4, 224 // 4])

    h_index, w_index = np.unravel_index(heatmap.argmax(), heatmap.shape)
    f_point = np.array([w_index / 56., h_index / 56.])

    return heatmap, f_point[0], f_point[1]


def make_pred(net, img, eye, face):
    net.eval()
    heatmaps = []

    data = preprocess_image_dlib(img, eye, face)

    image, face_image, gaze_field, eye_position = data['image'], data['face_image'], data['gaze_field'], data[
        'eye_position']
    image, face_image, gaze_field, eye_position = map(lambda x: Variable(x.unsqueeze(0).cuda(), volatile=True),
                                                      [image, face_image, gaze_field, eye_position])

    _, predict_heatmap = net([image, face_image, gaze_field, eye_position])

    final_output = predict_heatmap.cpu().data.numpy()

    heatmap = final_output.reshape([224 // 4, 224 // 4])

    h_index, w_index = np.unravel_index(heatmap.argmax(), heatmap.shape)
    f_point = np.array([w_index / 56., h_index / 56.])

    return heatmap, f_point[0], f_point[1]


def draw_result(im, eye, heatmap, gaze_point):
    x1, y1 = eye
    x2, y2 = gaze_point
    # im = cv2.imread(image_path)
    image_height, image_width = im.shape[:2]
    x1, y1 = image_width * x1, y1 * image_height
    x2, y2 = image_width * x2, y2 * image_height
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
    cv2.circle(im, (x1, y1), 5, [255, 255, 255], -1)
    cv2.circle(im, (x2, y2), 5, [255, 255, 255], -1)
    cv2.line(im, (x1, y1), (x2, y2), [255, 0, 0], 3)

    # heatmap visualization
    heatmap = ((heatmap - heatmap.min()) / (heatmap.max() - heatmap.min()) * 255).astype(np.uint8)
    heatmap = np.stack([heatmap, heatmap, heatmap], axis=2)
    heatmap = cv2.resize(heatmap, (image_width, image_height))

    heatmap = (0.8 * heatmap.astype(np.float32) + 0.2 * im.astype(np.float32)).astype(np.uint8)
    img = np.concatenate((im, heatmap), axis=1)


    return img


def main():
    #
    #yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    net = GazeNet()
    net = DataParallel(net)
    net.cuda()

    pretrained_dict = torch.load('./pretrained_model.pkl')
    model_dict = net.state_dict()
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
    model_dict.update(pretrained_dict)
    net.load_state_dict(model_dict)


    cap = cv2.VideoCapture(0)
    #video_writer = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1280, 480))
    while 1:
        ret, img = cap.read()
        detected = detect_face(img)
        for i, d in enumerate(detected):
            points = get_face_rect_xy(d)
            print(points)
            left_eye, right_eye = get_eye_coordinates(img, d)
            left_eye = normalized_xy(img, left_eye)
            right_eye = normalized_xy(img, right_eye)
            mean_eye = tuple(map(operator.add, left_eye, right_eye))
            mean_eye = tuple(xy / 2 for xy in mean_eye)
            heatmap, p_x, p_y = make_pred(net, img, mean_eye, points)
            print(f'{p_x}, {p_y}')
            drawn_img = draw_result(img, mean_eye, heatmap, (p_x, p_y))
            #video_writer.write(drawn_img)
            #results = yolo_model(img)
            #print(results)
            #results.show()
            cv2.imshow('img', drawn_img)

        if len(detected) == 0:
            cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    #video_writer.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
