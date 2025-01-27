import cv2
from vehicle_detector import VehicleDetector

vd = VehicleDetector()

img = cv2.imread("Fri_11-01_22-09.jpg")

threshold = 0.1
vehicle_boxes, confidences = vd.detect_vehicles(img)

vehicle_boxes = [box for box, conf in zip(vehicle_boxes, confidences) if conf >= threshold]  # Added filtering

for box in vehicle_boxes:
    x, y, w, h = box
    cv2.rectangle(img, (x, y), (x+w, y+h), (25, 0, 180), 3)
print(len(vehicle_boxes))

# cv2.imwrite("boxed_Fri_11-01_22-09.jpg", img)
cv2.imshow('causeway', img)
cv2.waitKey(0)

