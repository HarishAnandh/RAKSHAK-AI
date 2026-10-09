import httpx
from datetime import datetime
from typing import Dict, Any, List, Optional
import math

class LiveDisasterFeedTool:
    """
    LiveDisasterFeedTool
    Queries official live public disaster telemetry feeds:
    1. USGS Real-time Earthquake API (Global & Regional Seismic Grid)
    2. GDACS (Global Disaster Alert and Coordination System)
    """

    def __init__(self, timeout: float = 6.0):
        self.timeout = timeout
        self.user_agent = "RAKSHAK-AI/2.0 (Disaster Intelligence and Response Agent)"

    async def check_live_earthquakes(self, lat: Optional[float] = None, lon: Optional[float] = None, max_radius_km: float = 500.0) -> Dict[str, Any]:
        """
        Fetches real-time seismic telemetry from USGS and filters earthquakes near the target coordinates.
        """
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.get(url, headers={"User-Agent": self.user_agent})
                if res.status_code == 200:
                    data = res.json()
                    features = data.get("features", [])
                    
                    matched_events = []
                    for f in features:
                        props = f.get("properties", {})
                        geom = f.get("geometry", {})
                        coords = geom.get("coordinates", [0, 0, 0])
                        eq_lon, eq_lat, depth = coords[0], coords[1], coords[2]
                        
                        mag = props.get("mag", 0.0)
                        place = props.get("place", "Unknown")
                        time_ms = props.get("time", 0)
                        time_str = datetime.fromtimestamp(time_ms / 1000.0).strftime("%Y-%m-%d %H:%M:%S") if time_ms else "Recent"
                        
                        distance_km = None
                        if lat is not None and lon is not None:
                            distance_km = self._haversine_distance(lat, lon, eq_lat, eq_lon)
                            if distance_km <= max_radius_km:
                                matched_events.append({
                                    "magnitude": mag,
                                    "place": place,
                                    "latitude": eq_lat,
                                    "longitude": eq_lon,
                                    "depth_km": depth,
                                    "distance_km": round(distance_km, 1),
                                    "time_utc": time_str,
                                    "url": props.get("url")
                                })
                        elif mag >= 4.5:
                            # If no coordinates provided, keep significant regional events
                            matched_events.append({
                                "magnitude": mag,
                                "place": place,
                                "latitude": eq_lat,
                                "longitude": eq_lon,
                                "depth_km": depth,
                                "distance_km": None,
                                "time_utc": time_str,
                                "url": props.get("url")
                            })

                    return {
                        "status": "LIVE_FEED_ONLINE",
                        "provider": "USGS Real-time Seismic Grid",
                        "total_global_24h_events": len(features),
                        "nearby_events_count": len(matched_events),
                        "events": matched_events[:5],
                        "active_seismic_risk": len(matched_events) > 0 and any(e.get("magnitude", 0) >= 4.0 for e in matched_events),
                        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
        except Exception as e:
            return {
                "status": "FEED_TIMEOUT_OR_OFFLINE",
                "provider": "USGS Real-time Seismic Grid",
                "error": str(e),
                "nearby_events_count": 0,
                "events": [],
                "active_seismic_risk": False
            }

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Computes great-circle distance between two points in kilometers."""
        r = 6371.0  # Earth's radius in km
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = math.sin(d_lat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c
