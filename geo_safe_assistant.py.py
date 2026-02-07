import math
import pyttsx3

class GeoSafeAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        self.mu = 0.7  # Static friction coefficient
        self.g = 9.81

    def _get_distance(self, p1, p2):
        R = 6371000
        lat1, lon1 = map(math.radians, p1)
        lat2, lon2 = map(math.radians, p2)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

    def _calculate_radius(self, p1, p2, p3):
        """Calculates the radius of curvature for a 3-point segment."""
        a = self._get_distance(p1, p2)
        b = self._get_distance(p2, p3)
        c = self._get_distance(p3, p1)
        s = (a + b + c) / 2
        area_val = s * (s - a) * (s - b) * (s - c)
        if area_val <= 0: return float('inf')
        return (a * b * c) / (4 * math.sqrt(area_val))

    def analyze_path(self, path, current_speed_kmh):
        """
        Scans a list of coordinates to find the sharpest turn (minimum radius).
        This handles S-curves and tightening turns.
        """
        min_radius = float('inf')

        # Sliding window of 3 points to scan the whole path
        for i in range(len(path) - 2):
            segment_radius = self._calculate_radius(path[i], path[i+1], path[i+2])
            if segment_radius < min_radius:
                min_radius = segment_radius

        if min_radius == float('inf'):
            print("Path is straight.")
            return

        # Physics: Critical Velocity
        safe_v_kmh = int(math.sqrt(self.mu * self.g * min_radius) * 3.6)

        print(f"[System Log] Path Scan Complete. Sharpest Radius: {min_radius:.1f}m")
        print(f"[System Log] Recommended Speed: {safe_v_kmh}km/h")

        if current_speed_kmh > safe_v_kmh:
            msg = f"Complex turns ahead. The sharpest point requires {safe_v_kmh} kilometers per hour."
            self.engine.say(msg)
            self.engine.runAndWait()

# --- Testing a Complex Path ---
if __name__ == "__main__":
    # A series of coordinates representing an S-Curve or tightening turn
    complex_path = [
        (12.9710, 77.5940),
        (12.9712, 77.5942),
        (12.9713, 77.5945), # The turn starts
        (12.9714, 77.5946), # It gets sharper (Apex)
        (12.9713, 77.5948), # Reversing (S-Curve)
        (12.9711, 77.5950)
    ]
    
    ai = GeoSafeAssistant()
    ai.analyze_path(complex_path, current_speed_kmh=65)
