import cv2
import sys
import time
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from hand_detector import HandDetector
from fuzzy_bbox_smoother import FuzzyBBoxSmoother
from config import get_model_path, MODEL_CONFIG, CAMERA_CONFIG


class ComparisonDemo:
    """Show raw vs smoothed detection side-by-side."""
    
    def __init__(self):
        print("=" * 60)
        print("🔬 Raw vs Fuzzy Smoothed - Side-by-Side Comparison")
        print("=" * 60)
        
        # Initialize
        model_path = get_model_path()
        self.detector = HandDetector(model_path, MODEL_CONFIG['conf_threshold'])
        self.smoother = FuzzyBBoxSmoother()
        
        # Camera
        self.cap = cv2.VideoCapture(CAMERA_CONFIG['camera_index'])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['frame_width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['frame_height'])
        
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        
        print("✅ System ready!")
        print("\nPress 'q' to quit, 'r' to reset smoother\n")
        
        self.fps = 0
        self.prev_time = time.time()
    
    def draw_bbox(self, frame, bbox, color, label, conf=None):
        """Draw bounding box."""
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        text = f"{label} {conf:.2f}" if conf else label
        cv2.putText(frame, text, (x1, y1 - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    def add_title(self, frame, title, color):
        """Add title to frame."""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 40), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv2.putText(frame, title, (10, 28),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    
    def run(self):
        """Run comparison demo."""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Calculate FPS
            current_time = time.time()
            self.fps = 1 / (current_time - self.prev_time)
            self.prev_time = current_time
            
            # Detect
            detections = self.detector.detect(frame)
            
            # Create two copies
            frame_raw = frame.copy()
            frame_smooth = frame.copy()
            
            # Draw on both
            for det in detections:
                bbox = det['bbox']
                conf = det['conf']
                label = det['label']
                
                # Raw (left side)
                self.draw_bbox(frame_raw, bbox, (0, 0, 255), label, conf)
                
                # Smoothed (right side)
                smooth_bbox = self.smoother.smooth(bbox, conf)
                self.draw_bbox(frame_smooth, smooth_bbox, (0, 255, 0), label, conf)
            
            # Add titles
            self.add_title(frame_raw, "RAW YOLO (Jittery)", (0, 0, 255))
            self.add_title(frame_smooth, "FUZZY SMOOTHED (Stable)", (0, 255, 0))
            
            # Combine side-by-side
            combined = cv2.hconcat([frame_raw, frame_smooth])
            
            # Add FPS info
            cv2.putText(combined, f"FPS: {self.fps:.1f}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show
            cv2.imshow("Comparison: Raw vs Fuzzy Smoothed", combined)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.smoother.reset()
                print("🔄 Smoother reset")
        
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        demo = ComparisonDemo()
        demo.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
