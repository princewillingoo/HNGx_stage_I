from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import pytz

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_day() -> str:
    # Get the current day of the week in full
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[datetime.now(pytz.utc).weekday()]

def is_valid_utc_time() -> bool:
    # Get current UTC time and check if it's within +/-2 minutes
    current_time = datetime.now(pytz.utc)
    allowed_time_window = timedelta(minutes=2)
    return current_time - allowed_time_window <= current_time <= current_time + allowed_time_window

@app.get("/api")
async def get_info(
    slack_name: str = Query(..., description="User Slack name"),
    track: str = Query(..., description="User chosen track (e.g., 'backend, devops')")
):
    if not is_valid_utc_time():
        raise HTTPException(status_code=500, detail="Invalid UTC time")

    current_day = get_current_day()
    utc_time = datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    github_file_url = "https://github.com/princewilling/HNGx/blob/main/task-one/server.py"
    github_repo_url = "https://github.com/princewilling/HNGx"
    status_code = 200

    return {
        "slack_name": slack_name,
        "current_day": current_day,
        "utc_time": utc_time,
        "track": track,
        "github_file_url": github_file_url,
        "github_repo_url": github_repo_url,
        "status_code": status_code
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
## $ python3 task-one/server.py