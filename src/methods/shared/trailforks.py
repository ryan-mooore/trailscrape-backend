from types import SimpleNamespace
from typing import Any
import requests
import logging
from documents.documents import db

def get_api_trails(trail_ids: list[int]) -> dict[str, Any]:
    logging.info(f"TF API:requesting trails {trail_ids}")
    return requests.get(f"https://www.trailforks.com/rms/?rmsP=j2&mod=trailforks&op=map&format=json&z=1000&layers=tracks&bboxa=-180,-90,180,90&display=status&activitytype=1&trailids={','.join([str(trail_id) for trail_id in trail_ids])}").json()

def get_api_region(region_id: int, since:int=0, api_key: str = "docs") -> dict[str, Any]:
    logging.info(f"TF API:requesting region {region_id}")
    return requests.get(f"https://www.trailforks.com/api/1/region_status?rids={region_id}&since={since}&api_key={api_key}").json()

def get_trails(region: SimpleNamespace) -> list[dict]:

    gradeMap = {
        "2": 1, # beginner
        "3": 2, # easy
        "4": 3, # intermediate
        "11": 4, # advanced
        "5": 5, # expert
        "6": 6, # extreme / dbl black
        "8": None # Proline
    }

    trails = []
    regionIDs = region["methodInfo"]["regionID"] if type(region["methodInfo"]["regionID"]) is list else [region["methodInfo"]["regionID"]]
    for regionID in regionIDs:
        trailforks_region = db.trailforks_region.find_one({"str_ID": regionID})
        for trail in get_api_trails(trailforks_region["trails"].keys())["rmsD"]["tracks"]["rmsD"]["tracks"]:
            trails.append(
                {
                    "name": trail["name"],
                    "trailforksName": trailforks_region["trails"][trail["id"]],
                    "grade": gradeMap[trail["difficulty"]],
                    "isOpen": bool(trail["colour"] != "#be0014"),
                    "trailforksID": trail["id"],
                }
            )
    return trails

def get_park_status(region: SimpleNamespace) -> bool:
    regionIDs = region["methodInfo"]["regionID"] if type(region["methodInfo"]["regionID"]) is list else [region["methodInfo"]["regionID"]]
    open_regions = []
    for regionID in regionIDs:
        trailforks_region = db.trailforks_region.find_one({"str_ID": regionID})
        open_regions.append(get_api_region(trailforks_region["num_ID"])["data"]["updates"]["regions_info"]["rows"][0][1] != 4)
    return True in open_regions