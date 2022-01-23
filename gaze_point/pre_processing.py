import dlib
from imutils import face_utils

predictorPath = "shape_predictor_68_face_landmarks_GTX.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictorPath)

def detect_face(img):
    return detector(img)


def get_face_rect_xy(detected_face):
    x1, y1, x2, y2, w, h = detected_face.left(), detected_face.top(), detected_face.right() + 1, detected_face.bottom() + 1, detected_face.width(), detected_face.height()
    return [(x1, y1), (x2, y2)]


def get_eye_coordinates(img, detected_face):
    shape = predictor(img, detected_face)
    shape = face_utils.shape_to_np(shape)

    left_eye = shape[36:42].mean(axis=0)
    right_eye = shape[42:48].mean(axis=0)
    return left_eye, right_eye


def normalized_xy(img, pixel_loc):
    x, y = pixel_loc
    h, w, _ = img.shape
    return x / w, y / h
