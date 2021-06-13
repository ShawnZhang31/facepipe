import time
from locust import HttpUser, task, between
from image_base64 import img_base64

class QuickstartUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def hello_api(self):
        self.client.get("/api/v1/")

    @task(3)
    def face_bbox_detect(self):
        self.client.post("/api/v1/face/detect", json={"image":img_base64})
    
    @task(3)
    def face_landmark_detect(self):
        self.client.post("/api/v1/face/landmark", json={"image":img_base64})
