from types import SimpleNamespace
from typing import Any, Union
import requests
from helpers.setup import log
from helpers.setup import db

def get_api_trails(trail_ids: list[int]) -> dict[str, Any]:
    log.info(f"Requesting {len(trail_ids)} trails...")
    return requests.get(f"https://www.trailforks.com/rms/?rmsP=j2&mod=trailforks&op=map&format=json&z=1000&layers=tracks&bboxa=-180,-90,180,90&display=status&activitytype=1&trailids={','.join([str(trail_id) for trail_id in trail_ids])}").json()

def get_api_region(region_id: int, since:int=0, api_key: str = "docs") -> dict[str, Any]:
    log.info(f"Requesting region {region_id}...")
    return requests.get(f"https://www.trailforks.com/api/1/region_status?rids={region_id}&since={since}&api_key={api_key}").json()

def get_trails(regions: Union[str, list[str]]) -> list[dict]:

    gradeMap = {
        "2": 1, # beginner
        "3": 2, # easy
        "4": 3, # intermediate
        "11": 4, # advanced
        "5": 5, # expert
        "6": 6, # extreme / dbl black
        "8": 7 # Proline
    }

    trails = []
    regionIDs = regions if type(regions) is list else [regions]
    for regionID in regionIDs:
        log.info(f"Requesting trails for region {regionID}").add()
        log.info("Finding regionID...")
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
        log.sub()
    return trails

def get_park_status(regions: Union[str, list[str]]) -> bool:
    regionIDs = regions if type(regions) is list else [regions]
    open_regions = []
    for regionID in regionIDs:
        log.info(f"Requesting status for region {regionID}").add()
        log.info("Finding regionID...")
        trailforks_region = db.trailforks_region.find_one({"str_ID": regionID})
        open_regions.append(get_api_region(trailforks_region["num_ID"])["data"]["updates"]["regions_info"]["rows"][0][1] != 4)
        log.sub()
    return True in open_regions