import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyBBoxSmoother:
    """
    Smooths bounding box coordinates using fuzzy logic to reduce jitter.
    
    The fuzzy system uses:
    - Input 1: Motion magnitude (pixels)
    - Input 2: YOLO confidence (0-1)
    - Output: Smoothing factor alpha (0-1)
    """
    
    def __init__(self):
        """Initialize fuzzy logic system with membership functions and rules."""
        # Define input/output universes
        self.motion = ctrl.Antecedent(np.arange(0, 101, 1), 'motion')
        self.confidence = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'confidence')
        self.alpha = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'alpha')
        
        # Define membership functions for MOTION
        self.motion['small'] = fuzz.trapmf(self.motion.universe, [0, 0, 3, 8])
        self.motion['medium'] = fuzz.trapmf(self.motion.universe, [5, 12, 18, 25])
        self.motion['large'] = fuzz.trapmf(self.motion.universe, [20, 40, 100, 100])
        
        # Define membership functions for CONFIDENCE
        self.confidence['low'] = fuzz.trapmf(self.confidence.universe, [0, 0, 0.3, 0.5])
        self.confidence['medium'] = fuzz.trapmf(self.confidence.universe, [0.4, 0.5, 0.6, 0.7])
        self.confidence['high'] = fuzz.trapmf(self.confidence.universe, [0.6, 0.75, 1.0, 1.0])
        
        # Define membership functions for ALPHA (output)
        self.alpha['very_small'] = fuzz.trimf(self.alpha.universe, [0, 0.05, 0.15])
        self.alpha['small'] = fuzz.trimf(self.alpha.universe, [0.1, 0.2, 0.3])
        self.alpha['medium'] = fuzz.trimf(self.alpha.universe, [0.25, 0.4, 0.55])
        self.alpha['large'] = fuzz.trimf(self.alpha.universe, [0.5, 0.7, 0.85])
        self.alpha['very_large'] = fuzz.trimf(self.alpha.universe, [0.8, 0.95, 1.0])
        
        # Define fuzzy rules
        self.rules = [
            # If motion is small and confidence is high, minimal smoothing needed
            ctrl.Rule(self.motion['small'] & self.confidence['high'], self.alpha['very_small']),
            ctrl.Rule(self.motion['small'] & self.confidence['medium'], self.alpha['small']),
            ctrl.Rule(self.motion['small'] & self.confidence['low'], self.alpha['small']),
            
            # If motion is medium, moderate smoothing
            ctrl.Rule(self.motion['medium'] & self.confidence['high'], self.alpha['medium']),
            ctrl.Rule(self.motion['medium'] & self.confidence['medium'], self.alpha['small']),
            ctrl.Rule(self.motion['medium'] & self.confidence['low'], self.alpha['very_small']),
            
            # If motion is large and confidence is high, follow it
            ctrl.Rule(self.motion['large'] & self.confidence['high'], self.alpha['very_large']),
            ctrl.Rule(self.motion['large'] & self.confidence['medium'], self.alpha['large']),
            ctrl.Rule(self.motion['large'] & self.confidence['low'], self.alpha['medium']),
        ]
        
        # Create control system
        self.smoothing_ctrl = ctrl.ControlSystem(self.rules)
        self.smoother = ctrl.ControlSystemSimulation(self.smoothing_ctrl)
        
        # State variables
        self.prev_cx = None
        self.prev_cy = None
        self.prev_w = None
        self.prev_h = None
    
    def reset(self):
        """Reset the smoother state."""
        self.prev_cx = None
        self.prev_cy = None
        self.prev_w = None
        self.prev_h = None
    
    def smooth(self, bbox, conf):
        """
        Apply fuzzy smoothing to a bounding box.
        
        Args:
            bbox: Tuple (x1, y1, x2, y2) - bounding box coordinates
            conf: Float - YOLO confidence score (0-1)
        
        Returns:
            Tuple (x1, y1, x2, y2) - smoothed bounding box coordinates
        """
        x1, y1, x2, y2 = bbox
        
        # Calculate current center and size
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        w = x2 - x1
        h = y2 - y1
        
        # If first detection, initialize state
        if self.prev_cx is None:
            self.prev_cx = cx
            self.prev_cy = cy
            self.prev_w = w
            self.prev_h = h
            return bbox
        
        # Calculate motion magnitude
        dx = cx - self.prev_cx
        dy = cy - self.prev_cy
        motion_magnitude = np.sqrt(dx**2 + dy**2)
        
        # Clip values to valid ranges
        motion_magnitude = np.clip(motion_magnitude, 0, 100)
        conf = np.clip(conf, 0, 1)
        
        # Fuzzy inference
        try:
            self.smoother.input['motion'] = motion_magnitude
            self.smoother.input['confidence'] = conf
            self.smoother.compute()
            alpha = self.smoother.output['alpha']
        except:
            # Fallback to medium smoothing if fuzzy inference fails
            alpha = 0.3
        
        # Apply smoothing to center
        cx_smooth = self.prev_cx + alpha * (cx - self.prev_cx)
        cy_smooth = self.prev_cy + alpha * (cy - self.prev_cy)
        
        # Apply smoothing to size (less aggressive)
        w_smooth = self.prev_w + 0.5 * (w - self.prev_w)
        h_smooth = self.prev_h + 0.5 * (h - self.prev_h)
        
        # Update state
        self.prev_cx = cx_smooth
        self.prev_cy = cy_smooth
        self.prev_w = w_smooth
        self.prev_h = h_smooth
        
        # Convert back to x1, y1, x2, y2
        x1_smooth = int(cx_smooth - w_smooth / 2)
        y1_smooth = int(cy_smooth - h_smooth / 2)
        x2_smooth = int(cx_smooth + w_smooth / 2)
        y2_smooth = int(cy_smooth + h_smooth / 2)
        
        return (x1_smooth, y1_smooth, x2_smooth, y2_smooth)
    
    def get_debug_info(self):
        """Return debug information about the smoother state."""
        return {
            'prev_cx': self.prev_cx,
            'prev_cy': self.prev_cy,
            'prev_w': self.prev_w,
            'prev_h': self.prev_h
        }
