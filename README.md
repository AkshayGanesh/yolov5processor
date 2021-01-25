# Yolo v5 Inference Engine
Basically a wrapper for the detection program for ease of use.

## How to install:
pip install yolov5processor

## How to use:
```python
from yolov5processor.infer import ExecuteInference 

model = ExecuteInference(weight="path-to-weight.pt", confidence=0.4, \
            img_size=640, agnostic_nms=False, gpu=False, iou=0.5)

image = cv2.imread("imagepath.jpg")
pred = model.predict(image)
```
## Analyse the Output:

```python
print(pred)

{
  "points": [100, 120, 400, 500],
  "conf": 0.7,
  "class": "apple"
}
```
points key represnts the bounding box coordinates in the order x1, y1, x2, y2 respectively.
conf key represents the confidence.
class key represents the object class.
