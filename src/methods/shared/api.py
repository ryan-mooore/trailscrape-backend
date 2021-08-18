import requests
from typing import Any

ApiTrail = dict[str, Any]

def get_trails(info: dict) -> list[dict]:

    def filter_attributes(trail: ApiTrail, attribute_map: dict[str, str]) -> ApiTrail:
        return {attribute_map[k]:v for (k, v) in trail.items() if k in attribute_map.keys()}
    
    res = requests.get(info["url"]).json()
    return [filter_attributes(trail, attribute_map=info["attributeMap"]) for trail in res if info["filter"] and trail[info["filter"]] == True]