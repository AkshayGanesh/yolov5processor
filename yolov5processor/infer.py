import torch
from numpy import random

from yolov5processor.models.experimental import attempt_load
from yolov5processor.utils.datasets import letterbox
from yolov5processor.utils.general import (check_img_size, non_max_suppression, scale_coords)
from yolov5processor.utils.torch_utils import select_device


class ExecuteInference:
    def __init__(self, weight, confidence=0.4, img_size=640, agnostic_nms=False, gpu=False, iou=0.5):
        self.weight = weight
        self.confidence = confidence
        self.gpu = gpu
        self.iou = iou
        self.agnostic_nms = agnostic_nms
        self.img_size = img_size
        self.device, self.half = self.inference_device()
        self.names = None
        self.colors = None

    def inference_device(self):
        device = select_device('cpu')
        if self.gpu:
            device = select_device('0')
        half = device.type != 'cpu'
        return device, half

    def load_model(self):
        self.model = attempt_load(self.weight, map_location=self.device)
        self.imgsz = check_img_size(self.img_size, s=self.model.stride.max())
        if self.half:
            self.model.half()
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.names))]
        img = torch.zeros((1, 3, self.imgsz, self.imgsz), device=self.device)
        _ = self.model(img.half() if self.half else img) if self.device.type != 'cpu' else None

    def predict(self, image):
        img = letterbox(image, new_shape=self.img_size)[0]
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = self.model(img, augment=False)[0]
        pred = non_max_suppression(pred, self.confidence, self.iou, classes=None, agnostic=self.agnostic_nms)
        _output = list()
        for i, det in enumerate(pred):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img.shape).round()
            _output.append(det)
        return _output