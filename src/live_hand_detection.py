"""
Live Hand Detection with YOLO and Fuzzy Logic Smoothing
Real-time hand detection using camera with adaptive boundary box smoothing.
"""

import cv2
import sys
import time
import numpy as np
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from hand_detector import HandDetector
from fuzzy_bbox_smoother import FuzzyBBoxSmoother
from config import (
    get_model_path, 
    CAMERA_CONFIG, 
    FUZZY_CONFIG, 
    DISPLAY_CONFIG, 
    CONTROLS,
    MODEL_CONFIG
)


class LiveHandDetection:
    """
    Live hand detection system with fuzzy smoothing.
    """
    
    def __init__(self):
        """Initialize the detection system."""
        print("=" * 60)
        print("🤚 Live Hand Detection System")
        print("=" * 60)
        
        # Initialize detector
        model_path = get_model_path()
        self.detector = HandDetector(model_path, MODEL_CONFIG['conf_threshold'])
        
        # Initialize fuzzy smoother
        self.smoother = FuzzyBBoxSmoother()
        
        # Initialize camera
        self.cap = self._init_camera()
        
        # State
        self.smoothing_enabled = FUZZY_CONFIG['enabled']
        self.show_raw_boxes = True
        self.frame_count = 0
        self.fps = 0
        
        # FPS calculation
        self.prev_time = time.time()
        self.fps_buffer = []
        
        print("\n✅ System initialized successfully!")
        self._print_controls()
    
    def _init_camera(self):
        """Initialize camera with configuration."""
        print(f"\n📷 Opening camera {CAMERA_CONFIG['camera_index']}...")
        
        cap = cv2.VideoCapture(CAMERA_CONFIG['camera_index'])
        
        if not cap.isOpened():
            print("❌ Cannot open camera!")
            raise RuntimeError("Camera initialization failed")
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['frame_width'])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['frame_height'])
        cap.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
        
        # Get actual properties
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"✅ Camera opened: {actual_width}x{actual_height}")
        
        return cap
    
    def _print_controls(self):
        """Print keyboard controls."""
        print("\n⌨️  Controls:")
        print(f"  '{CONTROLS['quit']}' - Quit")
        print(f"  '{CONTROLS['toggle_smoothing']}' - Toggle smoothing")
        print(f"  '{CONTROLS['reset_smoothing']}' - Reset smoother")
        print(f"  '{CONTROLS['toggle_raw_boxes']}' - Toggle raw boxes")
        print(f"  '{CONTROLS['help']}' - Show help")
        print()
    
    def _calculate_fps(self):
        """Calculate FPS."""
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        
        # Moving average
        self.fps_buffer.append(fps)
        if len(self.fps_buffer) > 30:
            self.fps_buffer.pop(0)
        
        self.fps = sum(self.fps_buffer) / len(self.fps_buffer)
    
    def _draw_bbox(self, frame, bbox, color, label, conf=None, thickness=2):
        """Draw bounding box with label."""
        x1, y1, x2, y2 = bbox
        
        # Draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
        
        # Prepare label text
        if conf is not None:
            text = f"{label} {conf:.2f}"
        else:
            text = label
        
        # Draw label background
        (text_width, text_height), baseline = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        )
        cv2.rectangle(
            frame, 
            (x1, y1 - text_height - baseline - 5),
            (x1 + text_width + 5, y1),
            color,
            -1
        )
        
        # Draw label text
        cv2.putText(
            frame, text,
            (x1 + 2, y1 - baseline - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )
    
    def _draw_info_panel(self, frame):
        """Draw information panel on frame."""
        h, w = frame.shape[:2]
        
        # Info lines
        info_lines = []
        
        if DISPLAY_CONFIG['show_fps']:
            info_lines.append(f"FPS: {self.fps:.1f}")
        
        info_lines.append(f"Smoothing: {'ON' if self.smoothing_enabled else 'OFF'}")
        info_lines.append(f"Frame: {self.frame_count}")
        
        # Draw semi-transparent background
        overlay = frame.copy()
        panel_height = len(info_lines) * 25 + 20
        cv2.rectangle(overlay, (10, 10), (250, 10 + panel_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Draw info lines
        y_offset = 30
        for line in info_lines:
            cv2.putText(
                frame, line,
                (20, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                DISPLAY_CONFIG['color_text'],
                1,
                cv2.LINE_AA
            )
            y_offset += 25
    
    def _draw_help(self, frame):
        """Draw help overlay."""
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Help text
        help_text = [
            "KEYBOARD CONTROLS",
            "",
            f"'{CONTROLS['quit']}' - Quit application",
            f"'{CONTROLS['toggle_smoothing']}' - Toggle fuzzy smoothing",
            f"'{CONTROLS['reset_smoothing']}' - Reset smoother state",
            f"'{CONTROLS['toggle_raw_boxes']}' - Show/hide raw boxes",
            f"'{CONTROLS['help']}' - Close this help",
            "",
            "Press any key to continue..."
        ]
        
        y_offset = h // 2 - len(help_text) * 15
        for line in help_text:
            cv2.putText(
                frame, line,
                (w // 2 - 200, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )
            y_offset += 30
    
    def process_frame(self, frame):
        """Process a single frame."""
        # Detect hands
        detections = self.detector.detect(frame)
        
        # Draw detections
        for detection in detections:
            bbox = detection['bbox']
            conf = detection['conf']
            label = detection['label']
            
            # Draw raw detection (red, thinner)
            if self.show_raw_boxes:
                self._draw_bbox(
                    frame, bbox, 
                    DISPLAY_CONFIG['color_raw'], 
                    f"{label} (raw)",
                    conf if DISPLAY_CONFIG['show_confidence'] else None,
                    thickness=1
                )
            
            # Apply fuzzy smoothing if enabled
            if self.smoothing_enabled:
                smooth_bbox = self.smoother.smooth(bbox, conf)
                
                # Draw smoothed detection (green, thicker)
                self._draw_bbox(
                    frame, smooth_bbox,
                    DISPLAY_CONFIG['color_smooth'],
                    f"{label} (smooth)",
                    conf if DISPLAY_CONFIG['show_confidence'] else None,
                    thickness=2
                )
            else:
                # Reset smoother when disabled
                self.smoother.reset()
        
        # Draw info panel
        self._draw_info_panel(frame)
        
        return frame
    
    def run(self):
        """Run the detection loop."""
        print("🎬 Starting detection loop...")
        print("=" * 60)
        
        try:
            show_help = False
            
            while True:
                # Read frame
                ret, frame = self.cap.read()
                
                if not ret:
                    print("❌ Failed to read frame")
                    break
                
                self.frame_count += 1
                
                # Calculate FPS
                self._calculate_fps()
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Show help overlay if requested
                if show_help:
                    self._draw_help(processed_frame)
                
                # Display frame
                cv2.imshow(DISPLAY_CONFIG['window_title'], processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord(CONTROLS['quit']):
                    print("\n👋 Quitting...")
                    break
                
                elif key == ord(CONTROLS['toggle_smoothing']):
                    self.smoothing_enabled = not self.smoothing_enabled
                    print(f"🔧 Smoothing: {'ON' if self.smoothing_enabled else 'OFF'}")
                
                elif key == ord(CONTROLS['reset_smoothing']):
                    self.smoother.reset()
                    print("🔄 Smoother reset")
                
                elif key == ord(CONTROLS['toggle_raw_boxes']):
                    self.show_raw_boxes = not self.show_raw_boxes
                    print(f"🔧 Raw boxes: {'ON' if self.show_raw_boxes else 'OFF'}")
                
                elif key == ord(CONTROLS['help']):
                    show_help = not show_help
                
                elif show_help and key != 255:
                    show_help = False
        
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """Clean up resources."""
        print("\n🧹 Cleaning up...")
        self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Done!")


def main():
    """Main entry point."""
    try:
        app = LiveHandDetection()
        app.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
