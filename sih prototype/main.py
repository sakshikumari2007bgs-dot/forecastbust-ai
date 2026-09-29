from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi.responses import FileResponse

app = FastAPI(
    title="ForecastBust AI - SIH26079",
    description="AI-Based Forecast Bust Detection for Medium-Range Weather Forecasts",
    version="1.0.0"
)

# CORS allow (frontend se call karne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================== DATA ======================
REGIONS = {
    "nw": {
        "id": "nw",
        "name": "Northwest India",
        "lat": 28.5,
        "lng": 76.5,
        "bust": {1: 12, 2: 18, 3: 42, 4: 48, 5: 55, 6: 61, 7: 58, 8: 52, 9: 47, 10: 44},
        "conf": {1: 88, 2: 82, 3: 58, 4: 52, 5: 45, 6: 39, 7: 42, 8: 48, 9: 53, 10: 56},
        "drivers": [
            {"name": "Western Disturbance intensity", "impact": 0.82},
            {"name": "Moisture flux anomaly", "impact": 0.71},
            {"name": "Jet stream position error", "impact": 0.64},
            {"name": "Surface temperature bias", "impact": 0.41}
        ],
        "alert": "Elevated Risk: Western Disturbance + Monsoon trough interaction may degrade Day 3–5 rainfall skill over Northwest India."
    },
    "ne": {
        "id": "ne",
        "name": "Northeast India",
        "lat": 26.2,
        "lng": 92.5,
        "bust": {1: 8, 2: 11, 3: 19, 4: 28, 5: 35, 6: 41, 7: 44, 8: 39, 9: 36, 10: 33},
        "conf": {1: 92, 2: 89, 3: 81, 4: 72, 5: 65, 6: 59, 7: 56, 8: 61, 9: 64, 10: 67},
        "drivers": [
            {"name": "Monsoon trough position", "impact": 0.76},
            {"name": "Orographic lift uncertainty", "impact": 0.68},
            {"name": "Convective initiation bias", "impact": 0.55},
            {"name": "Soil moisture feedback", "impact": 0.38}
        ],
        "alert": "Moderate Risk: Orographic enhancement of rainfall remains a known model weakness."
    },
    "ci": {
        "id": "ci",
        "name": "Central India",
        "lat": 22.5,
        "lng": 78.5,
        "bust": {1: 10, 2: 15, 3: 31, 4: 39, 5: 47, 6: 53, 7: 49, 8: 45, 9: 41, 10: 38},
        "conf": {1: 90, 2: 85, 3: 69, 4: 61, 5: 53, 6: 47, 7: 51, 8: 55, 9: 59, 10: 62},
        "drivers": [
            {"name": "Monsoon depression track", "impact": 0.88},
            {"name": "Low-level jet strength", "impact": 0.73},
            {"name": "Diurnal cycle phase error", "impact": 0.59},
            {"name": "Land-surface coupling", "impact": 0.44}
        ],
        "alert": "High Attention: Active monsoon depression in Bay of Bengal."
    },
    "wi": {
        "id": "wi",
        "name": "Western India",
        "lat": 20.5,
        "lng": 73.5,
        "bust": {1: 9, 2: 14, 3: 22, 4: 30, 5: 38, 6: 44, 7: 42, 8: 37, 9: 34, 10: 31},
        "conf": {1: 91, 2: 86, 3: 78, 4: 70, 5: 62, 6: 56, 7: 58, 8: 63, 9: 66, 10: 69},
        "drivers": [
            {"name": "Arabian Sea moisture surge", "impact": 0.79},
            {"name": "Coastal convection bias", "impact": 0.61},
            {"name": "Heat low intensity", "impact": 0.52},
            {"name": "SSTs anomaly", "impact": 0.47}
        ],
        "alert": "Watch: Moisture surge from Arabian Sea can trigger rapid intensification."
    },
    "si": {
        "id": "si",
        "name": "South India",
        "lat": 12.5,
        "lng": 78.0,
        "bust": {1: 7, 2: 10, 3: 16, 4: 24, 5: 32, 6: 38, 7: 40, 8: 36, 9: 33, 10: 30},
        "conf": {1: 93, 2: 90, 3: 84, 4: 76, 5: 68, 6: 62, 7: 60, 8: 64, 9: 67, 10: 70},
        "drivers": [
            {"name": "ITCZ position error", "impact": 0.71},
            {"name": "Bay of Bengal convection", "impact": 0.66},
            {"name": "Topographic blocking", "impact": 0.48},
            {"name": "MJO phase influence", "impact": 0.43}
        ],
        "alert": "Relatively higher skill expected."
    },
    "ei": {
        "id": "ei",
        "name": "East India",
        "lat": 22.5,
        "lng": 86.5,
        "bust": {1: 11, 2: 16, 3: 27, 4: 36, 5: 44, 6: 50, 7: 48, 8: 43, 9: 39, 10: 36},
        "conf": {1: 89, 2: 84, 3: 73, 4: 64, 5: 56, 6: 50, 7: 52, 8: 57, 9: 61, 10: 64},
        "drivers": [
            {"name": "Monsoon depression landfall", "impact": 0.85},
            {"name": "Mesoscale convective systems", "impact": 0.70},
            {"name": "Soil moisture memory", "impact": 0.51},
            {"name": "Radiative feedback", "impact": 0.39}
        ],
        "alert": "Caution: Depression landfall location uncertainty drives large errors."
    }
}

