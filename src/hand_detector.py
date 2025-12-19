import cv2
from ultralytics import YOLO
import numpy as np


class HandDetector:
    """
    Hand detector using YOLO model.
    Handles model loading, detection, and result processing.
    """
    
    def __init__(self, model_path, conf_threshold=0.5):
        """
        Initialize hand detector.
        
        Args:
            model_path: Path to trained YOLO model (.pt file)
            conf_threshold: Minimum confidence threshold for detections
        """
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load YOLO model from file."""
        try:
            print(f"📦 Loading YOLO model from: {self.model_path}")
            self.model = YOLO(self.model_path)
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def detect(self, frame):
        """
        Detect hands in frame.
        
        Args:
            frame: OpenCV frame (numpy array)
        
        Returns:
            List of detections, each containing:
            - bbox: (x1, y1, x2, y2)
            - conf: confidence score
            - cls: class id
            - label: class name
        """
        if self.model is None:
            return []
        
        try:
            # Run inference
            results = self.model(frame, conf=self.conf_threshold, verbose=False)
            
            detections = []
            
            if len(results) > 0:
                result = results[0]
                
                # Extract boxes
                if result.boxes is not None and len(result.boxes) > 0:
                    boxes = result.boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
                    confs = result.boxes.conf.cpu().numpy()
                    classes = result.boxes.cls.cpu().numpy()
                    
                    for box, conf, cls in zip(boxes, confs, classes):
                        detection = {
                            'bbox': tuple(box.astype(int)),
                            'conf': float(conf),
                            'cls': int(cls),
                            'label': self.model.names[int(cls)]
                        }
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"⚠️  Detection error: {e}")
            return []
    
    def detect_and_annotate(self, frame):
        """
        Detect hands and return annotated frame using YOLO's built-in plotting.
        
        Args:
            frame: OpenCV frame
        
        Returns:
            Tuple (annotated_frame, detections)
        """
        try:
            results = self.model(frame, conf=self.conf_threshold, verbose=False)
            
            # Get annotated frame
            annotated_frame = results[0].plot()
            
            # Extract detections
            detections = []
            if len(results) > 0:
                result = results[0]
                if result.boxes is not None and len(result.boxes) > 0:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    confs = result.boxes.conf.cpu().numpy()
                    classes = result.boxes.cls.cpu().numpy()
                    
                    for box, conf, cls in zip(boxes, confs, classes):
                        detection = {
                            'bbox': tuple(box.astype(int)),
                            'conf': float(conf),
                            'cls': int(cls),
                            'label': self.model.names[int(cls)]
                        }
                        detections.append(detection)
            
            return annotated_frame, detections
            
        except Exception as e:
            print(f"⚠️  Detection error: {e}")
            return frame, []
    
    def get_model_info(self):
        """Get information about the loaded model."""
        if self.model is None:
            return None
        
        return {
            'model_path': self.model_path,
            'class_names': self.model.names,
            'num_classes': len(self.model.names),
            'conf_threshold': self.conf_threshold
        }
