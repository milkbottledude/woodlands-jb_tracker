from ultralytics import YOLO

# building new model
model = YOLO('yolov8n.yaml')
# training model with own data
results = model.train(data='config.yaml', epochs=40)