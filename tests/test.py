import cv2
from yolov5processor.infer import ExecuteInference

cap = cv2.VideoCapture("cement_bag_detection.avi")
yp = ExecuteInference(weight="last_cement.pt", gpu=False)
yp.__init__(weight="last_cement.pt", gpu=False)
ret = True
while ret:
    ret, frame = cap.read()
    print(yp.predict(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
