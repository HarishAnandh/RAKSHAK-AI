import re
import difflib
from typing import Optional, Dict, Any, Tuple, List

# Complete Registry of ALL 38 Tamil Nadu Districts + Extended Nationwide States
REGIONS_REGISTRY: Dict[str, Dict[str, Any]] = {
    # 1. Chennai
    "Chennai": {
        "aliases": ["chennai", "madras", "velachery", "tambaram", "omr", "ecr", "guindy", "adyar", "t nagar", "anna nagar", "porur", "sholinganallur", "ambattur", "royapettah", "triplicane", "mylapore", "perambur"],
        "zone": "North Coastal Tamil Nadu",
        "terrain": "Lowland Coastal Plain & Urban Drainage Basin",
        "coastal": True,
        "district": "Chennai",
        "is_primary_eoc": True,
        "vulnerability_score": 88,
        "primary_threat": "Urban Inundation & Bay of Bengal Cyclones",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 92, "risk_level": "CRITICAL", "historical_notes": "Adyar/Cooum basin overflow & high urban surface runoff", "icon": "Waves"},
            {"disaster_type": "Cyclone", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Direct northeast monsoon landfall corridor (Vardah, Michaung)", "icon": "Wind"},
            {"disaster_type": "Storm", "probability_percent": 85, "risk_level": "HIGH", "historical_notes": "Intense torrential downpours exceeding 200mm/24hr", "icon": "CloudLightning"},
            {"disaster_type": "Tsunami", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Vulnerable open coastline (Marina/Besant Nagar belt)", "icon": "AlertTriangle"},
            {"disaster_type": "Earthquake", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Seismic Zone III (Moderate risk)", "icon": "Activity"},
            {"disaster_type": "Fire", "probability_percent": 40, "risk_level": "MEDIUM", "historical_notes": "Urban commercial & electrical fire density", "icon": "Flame"},
            {"disaster_type": "Landslide", "probability_percent": 2, "risk_level": "LOW", "historical_notes": "Flat coastal terrain; negligible slope risk", "icon": "Mountain"}
        ]
    },
    # 2. Chengalpattu
    "Chengalpattu": {
        "aliases": ["chengalpattu", "changalpattu", "chengalpet", "chengalpet district", "mahabalipuram", "mamallapuram", "kelambakkam", "vandalur", "guduvanchery", "maraimalai nagar", "madurantakam", "tiruporur", "cheyyur"],
        "zone": "North Coastal Tamil Nadu",
        "terrain": "Coastal Lake Basin & Palar River Estuary",
        "coastal": True,
        "district": "Chengalpattu",
        "is_primary_eoc": True,
        "vulnerability_score": 84,
        "primary_threat": "Palar River Inundation & Coastal Surges",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 86, "risk_level": "HIGH", "historical_notes": "Madurantakam lake surplus & Palar river flooding", "icon": "Waves"},
            {"disaster_type": "Cyclone", "probability_percent": 84, "risk_level": "HIGH", "historical_notes": "East Coast Road (ECR) cyclone impact track", "icon": "Wind"},
            {"disaster_type": "Storm", "probability_percent": 80, "risk_level": "HIGH", "historical_notes": "Heavy coastal squalls during northeast monsoon", "icon": "CloudLightning"},
            {"disaster_type": "Tsunami", "probability_percent": 40, "risk_level": "MEDIUM", "historical_notes": "Mahabalipuram and coastal fishing settlements", "icon": "AlertTriangle"},
            {"disaster_type": "Fire", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Industrial clusters along GST corridor", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 25, "risk_level": "LOW", "historical_notes": "Seismic Zone II/III boundary", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 5, "risk_level": "LOW", "historical_notes": "Isolated hillocks; low landslide risk", "icon": "Mountain"}
        ]
    },
    # 3. Erode
    "Erode": {
        "aliases": ["erode", "bhavani", "gobichettipalayam", "gobi", "perundurai", "sathyamangalam", "anthiyur", "kodumudi", "chennimalai", "modakkurichi"],
        "zone": "West-Central Tamil Nadu",
        "terrain": "Kaveri & Bhavani River Basin & Sathyamangalam Foothills",
        "coastal": False,
        "district": "Erode",
        "is_primary_eoc": True,
        "vulnerability_score": 77,
        "primary_threat": "Bhavani River Flooding & Sathyamangalam Forest Fires",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 84, "risk_level": "HIGH", "historical_notes": "Bhavanisagar Dam surplus release and Kaveri river swelling", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 76, "risk_level": "HIGH", "historical_notes": "Sathyamangalam Tiger Reserve dry season forest fires", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Severe pre-monsoon convective thunderstorms and squalls", "icon": "CloudLightning"},
            {"disaster_type": "Cyclone", "probability_percent": 40, "risk_level": "MEDIUM", "historical_notes": "Inland depression rain bands", "icon": "Wind"},
            {"disaster_type": "Earthquake", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Seismic Zone II (Low to Moderate intraplate)", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 25, "risk_level": "LOW", "historical_notes": "Bargur and Hasanur ghat section slips", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Landlocked inland region (0% Tsunami risk)", "icon": "AlertTriangle"}
        ]
    },
    # 4. Coimbatore
    "Coimbatore": {
        "aliases": ["coimbatore", "kovai", "pollachi", "mettupalayam", "sulur", "valparai", "annur", "kinathukadavu", "madukkarai"],
        "zone": "West Tamil Nadu",
        "terrain": "Western Ghats Rainshadow Plateau & Mountain Slopes",
        "coastal": False,
        "district": "Coimbatore",
        "is_primary_eoc": True,
        "vulnerability_score": 79,
        "primary_threat": "Valparai Ghat Landslides & Noyyal River Spate",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Valparai / Anamalai ghat roads prone to debris flows", "icon": "Mountain"},
            {"disaster_type": "Fire", "probability_percent": 78, "risk_level": "HIGH", "historical_notes": "Western Ghats forest fire season (Feb - May)", "icon": "Flame"},
            {"disaster_type": "Flood", "probability_percent": 72, "risk_level": "HIGH", "historical_notes": "Bhavani and Noyyal river flash floods", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 74, "risk_level": "HIGH", "historical_notes": "Southwest monsoon high winds & cloudbursts", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 36, "risk_level": "LOW", "historical_notes": "Seismic Zone III (Coimbatore fault region)", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Shielded by Western Ghats", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Landlocked inland region (0% Tsunami risk)", "icon": "AlertTriangle"}
        ]
    },
    # 5. Tiruppur
    "Tiruppur": {
        "aliases": ["tiruppur", "tirupur", "dharapuram", "kangeyam", "avanshi", "avinashi", "udumalpet", "palladam", "madathukulam"],
        "zone": "West Tamil Nadu",
        "terrain": "Noyyal & Amaravathi River Basins",
        "coastal": False,
        "district": "Tiruppur",
        "is_primary_eoc": True,
        "vulnerability_score": 73,
        "primary_threat": "Amaravathi Dam Surplus Floods & Industrial Fires",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 76, "risk_level": "HIGH", "historical_notes": "Amaravathi reservoir release & Noyyal basin urban flooding", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Textile manufacturing & garment cluster fire density", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "High wind squalls across open plateau", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 32, "risk_level": "LOW", "historical_notes": "Seismic Zone II/III", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 36, "risk_level": "LOW", "historical_notes": "Inland depression rain", "icon": "Wind"},
            {"disaster_type": "Landslide", "probability_percent": 15, "risk_level": "LOW", "historical_notes": "Udumalpet foothill border sections", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Landlocked inland territory", "icon": "AlertTriangle"}
        ]
    },
    # 6. Salem
    "Salem": {
        "aliases": ["salem", "attur", "mettur", "omalur", "yercaud", "edappadi", "sankari", "valapady", "gangavalli"],
        "zone": "North-Western Tamil Nadu",
        "terrain": "Plateau & Shevaroy Mountain Foothills",
        "coastal": False,
        "district": "Salem",
        "is_primary_eoc": True,
        "vulnerability_score": 76,
        "primary_threat": "Mettur Dam Surplus Discharges & Yercaud Ghat Landslides",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 82, "risk_level": "HIGH", "historical_notes": "Yercaud Ghat road slope instabilities during monsoons", "icon": "Mountain"},
            {"disaster_type": "Flood", "probability_percent": 78, "risk_level": "HIGH", "historical_notes": "Cauvery basin flooding downstream of Mettur reservoir", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 74, "risk_level": "HIGH", "historical_notes": "Shevaroy forest fires in dry summer months", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Thunderstorm downpours across foothills", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 32, "risk_level": "LOW", "historical_notes": "Seismic Zone II (Low to Moderate)", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 42, "risk_level": "MEDIUM", "historical_notes": "Depression wind squalls & high rainfall", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Landlocked inland region (0% Tsunami risk)", "icon": "AlertTriangle"}
        ]
    },
    # 7. Namakkal
    "Namakkal": {
        "aliases": ["namakkal", "rasipuram", "tiruchengode", "kolli hills", "kolli", "paramathi velur", "kumarapalayam"],
        "zone": "North-Western Tamil Nadu",
        "terrain": "Cauvery River Border & Kolli Hills Mountain Slopes",
        "coastal": False,
        "district": "Namakkal",
        "is_primary_eoc": True,
        "vulnerability_score": 74,
        "primary_threat": "Kolli Hills Ghat Landslides & Cauvery Inundation",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 80, "risk_level": "HIGH", "historical_notes": "Kolli Hills hairpin bend slope washouts", "icon": "Mountain"},
            {"disaster_type": "Flood", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Paramathi Velur and Kumarapalayam Cauvery flooding", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "Kolli forest fires and poultry industry clusters", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Squall thunderstorms", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 28, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 38, "risk_level": "LOW", "historical_notes": "Peripheral monsoon rains", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland territory", "icon": "AlertTriangle"}
        ]
    },
    # 8. Cuddalore
    "Cuddalore": {
        "aliases": ["cuddalore", "chidambaram", "neyveli", "panruti", "virudhachalam", "parangipettai", "kurinjipadi", "bhuvanagiri", "srimushnam"],
        "zone": "North-Central Coastal Tamil Nadu",
        "terrain": "Low Coastal Basin & Delta Confluence",
        "coastal": True,
        "district": "Cuddalore",
        "is_primary_eoc": True,
        "vulnerability_score": 94,
        "primary_threat": "Extreme Cyclone Landfalls (Thane) & Gedilam River Floods",
        "hazards": [
            {"disaster_type": "Cyclone", "probability_percent": 96, "risk_level": "CRITICAL", "historical_notes": "Prime landfall zone for severe cyclonic storms in Bay of Bengal", "icon": "Wind"},
            {"disaster_type": "Flood", "probability_percent": 92, "risk_level": "CRITICAL", "historical_notes": "Simultaneous Pennaiyar/Gedilam river overflows & tidal lock", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Gale-force storms with surges above 2.5 meters", "icon": "CloudLightning"},
            {"disaster_type": "Tsunami", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "Severely impacted during 2004 Indian Ocean Tsunami", "icon": "AlertTriangle"},
            {"disaster_type": "Earthquake", "probability_percent": 28, "risk_level": "LOW", "historical_notes": "Seismic Zone III", "icon": "Activity"},
            {"disaster_type": "Fire", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Neyveli energy corridor industrial monitoring", "icon": "Flame"},
            {"disaster_type": "Landslide", "probability_percent": 2, "risk_level": "LOW", "historical_notes": "Flat coastal delta", "icon": "Mountain"}
        ]
    },
    # 9. Madurai
    "Madurai": {
        "aliases": ["madurai", "meenakshi", "thiruparankundram", "usilampatti", "melur", "vadipatti", "peraiyur", "sholavandan"],
        "zone": "South Tamil Nadu",
        "terrain": "Vaigai River Plain & Inland Semi-Arid Basin",
        "coastal": False,
        "district": "Madurai",
        "is_primary_eoc": True,
        "vulnerability_score": 72,
        "primary_threat": "Vaigai River Flash Inundation & Severe Heat/Thunderstorms",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Vaigai river surplus release affecting low-lying riverbanks", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Pre-monsoon and northeast monsoon squall thunderstorms", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 38, "risk_level": "LOW", "historical_notes": "Seismic Zone II / intraplate fault tremors", "icon": "Activity"},
            {"disaster_type": "Fire", "probability_percent": 55, "risk_level": "MEDIUM", "historical_notes": "Dry scrubland & dense heritage marketplace areas", "icon": "Flame"},
            {"disaster_type": "Cyclone", "probability_percent": 48, "risk_level": "MEDIUM", "historical_notes": "Depression rains originating from Gulf of Mannar", "icon": "Wind"},
            {"disaster_type": "Landslide", "probability_percent": 10, "risk_level": "LOW", "historical_notes": "Minor slope risk near Nagamalai hillocks", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Landlocked inland region (0% Tsunami risk)", "icon": "AlertTriangle"}
        ]
    },
    # 10. Nilgiris
    "Nilgiris": {
        "aliases": ["nilgiris", "nilgiri", "ooty", "udhagamandalam", "coonoor", "kotagiri", "gudalur", "kundah"],
        "zone": "Western Ghats Hilly Region",
        "terrain": "High Altitude Mountainous Terrain (Elevation > 2000m)",
        "coastal": False,
        "district": "Nilgiris",
        "is_primary_eoc": True,
        "vulnerability_score": 92,
        "primary_threat": "Massive Mountain Landslides & Cloudburst Torrents",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 96, "risk_level": "CRITICAL", "historical_notes": "Extreme slope instability; historic multi-location slips in monsoons", "icon": "Mountain"},
            {"disaster_type": "Storm", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Heavy southwest & northeast monsoon precipitation", "icon": "CloudLightning"},
            {"disaster_type": "Flood", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Gudalur and Pykara river valley flash floods", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 72, "risk_level": "HIGH", "historical_notes": "Shola grassland & eucalyptus plantation fires", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 34, "risk_level": "LOW", "historical_notes": "Seismic Zone III fault systems", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 40, "risk_level": "MEDIUM", "historical_notes": "High-velocity mountain wind squalls", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Mountain elevation (0% Tsunami risk)", "icon": "AlertTriangle"}
        ]
    },
    # 11. Nagapattinam
    "Nagapattinam": {
        "aliases": ["nagapattinam", "nagai", "velankanni", "veda", "vedaranyam", "kilvelur", "thirukuvalai"],
        "zone": "Central Coastal Tamil Nadu",
        "terrain": "Low-Lying Coastal Delta Plain & Estuary",
        "coastal": True,
        "district": "Nagapattinam",
        "is_primary_eoc": True,
        "vulnerability_score": 95,
        "primary_threat": "Severe Cyclone Surges (Gaja) & Tsunami Inundation",
        "hazards": [
            {"disaster_type": "Cyclone", "probability_percent": 98, "risk_level": "CRITICAL", "historical_notes": "Most cyclone-prone coastal district in southern India (Cyclone Gaja)", "icon": "Wind"},
            {"disaster_type": "Flood", "probability_percent": 94, "risk_level": "CRITICAL", "historical_notes": "Cauvery tail-end drainage block & sea water backflow", "icon": "Waves"},
            {"disaster_type": "Tsunami", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Epicenter of 2004 Indian Ocean Tsunami fatalities in Tamil Nadu", "icon": "AlertTriangle"},
            {"disaster_type": "Storm", "probability_percent": 90, "risk_level": "CRITICAL", "historical_notes": "Heavy coastal surges and gale squalls", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 25, "risk_level": "LOW", "historical_notes": "Seismic Zone II/III", "icon": "Activity"},
            {"disaster_type": "Fire", "probability_percent": 25, "risk_level": "LOW", "historical_notes": "Thatched rural coastal settlements", "icon": "Flame"},
            {"disaster_type": "Landslide", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Zero slope terrain", "icon": "Mountain"}
        ]
    },
    # 12. Kanyakumari
    "Kanyakumari": {
        "aliases": ["kanyakumari", "nagercoil", "cape comorin", "kanniyakumari", "padmanabhapuram", "colachel", "marthandam", "kuzhithurai", "thuckalay"],
        "zone": "Southernmost Coastal Tamil Nadu",
        "terrain": "Tri-Sea Confluence & Southern Western Ghats Foothills",
        "coastal": True,
        "district": "Kanyakumari",
        "is_primary_eoc": True,
        "vulnerability_score": 89,
        "primary_threat": "Arabian Sea Cyclones (Ockhi), Sea Surge & Foothill Landslides",
        "hazards": [
            {"disaster_type": "Cyclone", "probability_percent": 92, "risk_level": "CRITICAL", "historical_notes": "Exposed to both Arabian Sea & Bay of Bengal depressions (Ockhi)", "icon": "Wind"},
            {"disaster_type": "Flood", "probability_percent": 86, "risk_level": "HIGH", "historical_notes": "Pechiparai / Perunchani dam releases & Kodayar overflow", "icon": "Waves"},
            {"disaster_type": "Tsunami", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "High vulnerability at Colachel and Kanyakumari cape", "icon": "AlertTriangle"},
            {"disaster_type": "Landslide", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "Hilly Western Ghats sections around Pechiparai / Keeriparai", "icon": "Mountain"},
            {"disaster_type": "Storm", "probability_percent": 84, "risk_level": "HIGH", "historical_notes": "High ocean swell waves & gale force squalls", "icon": "CloudLightning"},
            {"disaster_type": "Fire", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Rubber plantation / scrub dry spells", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 25, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"}
        ]
    },
    # 13. Tiruchirappalli
    "Tiruchirappalli": {
        "aliases": ["tiruchirappalli", "tiruchi", "trichy", "srirangam", "manapparai", "thuvakudi", "lalgudi", "musiri", "thuraiyur"],
        "zone": "Central Tamil Nadu",
        "terrain": "Cauvery & Coleroon River Confluence Plain",
        "coastal": False,
        "district": "Tiruchirappalli",
        "is_primary_eoc": True,
        "vulnerability_score": 75,
        "primary_threat": "Cauvery-Coleroon Delta River Inundation",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 84, "risk_level": "HIGH", "historical_notes": "Upper Anicut / Mukkombu surplus discharge flooding", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Convective thunderstorm downpours", "icon": "CloudLightning"},
            {"disaster_type": "Cyclone", "probability_percent": 55, "risk_level": "MEDIUM", "historical_notes": "Inland depression rain bands", "icon": "Wind"},
            {"disaster_type": "Fire", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Commercial central bazaars & industrial estates", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 26, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 15, "risk_level": "LOW", "historical_notes": "Pachamalai hill slopes in north district", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland central location (0% Tsunami risk)", "icon": "AlertTriangle"}
        ]
    },
    # 14. Thanjavur
    "Thanjavur": {
        "aliases": ["thanjavur", "tanjore", "kumbakonam", "pattukkottai", "thiruvaiyaru", "peravurani", "orathanadu"],
        "zone": "Cauvery Delta Tamil Nadu",
        "terrain": "Grand Anicut / Cauvery Delta Rice Bowl Basin",
        "coastal": True,
        "district": "Thanjavur",
        "is_primary_eoc": True,
        "vulnerability_score": 86,
        "primary_threat": "Delta Canal Inundation & Cyclone Gaja Impacts",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 90, "risk_level": "CRITICAL", "historical_notes": "Vennar/Cauvery canal bank breaches & standing water", "icon": "Waves"},
            {"disaster_type": "Cyclone", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Pattukkottai / coastal delta cyclone destruction", "icon": "Wind"},
            {"disaster_type": "Storm", "probability_percent": 82, "risk_level": "HIGH", "historical_notes": "Heavy delta monsoon storms", "icon": "CloudLightning"},
            {"disaster_type": "Tsunami", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Palk Strait shoreline", "icon": "AlertTriangle"},
            {"disaster_type": "Earthquake", "probability_percent": 24, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Fire", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Thatched delta villages", "icon": "Flame"},
            {"disaster_type": "Landslide", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Flat delta terrain", "icon": "Mountain"}
        ]
    },
    # 15. Dindigul
    "Dindigul": {
        "aliases": ["dindigul", "kodaikanal", "palani", "oddanchatram", "natham", "nilakkottai", "vedasandur"],
        "zone": "South-Central Tamil Nadu",
        "terrain": "Palani Hills / Kodaikanal Mountain Ghats & Semi-Arid Plains",
        "coastal": False,
        "district": "Dindigul",
        "is_primary_eoc": True,
        "vulnerability_score": 80,
        "primary_threat": "Kodaikanal Ghat Landslides & Mountain Cloudbursts",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 90, "risk_level": "CRITICAL", "historical_notes": "Kodaikanal ghat road slips (Batlagundu & Palani routes)", "icon": "Mountain"},
            {"disaster_type": "Fire", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Palani Hills shola and pine forest summer fires", "icon": "Flame"},
            {"disaster_type": "Flood", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Amaravathi & Shanmuganathi river flash floods", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 72, "risk_level": "HIGH", "historical_notes": "Heavy mountain squall rain", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 40, "risk_level": "MEDIUM", "historical_notes": "Western Ghats peripheral rain", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland territory", "icon": "AlertTriangle"}
        ]
    },
    # 16. Theni
    "Theni": {
        "aliases": ["theni", "bodinayakanur", "bodi", "periyakulam", "cumbum", "uttampalayam", "megamalai", "andipatti"],
        "zone": "South-Western Tamil Nadu",
        "terrain": "Cumbum Valley & High Meghamalai / Western Ghats Hills",
        "coastal": False,
        "district": "Theni",
        "is_primary_eoc": True,
        "vulnerability_score": 82,
        "primary_threat": "Meghamalai & Bodi Ghat Landslides / Forest Fires",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Bodimettu & Meghamalai ghat landslides in monsoon", "icon": "Mountain"},
            {"disaster_type": "Fire", "probability_percent": 80, "risk_level": "HIGH", "historical_notes": "Meghamalai / Kurangani reserve forest fires", "icon": "Flame"},
            {"disaster_type": "Flood", "probability_percent": 74, "risk_level": "HIGH", "historical_notes": "Vaigai Dam and Suruli falls flash deluges", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Western Ghats monsoon thunder cells", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 32, "risk_level": "LOW", "historical_notes": "Seismic Zone II/III", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Shielded by High Ghats", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland valley", "icon": "AlertTriangle"}
        ]
    },
    # 17. Tirunelveli
    "Tirunelveli": {
        "aliases": ["tirunelveli", "nellai", "palayamkottai", "cheranmahadevi", "ambasamudram", "nanguneri", "radhapuram"],
        "zone": "Deep South Tamil Nadu",
        "terrain": "Thamirabarani River Basin & Western Ghats Border",
        "coastal": False,
        "district": "Tirunelveli",
        "is_primary_eoc": True,
        "vulnerability_score": 85,
        "primary_threat": "Thamirabarani River Megafloods & Manjolai Landslides",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 92, "risk_level": "CRITICAL", "historical_notes": "Record Thamirabarani river flooding (Dec 2023 deluge)", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 84, "risk_level": "HIGH", "historical_notes": "Extreme monsoon downpours exceeding 400mm", "icon": "CloudLightning"},
            {"disaster_type": "Landslide", "probability_percent": 78, "risk_level": "HIGH", "historical_notes": "Manjolai tea estate & Kalakad hills slips", "icon": "Mountain"},
            {"disaster_type": "Cyclone", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Gulf of Mannar cyclonic rainstorms", "icon": "Wind"},
            {"disaster_type": "Fire", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "KMTR forest border monitoring", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 24, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland river basin", "icon": "AlertTriangle"}
        ]
    },
    # 18. Thoothukudi
    "Thoothukudi": {
        "aliases": ["thoothukudi", "tuticorin", "tiruchendur", "kovilpatti", "kayalpattinam", "sathankulam", "vilathikulam", "ottapidaram"],
        "zone": "Deep South Coastal Tamil Nadu",
        "terrain": "Gulf of Mannar Coastal Plain & Port Corridor",
        "coastal": True,
        "district": "Thoothukudi",
        "is_primary_eoc": True,
        "vulnerability_score": 91,
        "primary_threat": "Catastrophic Flash Flooding & Coastal Sea Ingress",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 94, "risk_level": "CRITICAL", "historical_notes": "Historic December 2023 mega-inundation of Tuticorin town", "icon": "Waves"},
            {"disaster_type": "Cyclone", "probability_percent": 85, "risk_level": "HIGH", "historical_notes": "Gulf of Mannar cyclones & gale surges", "icon": "Wind"},
            {"disaster_type": "Storm", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Severe convective sea storms", "icon": "CloudLightning"},
            {"disaster_type": "Tsunami", "probability_percent": 60, "risk_level": "MEDIUM", "historical_notes": "Tiruchendur / Kayalpattinam coastal vulnerability", "icon": "AlertTriangle"},
            {"disaster_type": "Fire", "probability_percent": 40, "risk_level": "MEDIUM", "historical_notes": "Thermal plant & port industrial chemical safety", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 22, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Flat coastal plain", "icon": "Mountain"}
        ]
    },
    # 19. Ramanathapuram
    "Ramanathapuram": {
        "aliases": ["ramanathapuram", "ramnad", "rameswaram", "dhanushkodi", "paramakudi", "keelakarai", "kilakarai", "mandapam", "kamuthi"],
        "zone": "Deep South Coastal Tamil Nadu",
        "terrain": "Pamban Island, Dhanushkodi Strip & Arid Coastal Plains",
        "coastal": True,
        "district": "Ramanathapuram",
        "is_primary_eoc": True,
        "vulnerability_score": 93,
        "primary_threat": "Extreme Cyclonic Surges (1964 Rameswaram Disaster) & Sea Ingress",
        "hazards": [
            {"disaster_type": "Cyclone", "probability_percent": 95, "risk_level": "CRITICAL", "historical_notes": "1964 Dhanushkodi super-cyclone & frequent storm tracks", "icon": "Wind"},
            {"disaster_type": "Storm", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Pamban Bridge high wind gale warnings", "icon": "CloudLightning"},
            {"disaster_type": "Flood", "probability_percent": 82, "risk_level": "HIGH", "historical_notes": "Gundar / Vaigai tail-end flooding & sea water backflow", "icon": "Waves"},
            {"disaster_type": "Tsunami", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "Rameswaram coastal tip exposure", "icon": "AlertTriangle"},
            {"disaster_type": "Fire", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Scrub fires in summer", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 20, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Flat sandspit & coastal plain", "icon": "Mountain"}
        ]
    },
    # 20. Kanchipuram
    "Kanchipuram": {
        "aliases": ["kanchipuram", "kancheepuram", "conjeevaram", "sriperumbudur", "walajabad", "uthiramerur", "kundrathur"],
        "zone": "North Tamil Nadu",
        "terrain": "Palar River Basin & Sriperumbudur Industrial Hub",
        "coastal": False,
        "district": "Kanchipuram",
        "is_primary_eoc": True,
        "vulnerability_score": 81,
        "primary_threat": "Chembarambakkam / Palar River Inundation & Industrial Fire Risk",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Chembarambakkam reservoir release & Palar river flooding", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Sriperumbudur / Oragadam automobile & electronics industrial zone", "icon": "Flame"},
            {"disaster_type": "Cyclone", "probability_percent": 78, "risk_level": "HIGH", "historical_notes": "North coastal cyclone peripheral track", "icon": "Wind"},
            {"disaster_type": "Storm", "probability_percent": 76, "risk_level": "HIGH", "historical_notes": "Monsoon squalls", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 28, "risk_level": "LOW", "historical_notes": "Seismic Zone II/III", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 5, "risk_level": "LOW", "historical_notes": "Negligible elevation", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland district", "icon": "AlertTriangle"}
        ]
    },
    # 21. Tiruvallur
    "Tiruvallur": {
        "aliases": ["tiruvallur", "thiruvallur", "avadi", "ponneri", "gummidipoondi", "ennore", "tiruttani", "poonamallee", "red hills", "minjur"],
        "zone": "North Coastal Tamil Nadu",
        "terrain": "Kosasthalaiyar & Araniyar River Delta & Ennore Creek",
        "coastal": True,
        "district": "Tiruvallur",
        "is_primary_eoc": True,
        "vulnerability_score": 87,
        "primary_threat": "Poondi Dam Surplus Floods, Ennore Oil Spills & Cyclones",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 92, "risk_level": "CRITICAL", "historical_notes": "Poondi reservoir surplus & Kosasthalaiyar river inundation", "icon": "Waves"},
            {"disaster_type": "Cyclone", "probability_percent": 86, "risk_level": "HIGH", "historical_notes": "Pulicat / Gummidipoondi coastal cyclone landfall", "icon": "Wind"},
            {"disaster_type": "Storm", "probability_percent": 82, "risk_level": "HIGH", "historical_notes": "Heavy coastal storms", "icon": "CloudLightning"},
            {"disaster_type": "Fire", "probability_percent": 55, "risk_level": "MEDIUM", "historical_notes": "Ennore / Manali petrochemical industrial cluster", "icon": "Flame"},
            {"disaster_type": "Tsunami", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Pulicat lake sandbar coastal villages", "icon": "AlertTriangle"},
            {"disaster_type": "Earthquake", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Seismic Zone III", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 5, "risk_level": "LOW", "historical_notes": "Tiruttani hill temple slopes only", "icon": "Mountain"}
        ]
    },
    # 22. Vellore
    "Vellore": {
        "aliases": ["vellore", "katpadi", "gudiyatham", "anaicut", "pernamallur"],
        "zone": "Northern Tamil Nadu",
        "terrain": "Palar River Basin & Eastern Ghats Hillocks",
        "coastal": False,
        "district": "Vellore",
        "is_primary_eoc": True,
        "vulnerability_score": 75,
        "primary_threat": "Palar River Flash Flooding & Summer Heatwaves",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 78, "risk_level": "HIGH", "historical_notes": "Palar river flash floods & Gudiyatham Mordhana dam releases", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Dry hills & tanneries industrial areas", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Thunderstorm squalls", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 32, "risk_level": "LOW", "historical_notes": "Seismic Zone III (Palar fault line)", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Inland depression rain", "icon": "Wind"},
            {"disaster_type": "Landslide", "probability_percent": 20, "risk_level": "LOW", "historical_notes": "Mordhana ghat section", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland district", "icon": "AlertTriangle"}
        ]
    },
    # 23. Ranipet
    "Ranipet": {
        "aliases": ["ranipet", "ranipettai", "arrakkonam", "arakkonam", "walajah", "arcot", "sholinghur"],
        "zone": "Northern Tamil Nadu",
        "terrain": "Palar River Basin & Industrial Chemical Hub",
        "coastal": False,
        "district": "Ranipet",
        "is_primary_eoc": True,
        "vulnerability_score": 74,
        "primary_threat": "Palar River Overflow & Industrial Chemical Fire Hazards",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 78, "risk_level": "HIGH", "historical_notes": "Palar river inundation at Arcot & Arakkonam waterlogging", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 72, "risk_level": "HIGH", "historical_notes": "SIPCOT industrial chemical manufacturing units", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Thunderstorm squalls", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Seismic Zone III", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 48, "risk_level": "MEDIUM", "historical_notes": "Depression rains", "icon": "Wind"},
            {"disaster_type": "Landslide", "probability_percent": 10, "risk_level": "LOW", "historical_notes": "Sholinghur hill temple section", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland location", "icon": "AlertTriangle"}
        ]
    },
    # 24. Tirupathur
    "Tirupathur": {
        "aliases": ["tirupathur", "tirupattur", "thirupathur", "ambur", "vaniyambadi", "yelagiri", "natrampalli"],
        "zone": "Northern Tamil Nadu",
        "terrain": "Yelagiri & Javadhu Hills Slopes & Palar Valley",
        "coastal": False,
        "district": "Tirupathur",
        "is_primary_eoc": True,
        "vulnerability_score": 78,
        "primary_threat": "Yelagiri Hills Landslides & Ambur/Vaniyambadi Floods",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 84, "risk_level": "HIGH", "historical_notes": "Yelagiri ghat road 14 hairpin bend slips", "icon": "Mountain"},
            {"disaster_type": "Flood", "probability_percent": 76, "risk_level": "HIGH", "historical_notes": "Palar river flooding in Vaniyambadi and Ambur", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Javadhu & Yelagiri forest fires", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Hill squalls", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 28, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 38, "risk_level": "LOW", "historical_notes": "Inland rain", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland hills", "icon": "AlertTriangle"}
        ]
    },
    # 25. Tiruvannamalai
    "Tiruvannamalai": {
        "aliases": ["tiruvannamalai", "thiruvannamalai", "arani", "chengama", "polur", "vandavasi", "chetpet"],
        "zone": "Northern Tamil Nadu",
        "terrain": "Annamalai Holy Hill & Javadhu Hills Foothills",
        "coastal": False,
        "district": "Tiruvannamalai",
        "is_primary_eoc": True,
        "vulnerability_score": 77,
        "primary_threat": "Girivalam Mountain Debris Slips & Sathanur Dam Surplus",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 80, "risk_level": "HIGH", "historical_notes": "Annamalai hill boulder falls & Javadhu hills slips (Deepam rain)", "icon": "Mountain"},
            {"disaster_type": "Flood", "probability_percent": 78, "risk_level": "HIGH", "historical_notes": "Sathanur Dam surplus and Thenpennai river swelling", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 74, "risk_level": "HIGH", "historical_notes": "Annamalai mountain scrub fires during Karthigai Deepam", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Pre-monsoon thunderstorms", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 28, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Depression rains", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland mountain", "icon": "AlertTriangle"}
        ]
    },
    # 26. Viluppuram
    "Viluppuram": {
        "aliases": ["viluppuram", "villupuram", "tindivanam", "marakkanam", "gingee", "vikravandi", "vanur"],
        "zone": "North Coastal Tamil Nadu",
        "terrain": "Thenpennai River Basin & Marakkanam Salt Pans / Coast",
        "coastal": True,
        "district": "Viluppuram",
        "is_primary_eoc": True,
        "vulnerability_score": 85,
        "primary_threat": "Thenpennai River Floods & Marakkanam Cyclone Landfalls",
        "hazards": [
            {"disaster_type": "Cyclone", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Marakkanam / Tindivanam coastal cyclone impact corridor", "icon": "Wind"},
            {"disaster_type": "Flood", "probability_percent": 86, "risk_level": "HIGH", "historical_notes": "Thenpennai river inundation & Tindivanam waterlogging", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 82, "risk_level": "HIGH", "historical_notes": "Northeast monsoon storms", "icon": "CloudLightning"},
            {"disaster_type": "Tsunami", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Marakkanam coastline", "icon": "AlertTriangle"},
            {"disaster_type": "Fire", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Gingee scrubland", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 26, "risk_level": "LOW", "historical_notes": "Seismic Zone II/III", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 15, "risk_level": "LOW", "historical_notes": "Gingee fort hillocks", "icon": "Mountain"}
        ]
    },
    # 27. Kallakurichi
    "Kallakurichi": {
        "aliases": ["kallakurichi", "sankarapuram", "kalrayan hills", "ulundurpet", "chinnasalem", "tirukoilur"],
        "zone": "North-Central Tamil Nadu",
        "terrain": "Kalrayan Mountain Hills & Manimuktha River Basin",
        "coastal": False,
        "district": "Kallakurichi",
        "is_primary_eoc": True,
        "vulnerability_score": 79,
        "primary_threat": "Kalrayan Hills Landslides & Manimuktha Floods",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 84, "risk_level": "HIGH", "historical_notes": "Kalrayan hills tribal road slope washouts", "icon": "Mountain"},
            {"disaster_type": "Flood", "probability_percent": 78, "risk_level": "HIGH", "historical_notes": "Manimuktha & Gomukhi dam surplus discharges", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 72, "risk_level": "HIGH", "historical_notes": "Kalrayan reserve forest dry fires", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Monsoon thunderstorms", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 26, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 42, "risk_level": "MEDIUM", "historical_notes": "Inland depression rain", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland hills", "icon": "AlertTriangle"}
        ]
    },
    # 28. Mayiladuthurai
    "Mayiladuthurai": {
        "aliases": ["mayiladuthurai", "mayavaram", "sirkazhi", "tarangambadi", "tharangambadi", "poompuhar", "kuthalam"],
        "zone": "Central Coastal Tamil Nadu",
        "terrain": "Cauvery River Tail-End Delta & Poompuhar Coast",
        "coastal": True,
        "district": "Mayiladuthurai",
        "is_primary_eoc": True,
        "vulnerability_score": 92,
        "primary_threat": "Sirkazhi Record Cloudbursts & Tharangambadi Cyclones",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 94, "risk_level": "CRITICAL", "historical_notes": "Sirkazhi 440mm record cloudburst deluge (Nov 2022)", "icon": "Waves"},
            {"disaster_type": "Cyclone", "probability_percent": 92, "risk_level": "CRITICAL", "historical_notes": "Poompuhar / Tharangambadi direct cyclone landfall track", "icon": "Wind"},
            {"disaster_type": "Storm", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Severe delta squall rain and coastal surges", "icon": "CloudLightning"},
            {"disaster_type": "Tsunami", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "Tharangambadi historic tsunami inundation", "icon": "AlertTriangle"},
            {"disaster_type": "Earthquake", "probability_percent": 24, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Fire", "probability_percent": 25, "risk_level": "LOW", "historical_notes": "Rural thatched huts", "icon": "Flame"},
            {"disaster_type": "Landslide", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Flat coastal delta", "icon": "Mountain"}
        ]
    },
    # 29. Tiruvarur
    "Tiruvarur": {
        "aliases": ["tiruvarur", "thiruvarur", "mannargudi", "muthupet", "nannilam", "kudavasal", "valangaiman", "needamangalam"],
        "zone": "Cauvery Delta Tamil Nadu",
        "terrain": "Delta Canal Network & Muthupet Mangrove Estuary",
        "coastal": True,
        "district": "Tiruvarur",
        "is_primary_eoc": True,
        "vulnerability_score": 90,
        "primary_threat": "Muthupet Cyclone Surges & Agricultural Inundation",
        "hazards": [
            {"disaster_type": "Cyclone", "probability_percent": 92, "risk_level": "CRITICAL", "historical_notes": "Severe destruction during Cyclone Gaja in Mannargudi & Muthupet", "icon": "Wind"},
            {"disaster_type": "Flood", "probability_percent": 90, "risk_level": "CRITICAL", "historical_notes": "Delta drainage congestion submerging paddy crops", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 84, "risk_level": "HIGH", "historical_notes": "High wind squalls and monsoon rainfall", "icon": "CloudLightning"},
            {"disaster_type": "Tsunami", "probability_percent": 40, "risk_level": "MEDIUM", "historical_notes": "Muthupet lagoon buffer", "icon": "AlertTriangle"},
            {"disaster_type": "Fire", "probability_percent": 25, "risk_level": "LOW", "historical_notes": "Rural villages", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 22, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Flat delta", "icon": "Mountain"}
        ]
    },
    # 30. Ariyalur
    "Ariyalur": {
        "aliases": ["ariyalur", "jayankondam", "sendurai", "gangaikonda cholapuram", "udayarpalayam"],
        "zone": "Central Tamil Nadu",
        "terrain": "Marudaiyar River Basin & Cement Limestone Belt",
        "coastal": False,
        "district": "Ariyalur",
        "is_primary_eoc": True,
        "vulnerability_score": 72,
        "primary_threat": "Marudaiyar Flash Inundation & Industrial Mining Safety",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 76, "risk_level": "HIGH", "historical_notes": "Marudaiyar river overflow and mine pit waterlogging", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "Cashew plantation dry fires and cement industrial units", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Delta edge thunderstorms", "icon": "CloudLightning"},
            {"disaster_type": "Cyclone", "probability_percent": 52, "risk_level": "MEDIUM", "historical_notes": "Inland cyclone winds", "icon": "Wind"},
            {"disaster_type": "Earthquake", "probability_percent": 24, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 10, "risk_level": "LOW", "historical_notes": "Limestone quarry slopes", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland plain", "icon": "AlertTriangle"}
        ]
    },
    # 31. Perambalur
    "Perambalur": {
        "aliases": ["perambalur", "kunnam", "veppanthattai", "alathur"],
        "zone": "Central Tamil Nadu",
        "terrain": "Pachamalai Hills Border & Vellar Basin Plain",
        "coastal": False,
        "district": "Perambalur",
        "is_primary_eoc": True,
        "vulnerability_score": 70,
        "primary_threat": "Vellar River Flash Floods & Pachamalai Foothill Storms",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 74, "risk_level": "HIGH", "historical_notes": "Kottarai dam surplus & Vellar river overflow", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 60, "risk_level": "MEDIUM", "historical_notes": "Scrubland and dry cotton fields", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Convective summer thunderstorms", "icon": "CloudLightning"},
            {"disaster_type": "Cyclone", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Peripheral monsoon rains", "icon": "Wind"},
            {"disaster_type": "Earthquake", "probability_percent": 24, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 15, "risk_level": "LOW", "historical_notes": "Veppanthattai hill sections", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland plain", "icon": "AlertTriangle"}
        ]
    },
    # 32. Pudukkottai
    "Pudukkottai": {
        "aliases": ["pudukkottai", "pudukottai", "aranthangi", "viralimalai", "avudayarkoil", "gandarvakottai", "ilanji", "manamelkudi"],
        "zone": "Central Coastal Tamil Nadu",
        "terrain": "Palk Strait Coast & Semi-Arid Laterite Plateau",
        "coastal": True,
        "district": "Pudukkottai",
        "is_primary_eoc": True,
        "vulnerability_score": 82,
        "primary_threat": "Manamelkudi Cyclonic Landfalls & Vellar Floods",
        "hazards": [
            {"disaster_type": "Cyclone", "probability_percent": 86, "risk_level": "HIGH", "historical_notes": "Cyclone Gaja direct impact in Aranthangi & coastal belt", "icon": "Wind"},
            {"disaster_type": "Flood", "probability_percent": 78, "risk_level": "HIGH", "historical_notes": "Agniyar & Vellar river flash deluges", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 76, "risk_level": "HIGH", "historical_notes": "Palk Bay coastal squalls", "icon": "CloudLightning"},
            {"disaster_type": "Tsunami", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Palk Strait shoreline", "icon": "AlertTriangle"},
            {"disaster_type": "Fire", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Cashew and eucalyptus plantations", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 22, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 5, "risk_level": "LOW", "historical_notes": "Viralimalai hillock", "icon": "Mountain"}
        ]
    },
    # 33. Karur
    "Karur": {
        "aliases": ["karur", "kulithalai", "aravakkurichi", "manmangalam", "krishnarayapuram", "pugalur"],
        "zone": "Central Tamil Nadu",
        "terrain": "Amaravathi & Kaveri River Confluence Plain",
        "coastal": False,
        "district": "Karur",
        "is_primary_eoc": True,
        "vulnerability_score": 73,
        "primary_threat": "Mayaunur Barrage / Kaveri River Flooding",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 82, "risk_level": "HIGH", "historical_notes": "Mayanur Barrage surplus release inundating riverbanks", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 68, "risk_level": "HIGH", "historical_notes": "Textile bleaching & export processing fire safety", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "Thunderstorm squalls", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 25, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 40, "risk_level": "MEDIUM", "historical_notes": "Depression rains", "icon": "Wind"},
            {"disaster_type": "Landslide", "probability_percent": 5, "risk_level": "LOW", "historical_notes": "Inland flat plain", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland territory", "icon": "AlertTriangle"}
        ]
    },
    # 34. Dharmapuri
    "Dharmapuri": {
        "aliases": ["dharmapuri", "hogenakkal", "harur", "palacode", "pennagaram", "karimangalam", "nallampalli"],
        "zone": "North-Western Tamil Nadu",
        "terrain": "Cauvery Hogenakkal Gorge & Eastern Ghats Slopes",
        "coastal": False,
        "district": "Dharmapuri",
        "is_primary_eoc": True,
        "vulnerability_score": 77,
        "primary_threat": "Hogenakkal Cauvery Gorge Flash Floods & Chitteri Landslides",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 85, "risk_level": "HIGH", "historical_notes": "Hogenakkal waterfalls surge exceeding 1.5 lakh cusecs", "icon": "Waves"},
            {"disaster_type": "Landslide", "probability_percent": 80, "risk_level": "HIGH", "historical_notes": "Chitteri hills and Harur ghat road slips", "icon": "Mountain"},
            {"disaster_type": "Fire", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Pennagaram reserve forest dry summer fires", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Heavy monsoon thunderstorms", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 28, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Inland terrain", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland gorge", "icon": "AlertTriangle"}
        ]
    },
    # 35. Krishnagiri
    "Krishnagiri": {
        "aliases": ["krishnagiri", "hosur", "denkanikottai", "pochampalli", "urachikottai", "bargur", "kelamangalam"],
        "zone": "North-Western Tamil Nadu",
        "terrain": "Deccan Plateau Rim & South Pennar River Basin",
        "coastal": False,
        "district": "Krishnagiri",
        "is_primary_eoc": True,
        "vulnerability_score": 75,
        "primary_threat": "KRP Dam Surplus Flooding & Hosur Industrial Fire Risks",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 80, "risk_level": "HIGH", "historical_notes": "Krishnagiri Reservoir Project (KRP) surplus release flooding", "icon": "Waves"},
            {"disaster_type": "Fire", "probability_percent": 72, "risk_level": "HIGH", "historical_notes": "Hosur industrial electronic / EV manufacturing corridors", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Pre-monsoon thunderstorms & hailstorms", "icon": "CloudLightning"},
            {"disaster_type": "Landslide", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Thally & Denkanikottai hill forest sections", "icon": "Mountain"},
            {"disaster_type": "Earthquake", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Deccan plateau elevation", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "High plateau (0% Tsunami)", "icon": "AlertTriangle"}
        ]
    },
    # 36. Virudhunagar
    "Virudhunagar": {
        "aliases": ["virudhunagar", "sivakasi", "srivilliputhur", "rajapalayam", "aruppukkottai", "sattur", "kariapatti"],
        "zone": "South Tamil Nadu",
        "terrain": "Gundar River Plain & Sivakasi Industrial Pyrotechnic Belt",
        "coastal": False,
        "district": "Virudhunagar",
        "is_primary_eoc": True,
        "vulnerability_score": 83,
        "primary_threat": "Sivakasi Fireworks Industrial Blazes & Western Ghats Hill Slips",
        "hazards": [
            {"disaster_type": "Fire", "probability_percent": 94, "risk_level": "CRITICAL", "historical_notes": "Sivakasi fireworks/match industry explosion & fire risks", "icon": "Flame"},
            {"disaster_type": "Flood", "probability_percent": 74, "risk_level": "HIGH", "historical_notes": "Gundar & Vaippar river flash deluges", "icon": "Waves"},
            {"disaster_type": "Landslide", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "Srivilliputhur Megamalai tiger reserve ghat slips", "icon": "Mountain"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Monsoon squalls", "icon": "CloudLightning"},
            {"disaster_type": "Earthquake", "probability_percent": 25, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 42, "risk_level": "MEDIUM", "historical_notes": "Gulf of Mannar rain bands", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland territory", "icon": "AlertTriangle"}
        ]
    },
    # 37. Sivaganga
    "Sivaganga": {
        "aliases": ["sivaganga", "karaikudi", "devakottai", "manamadurai", "tirupathur sivaganga", "singampunari", "kalaiyarkoil"],
        "zone": "South Tamil Nadu",
        "terrain": "Vaigai River Plain & Chettinad Plateau",
        "coastal": False,
        "district": "Sivaganga",
        "is_primary_eoc": True,
        "vulnerability_score": 72,
        "primary_threat": "Vaigai River Inundation & Severe Pre-Monsoon Lightning",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 76, "risk_level": "HIGH", "historical_notes": "Manamadurai Vaigai river overflow", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 72, "risk_level": "HIGH", "historical_notes": "Lightning strikes and high wind squalls", "icon": "CloudLightning"},
            {"disaster_type": "Fire", "probability_percent": 55, "risk_level": "MEDIUM", "historical_notes": "Dry scrubland & heritage town fire safety", "icon": "Flame"},
            {"disaster_type": "Cyclone", "probability_percent": 50, "risk_level": "MEDIUM", "historical_notes": "Palk Bay depression rains", "icon": "Wind"},
            {"disaster_type": "Earthquake", "probability_percent": 24, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Landslide", "probability_percent": 5, "risk_level": "LOW", "historical_notes": "Flat plateau", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland district", "icon": "AlertTriangle"}
        ]
    },
    # 38. Tenkasi
    "Tenkasi": {
        "aliases": ["tenkasi", "courtallam", "kutralam", "sankarankovil", "kadayanallur", "shenkottai", "alangulam", "puliangudi", "vasudevanallur"],
        "zone": "Deep South Tamil Nadu",
        "terrain": "Courtallam Western Ghats Foothills & Chittar River Basin",
        "coastal": False,
        "district": "Tenkasi",
        "is_primary_eoc": True,
        "vulnerability_score": 83,
        "primary_threat": "Courtallam Flash Falls Deluges & Shenkottai Ghat Landslides",
        "hazards": [
            {"disaster_type": "Landslide", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Aryankavu / Shenkottai ghat pass mountain slips", "icon": "Mountain"},
            {"disaster_type": "Flood", "probability_percent": 86, "risk_level": "HIGH", "historical_notes": "Courtallam Main/Five falls flash floods & Chittar river surge", "icon": "Waves"},
            {"disaster_type": "Storm", "probability_percent": 82, "risk_level": "HIGH", "historical_notes": "Heavy southwest & northeast monsoon precipitation", "icon": "CloudLightning"},
            {"disaster_type": "Fire", "probability_percent": 65, "risk_level": "MEDIUM", "historical_notes": "Western Ghats forest border fires", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 26, "risk_level": "LOW", "historical_notes": "Seismic Zone II", "icon": "Activity"},
            {"disaster_type": "Cyclone", "probability_percent": 50, "risk_level": "MEDIUM", "historical_notes": "Depression rains", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland foothill valley", "icon": "AlertTriangle"}
        ]
    },

    # --- Extended Regions: Punjab & Others ---
    "Punjab": {
        "aliases": ["punjab", "amritsar", "ludhiana", "jalandhar", "patiala", "bathinda", "mohali"],
        "zone": "North India (Punjab State)",
        "terrain": "Alluvial River Plains (Indus Basin)",
        "coastal": False,
        "district": "Punjab",
        "is_primary_eoc": False,
        "vulnerability_score": 78,
        "primary_threat": "Sutlej/Beas River Monsoonal Floods & Himalayan Seismic Tremors",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 86, "risk_level": "HIGH", "historical_notes": "Sutlej, Beas, and Ghaggar river embankment breaches during monsoons", "icon": "Waves"},
            {"disaster_type": "Earthquake", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Seismic Zone IV in northern belts (Himalayan foothills proximity)", "icon": "Activity"},
            {"disaster_type": "Storm", "probability_percent": 72, "risk_level": "HIGH", "historical_notes": "Severe Western Disturbance dust storms & hailstorms", "icon": "CloudLightning"},
            {"disaster_type": "Fire", "probability_percent": 62, "risk_level": "MEDIUM", "historical_notes": "Post-harvest dry residue & industrial urban fires", "icon": "Flame"},
            {"disaster_type": "Cyclone", "probability_percent": 12, "risk_level": "LOW", "historical_notes": "Landlocked northern territory", "icon": "Wind"},
            {"disaster_type": "Landslide", "probability_percent": 8, "risk_level": "LOW", "historical_notes": "Sub-Himalayan Shivalik border zones only", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Landlocked inland territory (0% Tsunami risk)", "icon": "AlertTriangle"}
        ]
    },
    "Kerala": {
        "aliases": ["kerala", "kochi", "cochin", "thiruvananthapuram", "trivandrum", "kozhikode", "calicut", "wayanad", "idukki", "munnar"],
        "zone": "South-West Coastal India",
        "terrain": "Western Ghats Slopes & Coastal Arabian Sea Lowlands",
        "coastal": True,
        "district": "Kerala",
        "is_primary_eoc": False,
        "vulnerability_score": 93,
        "primary_threat": "Extreme Monsoon Floods & Wayanad/Idukki Landslides",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 94, "risk_level": "CRITICAL", "historical_notes": "Severe southwest monsoon river basin deluges (2018, 2019)", "icon": "Waves"},
            {"disaster_type": "Landslide", "probability_percent": 95, "risk_level": "CRITICAL", "historical_notes": "High-risk slope failures in Wayanad, Idukki, and Meppadi", "icon": "Mountain"},
            {"disaster_type": "Storm", "probability_percent": 88, "risk_level": "HIGH", "historical_notes": "Arabian Sea squalls and high rainfall cloudbursts", "icon": "CloudLightning"},
            {"disaster_type": "Cyclone", "probability_percent": 72, "risk_level": "HIGH", "historical_notes": "Arabian Sea coastal cyclonic depressions", "icon": "Wind"},
            {"disaster_type": "Tsunami", "probability_percent": 55, "risk_level": "MEDIUM", "historical_notes": "Arabian sea coastal surge vulnerability", "icon": "AlertTriangle"},
            {"disaster_type": "Fire", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Plantation dry spells", "icon": "Flame"},
            {"disaster_type": "Earthquake", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Seismic Zone III", "icon": "Activity"}
        ]
    },
    "Delhi": {
        "aliases": ["delhi", "new delhi", "ncr", "noida", "gurgaon", "gurugram", "faridabad"],
        "zone": "National Capital Region",
        "terrain": "Yamuna River Floodplain & Semi-Arid Urban Basin",
        "coastal": False,
        "district": "Delhi NCR",
        "is_primary_eoc": False,
        "vulnerability_score": 80,
        "primary_threat": "Yamuna River Floods & Himalayan Seismic Vulnerability (Zone IV)",
        "hazards": [
            {"disaster_type": "Flood", "probability_percent": 82, "risk_level": "HIGH", "historical_notes": "Hathnikund barrage release causing Yamuna floodplain inundation", "icon": "Waves"},
            {"disaster_type": "Earthquake", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Seismic Zone IV (High earthquake hazard zone)", "icon": "Activity"},
            {"disaster_type": "Fire", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Dense commercial & industrial electrical fire incidents", "icon": "Flame"},
            {"disaster_type": "Storm", "probability_percent": 68, "risk_level": "MEDIUM", "historical_notes": "Severe dust storms & pre-monsoon squalls", "icon": "CloudLightning"},
            {"disaster_type": "Cyclone", "probability_percent": 10, "risk_level": "LOW", "historical_notes": "Inland landlocked capital", "icon": "Wind"},
            {"disaster_type": "Landslide", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Flat terrain", "icon": "Mountain"},
            {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland capital", "icon": "AlertTriangle"}
        ]
    }
}

class RegionIdentificationTool:
    """Tool for deterministic or assisted location detection with fuzzy & phonetic matching."""
    
    def __init__(self):
        self.registry = REGIONS_REGISTRY

    def identify_region(self, text: str) -> Tuple[Optional[str], Optional[Dict[str, Any]], float]:
        """
        Analyzes natural language text and returns (canonical_name, metadata, confidence).
        Supports exact keyword match, regex word-boundary, and phonetic/fuzzy matching.
        """
        cleaned = text.lower()
        
        # 1. Exact / Word Boundary Matching
        for canonical_name, data in self.registry.items():
            for alias in data["aliases"]:
                pattern = r'\b' + re.escape(alias) + r'\b'
                if re.search(pattern, cleaned):
                    conf = 0.98 if data.get("is_primary_eoc") else 0.88
                    return canonical_name, data, conf

        # 2. Fuzzy Matching for Spelling Variations (e.g. "changalpattu" -> "Chengalpattu", "chengalpet")
        words = re.findall(r'\b[a-zA-Z]{4,}\b', cleaned)
        all_aliases = {}
        for canonical_name, data in self.registry.items():
            for alias in data["aliases"]:
                if len(alias) >= 4:
                    all_aliases[alias] = (canonical_name, data)

        for word in words:
            matches = difflib.get_close_matches(word, all_aliases.keys(), n=1, cutoff=0.80)
            if matches:
                matched_alias = matches[0]
                canonical_name, data = all_aliases[matched_alias]
                return canonical_name, data, 0.85

        return None, None, 0.0

    async def resolve_region_dynamic(self, text: str) -> Tuple[Optional[str], Optional[Dict[str, Any]], float]:
        """
        Dynamic GIS Resolver:
        1. Fast check against high-speed local registry (Tamil Nadu districts).
        2. If unlisted entity, performs live OpenStreetMap Nominatim geocoding for any global/regional location.
        """
        # Step 1: Local registry check
        reg_name, reg_meta, conf = self.identify_region(text)
        if reg_name and conf >= 0.85:
            return reg_name, reg_meta, conf

        # Step 2: Extract candidate entity words for Live OpenStreetMap Geocoding
        # Remove common query and disaster words
        stop_words = {
            "heavy", "severe", "major", "minor", "flooding", "flood", "rain", "cyclone", "storm", 
            "earthquake", "fire", "landslide", "tsunami", "alert", "warning", "in", "near", "at", 
            "reported", "today", "yesterday", "now", "happening", "is", "there", "what", "the", 
            "weather", "temperature", "forecast", "damage", "district", "city", "town", "village"
        }
        tokens = [w for w in re.findall(r'[a-zA-Z]{3,}', text) if w.lower() not in stop_words]
        if not tokens:
            return reg_name, reg_meta, conf

        candidate_query = " ".join(tokens[:3])
        try:
            import httpx
            url = f"https://nominatim.openstreetmap.org/search?q={candidate_query}&format=json&addressdetails=1&limit=1"
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.get(url, headers={"User-Agent": "RAKSHAK-AI-GIS-Agent"})
                if res.status_code == 200 and res.json():
                    item = res.json()[0]
                    resolved_name = item.get("name") or tokens[0].title()
                    addr = item.get("address", {})
                    state = addr.get("state", "India")
                    country = addr.get("country", "India")
                    lat = float(item.get("lat", 0.0))
                    lon = float(item.get("lon", 0.0))
                    
                    is_coastal = any(c in item.get("display_name", "").lower() for c in ["coast", "beach", "port", "bay", "ocean", "sea", "chennai", "cuddalore"])

                    dynamic_meta = {
                        "aliases": [resolved_name.lower()],
                        "zone": f"{state}, {country}",
                        "terrain": "Dynamic GIS Resolved Terrain",
                        "coastal": is_coastal,
                        "district": resolved_name,
                        "latitude": lat,
                        "longitude": lon,
                        "osm_display_name": item.get("display_name"),
                        "vulnerability_score": 75 if is_coastal else 65,
                        "primary_threat": "Dynamic Atmospheric & Regional Inundation Hazards",
                        "hazards": [
                            {"disaster_type": "Flood", "probability_percent": 80 if is_coastal else 68, "risk_level": "HIGH", "historical_notes": "Regional drainage basin & precipitation", "icon": "Waves"},
                            {"disaster_type": "Storm", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Convective thunderstorm activity", "icon": "CloudLightning"},
                            {"disaster_type": "Fire", "probability_percent": 50, "risk_level": "MEDIUM", "historical_notes": "Commercial / dry season monitoring", "icon": "Flame"},
                            {"disaster_type": "Earthquake", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Intraplate seismic activity", "icon": "Activity"},
                            {"disaster_type": "Cyclone", "probability_percent": 75 if is_coastal else 30, "risk_level": "HIGH" if is_coastal else "LOW", "historical_notes": "Coastal depression risk" if is_coastal else "Inland wind shield", "icon": "Wind"},
                            {"disaster_type": "Tsunami", "probability_percent": 40 if is_coastal else 0, "risk_level": "MEDIUM" if is_coastal else "LOW", "historical_notes": "Marine surge" if is_coastal else "Inland elevation safe", "icon": "AlertTriangle"}
                        ],
                        "emergency_contacts": [
                            "📞 112 — National Emergency Helpline",
                            "📞 1070 — State Disaster Management Authority",
                            "📞 101 — Fire and Rescue Services"
                        ]
                    }
                    return resolved_name, dynamic_meta, 0.92
        except Exception:
            pass

        return reg_name, reg_meta, conf

    def get_regional_hazard_profile(self, region_name: str, region_meta: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Generates the full hazard probability profile for a given region."""
        if not region_meta and region_name in self.registry:
            region_meta = self.registry[region_name]

        if not region_meta:
            # Generate smart deterministic baseline
            return {
                "region_name": region_name,
                "zone": "General Indian District",
                "terrain": "Mixed Terrain",
                "coastal": False,
                "composite_vulnerability_score": 65,
                "primary_threat": "Monsoonal Floods & Severe Thunderstorms",
                "hazards": [
                    {"disaster_type": "Flood", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Monsoon surface drainage & river overflow", "icon": "Waves"},
                    {"disaster_type": "Storm", "probability_percent": 70, "risk_level": "HIGH", "historical_notes": "Convective storm cells & squalls", "icon": "CloudLightning"},
                    {"disaster_type": "Fire", "probability_percent": 50, "risk_level": "MEDIUM", "historical_notes": "Summer dry conditions", "icon": "Flame"},
                    {"disaster_type": "Earthquake", "probability_percent": 35, "risk_level": "LOW", "historical_notes": "Seismic Zone II/III", "icon": "Activity"},
                    {"disaster_type": "Cyclone", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Inland peripheral wind activity", "icon": "Wind"},
                    {"disaster_type": "Landslide", "probability_percent": 15, "risk_level": "LOW", "historical_notes": "Local elevation dependent", "icon": "Mountain"},
                    {"disaster_type": "Tsunami", "probability_percent": 0, "risk_level": "LOW", "historical_notes": "Inland region", "icon": "AlertTriangle"}
                ],
                "emergency_contacts": ["112 (National Emergency)", "1077 (District Collectorate)", "1070 (State EOC)"]
            }

        hazards = region_meta.get("hazards", [])
        if not hazards:
            coastal = region_meta.get("coastal", False)
            hazards = [
                {"disaster_type": "Flood", "probability_percent": 85 if coastal else 70, "risk_level": "HIGH", "historical_notes": "Monsoonal inundation vulnerability", "icon": "Waves"},
                {"disaster_type": "Cyclone", "probability_percent": 85 if coastal else 35, "risk_level": "HIGH" if coastal else "LOW", "historical_notes": "Bay of Bengal weather system exposure", "icon": "Wind"},
                {"disaster_type": "Storm", "probability_percent": 75, "risk_level": "HIGH", "historical_notes": "Heavy seasonal convective squalls", "icon": "CloudLightning"},
                {"disaster_type": "Earthquake", "probability_percent": 30, "risk_level": "LOW", "historical_notes": "Seismic Zone II/III", "icon": "Activity"},
                {"disaster_type": "Fire", "probability_percent": 45, "risk_level": "MEDIUM", "historical_notes": "Urban and scrubland fire monitoring", "icon": "Flame"},
                {"disaster_type": "Tsunami", "probability_percent": 50 if coastal else 0, "risk_level": "MEDIUM" if coastal else "LOW", "historical_notes": "Coastal surge risk", "icon": "AlertTriangle"},
                {"disaster_type": "Landslide", "probability_percent": 10, "risk_level": "LOW", "historical_notes": "Slope risk minimal", "icon": "Mountain"}
            ]

        # Sort hazards by probability descending
        sorted_hazards = sorted(hazards, key=lambda h: h["probability_percent"], reverse=True)

        return {
            "region_name": region_name,
            "zone": region_meta.get("zone", "Tamil Nadu"),
            "terrain": region_meta.get("terrain", "Coastal / Inland Terrain"),
            "coastal": region_meta.get("coastal", False),
            "composite_vulnerability_score": region_meta.get("vulnerability_score", 75),
            "primary_threat": region_meta.get("primary_threat", f"Seasonal Inundation & Weather Hazards in {region_name}"),
            "hazards": sorted_hazards,
            "emergency_contacts": [
                "📞 112 — National Disaster & Police Helpline",
                f"📞 1077 — {region_name} District Disaster Operations Centre",
                "📞 1070 — Tamil Nadu State Disaster Management Authority (TNSDMA)",
                "📞 101 — Fire & Rescue Command"
            ]
        }

    def get_supported_regions(self):
        return [k for k, v in self.registry.items() if v.get("is_primary_eoc")]

    def get_all_regions(self):
        return list(self.registry.keys())

