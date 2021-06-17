from types import SimpleNamespace
from documents.documents import TrailforksRegion
from typing import Any
import requests
import logging

def get_trail(trail_id: int, api_key:str="docs") -> dict[str, Any]:
    logging.info(f"TF API:requesting trail {trail_id}")
    return requests.get(f"https://www.trailforks.com/api/1/trail?id={trail_id}&api_key={api_key}").json()

def get_region(region_id: int, since:int=0, api_key: str = "docs") -> dict[str, Any]:
    logging.info(f"TF API:requesting region {region_id}")
    return requests.get(f"https://www.trailforks.com/api/1/region_status?rids={region_id}&since={since}&api_key={api_key}").json()

def get_trails(region: SimpleNamespace) -> list[dict]:
    trails = []
    regionIDs = region.methodInfo["regionID"] if type(region.methodInfo["regionID"]) is list else [region.methodInfo["regionID"]]
    for regionID in regionIDs:
        trailforks_region = TrailforksRegion.objects(str_ID=regionID)[0]
        for trail_id in trailforks_region.trails:
            res = get_trail(trail_id)["data"]
            trails.append(
                {
                    "name": res["title"],
                    "trailforksName": res["title"],
                    "grade": res["difficulty"],
                    "isOpen": bool(res["status"]),
                    "trailforksID": trail_id,
                }
            )
    return trails

def get_park_status(region: SimpleNamespace) -> bool:
    regionIDs = region.methodInfo["regionID"] if type(region.methodInfo["regionID"]) is list else [region.methodInfo["regionID"]]
    open_regions = []
    for regionID in regionIDs:
        trailforks_region = TrailforksRegion.objects(str_ID=regionID)[0]
        open_regions.append(get_region(trailforks_region.num_ID)["data"]["updates"]["regions_info"]["rows"][0][1] != 4)
    return True in open_regions