# ====================== APIs ======================
@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/")
def root():
    return {
        "project": "ForecastBust AI",
        "ps_number": "SIH26079",
        "title": "AI-Based Forecast Bust Detection for Medium-Range Weather Forecasts",
        "organization": "Ministry of Earth Sciences (MoES) - NCMRWF",
        "status": "running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/regions")
def get_all_regions():
    result = []
    for r in REGIONS.values():
        result.append({
            "id": r["id"],
            "name": r["name"],
            "lat": r["lat"],
            "lng": r["lng"]
        })
    return {"regions": result}


@app.get("/api/region/{region_id}")
def get_region(region_id: str, lead: int = 3):
    if region_id not in REGIONS:
        return {"error": "Region not found"}
    
    r = REGIONS[region_id]
    conf = r["conf"].get(lead, 50)
    bust = r["bust"].get(lead, 30)
    
    return {
        "id": r["id"],
        "name": r["name"],
        "lat": r["lat"],
        "lng": r["lng"],
        "lead_time": lead,
        "confidence": conf,
        "bust_probability": bust,
        "expected_rmse": round(2.1 + (100 - conf) / 25, 1),
        "drivers": r["drivers"],
        "alert": r["alert"],
        "confidence_series": r["conf"],
        "bust_series": r["bust"]
    }


@app.get("/api/national")
def get_national_summary(lead: int = 3):
    confs = [r["conf"].get(lead, 50) for r in REGIONS.values()]
    busts = [r["bust"].get(lead, 30) for r in REGIONS.values()]
    
    avg_conf = round(sum(confs) / len(confs))
    avg_bust = round(sum(busts) / len(busts))
    
    highest_risk = max(REGIONS.values(), key=lambda x: x["bust"].get(lead, 0))
    
    return {
        "lead_time": lead,
        "avg_confidence": avg_conf,
        "avg_bust_probability": avg_bust,
        "expected_rmse": round(2.4 + (100 - avg_conf) / 28, 1),
        "highest_risk_region": {
            "id": highest_risk["id"],
            "name": highest_risk["name"],
            "bust_probability": highest_risk["bust"].get(lead, 0)
        },
        "alert": f"Day {lead} shows elevated bust risk over Northwest & Central India."
    }


@app.get("/api/map-data")
def get_map_data(lead: int = 3):
    result = []
    for r in REGIONS.values():
        result.append({
            "id": r["id"],
            "name": r["name"],
            "lat": r["lat"],
            "lng": r["lng"],
            "confidence": r["conf"].get(lead, 50),
            "bust_probability": r["bust"].get(lead, 30)
        })
    return {
        "lead_time": lead,
        "regions": result
    }


@app.get("/api/lead-times")
def get_all_lead_times():
    data = []
    for day in range(1, 11):
        confs = [r["conf"][day] for r in REGIONS.values()]
        busts = [r["bust"][day] for r in REGIONS.values()]
        data.append({
            "day": day,
            "avg_confidence": round(sum(confs) / len(confs)),
            "avg_bust": round(sum(busts) / len(busts))
        })
    return {"lead_times": data}


if __name__ == "__main__":
    import os, uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))