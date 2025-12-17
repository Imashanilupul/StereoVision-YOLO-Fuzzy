"""
Configuration for Hand Detection System
"""

import os

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model configuration
MODEL_CONFIG = {
    # Path to trained YOLO model
    'model_path': os.path.join(PROJECT_ROOT, 'models', 'Yolo', 'best.pt'),
    
    # Alternative: use a default model if custom model not found
    'fallback_model': 'yolov8n.pt',
    
    # Detection confidence threshold
    'conf_threshold': 0.5,
}

# Camera configuration
CAMERA_CONFIG = {
    # Camera index (0 for default webcam, 1 for external)
    'camera_index': 0,
    
    # Frame dimensions
    'frame_width': 640,
    'frame_height': 480,
    
    # FPS limit
    'fps': 30,
}

# Fuzzy smoothing configuration
FUZZY_CONFIG = {
    # Enable/disable fuzzy smoothing
    'enabled': True,
    
    # Minimum detections before starting smoothing
    'min_detections': 3,
}

# Display configuration
DISPLAY_CONFIG = {
    # Window title
    'window_title': 'Hand Detection - YOLO + Fuzzy Smoothing',
    
    # Show FPS counter
    'show_fps': True,
    
    # Show confidence scores
    'show_confidence': True,
    
    # Show smoothing info
    'show_smoothing_info': True,
    
    # Colors (BGR format)
    'color_raw': (0, 0, 255),      # Red for raw detection
    'color_smooth': (0, 255, 0),   # Green for smoothed detection
    'color_text': (255, 255, 255), # White for text
    'color_bg': (0, 0, 0),         # Black for background
}

# Keyboard shortcuts
CONTROLS = {
    'quit': 'q',
    'toggle_smoothing': 's',
    'reset_smoothing': 'r',
    'toggle_raw_boxes': 't',
    'help': 'h',
}

def get_model_path():
    """Get the model path, checking if it exists."""
    model_path = MODEL_CONFIG['model_path']
    
    if os.path.exists(model_path):
        return model_path
    else:
        print(f"⚠️  Custom model not found at: {model_path}")
        print(f"📦 Using fallback model: {MODEL_CONFIG['fallback_model']}")
        return MODEL_CONFIG['fallback_model']
