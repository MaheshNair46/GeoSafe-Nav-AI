import math
import pyttsx3

class GeoSafeAssistant:
    """
    AI-driven navigation assistant that calculates safe cornering speeds 
    based on road geometry and environmental friction.
    """
    def __init__(self, weather="dry"):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        
        # Friction coefficients (mu): dry=0.7, wet=0.4, icy=0.1
        weather_map = {"dry": 0.7, "wet": 0.4, "icy": 0.1}
        self.mu = weather_map.get(weather.lower(), 0.7)
        self.g = 9.81

    def _get_distance(self, p1, p2):
        """Haversine formula for spherical distance between GPS coordinates."""
        R = 6371000
        lat1, lon1 = map(math.radians, p1)
        lat2, lon2 = map(math.radians, p2)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

    def analyze_and_alert(self, points, current_speed_kmh):
        """Calculates critical velocity for a curve defined by three points."""
        p1, p2, p3 = points
        a = self._get_distance(p1, p2)
        b = self._get_distance(p2, p3)
        c = self._get_distance(p3, p1)
        
        # Calculate circumradius using Heron's area formula
        s = (a + b + c) / 2
        area_val = s * (s - a) * (s - b) * (s - c)
        
        if area_val <= 0: return 

        radius = (a * b * c) / (4 * math.sqrt(area_val))
        
        # Critical Velocity Formula: v = sqrt(mu * g * r)
        safe_v_kmh = int(math.sqrt(self.mu * self.g * radius) * 3.6)

        print(f"[System Log] Curve Radius: {radius:.1f}m | Threshold: {safe_v_kmh}km/h")

        if current_speed_kmh > safe_v_kmh:
            msg = f"Caution. Sharp curve ahead. Reduce speed to {safe_v_kmh} kilometers per hour."
            self.engine.say(msg)
            self.engine.runAndWait()

if __name__ == "__main__":
    # Test Case: Sharp curve in wet conditions
    sharp_turn = [(12.9716, 77.5946), (12.9717, 77.5947), (12.9718, 77.5946)]
    ai = GeoSafeAssistant(weather="wet")
    ai.analyze_and_alert(sharp_turn, current_speed_kmh=60)