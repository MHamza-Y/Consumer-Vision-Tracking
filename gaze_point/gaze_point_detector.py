import torch
from torch.autograd import Variable
from torch.nn import DataParallel
from gazenet import GazeNet
import numpy as np
import cv2
from PIL import Image
from torchvision import transforms
import operator

from pre_processing import detect_face, get_face_rect_xy, get_eye_coordinates, normalized_xy

data_transforms = {
    'train': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'test': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
}


class GazePointDetector:

    def __init__(self, pretrained_dict_path='./pretrained_model.pkl'):
        print('Initializing GazeNet')
        self.net = GazeNet()
        self.net = DataParallel(self.net)
        self.net.cuda()
        print('Loading Dict')
        pretrained_dict = torch.load(pretrained_dict_path)
        model_dict = self.net.state_dict()
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
        model_dict.update(pretrained_dict)
        self.net.load_state_dict(model_dict)
        print('Dict Loaded')
        print('Model Initialization Complete')

    def generate_data_field(self, eye_point):
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

    def preprocess_image_dlib(self, image, eye, face):
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
        gaze_field = self.generate_data_field(eye_point=eye)
        sample = {'image': image,
                  'face_image': face_image,
                  'eye_position': torch.FloatTensor(eye),
                  'gaze_field': torch.from_numpy(gaze_field)}

        return sample

    def make_pred(self, net, img, eye, face):
        net.eval()
        heatmaps = []

        data = self.preprocess_image_dlib(img, eye, face)

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

    def get_gaze_points(self, img):
        detected = detect_face(img)
        gazed_points = []
        for i, d in enumerate(detected):
            points = get_face_rect_xy(d)
            left_eye, right_eye = get_eye_coordinates(img, d)
            left_eye = normalized_xy(img, left_eye)
            right_eye = normalized_xy(img, right_eye)
            mean_eye = tuple(map(operator.add, left_eye, right_eye))
            mean_eye = tuple(xy / 2 for xy in mean_eye)
            heatmap, p_x, p_y = self.make_pred(self.net, img, mean_eye, points)
            p_x, p_y = self.normalized_xy_to_standard(img, p_x, p_y)
            gazed_points.append({'x': p_x, 'y': p_y})

        return gazed_points

    def normalized_xy_to_standard(self, img, x, y):
        h, w, _ = img.shape
        return x * w, y * h
