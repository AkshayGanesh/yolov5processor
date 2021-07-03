import cv2
from yolov5processor.infer import ExecuteInference

model = ExecuteInference(weight="/home/akshay/yolov5/wt.pt",
                         confidence=0.4, img_size=640, agnostic_nms=False, gpu=False, iou=0.5)
cap = cv2.VideoCapture("/home/akshay/demo_video.mp4")

ret = True
while ret:
    ret, image = cap.read()
    pred = model.predict(image)
    print(pred)
cap.release()
