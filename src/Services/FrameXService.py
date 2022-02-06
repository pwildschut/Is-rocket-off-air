import json
from typing import TypedDict, Text, List
import requests, os

API_BASE = os.getenv("API_BASE", "https://framex-dev.wadrid.net/api")
VIDEO_NAME = os.getenv(
    "VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
)

class VideoInfoResponse(TypedDict):
    """
    That's a video from the API
    """
    name: str
    width: int
    height: int
    frames: int
    frame_rate: List[int]
    url: str
    first_frame: str
    last_frame: str

class FrameXService:    
    def getFrame(frame: int):
        url = f"{API_BASE}/video/{VIDEO_NAME}/frame/{frame}/"
        r = requests.get(url)

        return r.content

    def getVideoInfo() -> VideoInfoResponse:
        url = f"{API_BASE}/video/{VIDEO_NAME}/"
       
        r = requests.get(url)

        return r.json()
