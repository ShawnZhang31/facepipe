from typing import Any, Union
import mediapipe as mp
import numpy as np
import cv2
from typing import Union
import math

class FrontFaceDetect(object):
    """mp face detection and face landmarks shape predictor class """
    def __init__(self, max_face_num:Union[int, None] = None, min_detection_confidence:float =0.5) -> None:
        super().__init__()
        self.face_detector = mp.solutions.face_detection
        self.face_predictor = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.max_face_num = max_face_num
        self.min_detection_confidence = min_detection_confidence
    
    def detectFace(self, image:np.array, max_face_num:Union[int, None] = None):
        faces=[]

        if max_face_num is None:
            max_face_num = self.max_face_num
        
        with self.face_detector.FaceDetection(min_detection_confidence=self.min_detection_confidence) as face_detection:
            # 将图像由OpenCV的BGR格式转换为RGB格式
            image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = face_detection.process(image_RGB)
            # 提取人脸信息
            if not results.detections:
                print("no face detected")
            else:
                detections = results.detections
                face_info = dict()
                img_height = image.shape[0]
                img_width = image.shape[1]
                for idx in range(min(len(detections), max_face_num) if max_face_num is not None else len(detections)):
                    detection = detections[idx]
                    # self.mp_drawing.draw_detection(image, detection)
                    location_data = detection.location_data
                    bbox = {
                        "xmin": int(location_data.relative_bounding_box.xmin * img_width),
                        "ymin": int(location_data.relative_bounding_box.ymin * img_height),
                        "width": int(location_data.relative_bounding_box.width * img_width),
                        "height": int(location_data.relative_bounding_box.height * img_height),
                    }
                    # cv2.rectangle(image, 
                    #             (bbox['xmin'], bbox['ymin']),
                    #             (bbox['xmin']+bbox['width'],bbox['ymin']+bbox['height']),
                    #             (255, 255, 0),
                    #             3)
                    keypoints = []
                    for keypoint in location_data.relative_keypoints:
                        point = (int(keypoint.x * img_width), int(keypoint.y * img_height))
                        # cv2.circle(image, point, 2, (255, 255, 0), 1)
                        keypoints.append(point)
                    face_info['bbox'] = bbox
                    face_info['keypoints'] = keypoints
                    faces.append(face_info)
        # cv2.imwrite("./docs/face_detect_d.jpg", image)
        return faces

    def detectFaceLandmarks(self, image, max_num_faces:Union[int, None] = None):
        
        landmarks = []

        if max_num_faces is None:
            max_num_faces = self.max_face_num
        
        with self.face_predictor.FaceMesh(static_image_mode=True, max_num_faces=20 if max_num_faces is None else max_num_faces, min_detection_confidence=self.min_detection_confidence) as face_mesh:
            # 将图像由OpenCV的BGR格式转换为RGB格式
            image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image_RGB)
            if not results.multi_face_landmarks:
                pass
            else:
                multi_face_landmarks = results.multi_face_landmarks
                img_height, img_width = image.shape[0], image.shape[1]
                for shape in multi_face_landmarks:
                    face_shape = []
                    for landmark in shape.landmark:
                        point = self.__mediapipe_landmarks_to_image_cordation(landmark, img_height, img_width)
                        face_shape.append(point)
                        cv2.circle(image, point, 2, (255, 0, 255), -1)
                    landmarks.append(face_shape)
        # cv2.imwrite("./docs/face_landmarks_d.jpg", image)
        return landmarks
    
    def __mediapipe_landmarks_to_image_cordation(self, landmark, img_height, img_width):
        point = (int(landmark.x * img_width), int(landmark.y * img_height))
        return point


if __name__ == "__main__":
    image = cv2.imread("./test_imgs/one_face.jpeg", cv2.IMREAD_COLOR)
    # image = cv2.imread("./docs/faces.jpeg", cv2.IMREAD_COLOR)

    faceDetectTool = FrontFaceDetect(min_detection_confidence=0.5)
    # faces = faceDetectTool.detectFace(image)

    # print(faces)

    # landmarks = faceDetectTool.detectFaceLandmarks(image)
    # print(landmarks)

    cv2.imshow("image", image)
    cv2.waitKey()
