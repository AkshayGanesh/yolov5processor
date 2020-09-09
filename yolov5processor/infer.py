import torch
import numpy as np
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
        self.model, self.names, self.colors = self.load_model()
        print("Loaded Models...")

    def inference_device(self):
        device = select_device('cpu')
        if self.gpu:
            device = select_device(str(torch.cuda.current_device()))
        half = device.type != 'cpu'
        return device, half

    def load_model(self):
        model = attempt_load(self.weight, map_location=self.device)
        imgsz = check_img_size(self.img_size, s=model.stride.max())
        if self.half:
            model.half()
        names = model.module.names if hasattr(model, 'module') else model.names
        print("classes: {}".format(names))
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
        img = torch.zeros((1, 3, imgsz, imgsz), device=self.device)
        _ = model(img.half() if self.half else img) if self.device.type != 'cpu' else None
        return model, names, colors

    def predict(self, image):
        img = letterbox(image, new_shape=self.img_size)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = self.model(img, augment=False)[0]
        pred = non_max_suppression(pred, self.confidence, self.iou, classes=None, agnostic=self.agnostic_nms)
        _output = list()
        for i, det in enumerate(pred):
            if det is not None and len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    _output.append({"points": xyxy, "conf": conf, "class": cls})
        return _output
