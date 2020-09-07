import cv2
from yolov5processor.infer import ExecuteInference
cap = cv2.VideoCapture("/home/administrator/akshay/yolov5processor/tests/cement_bag_detection.avi")
yp = ExecuteInference(weight="/home/administrator/akshay/yolov5processor/tests/last_cement.pt", gpu=True)
ret = True
while ret:
    ret, frame = cap.read()
    print(yp.predict(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
