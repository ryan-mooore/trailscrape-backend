from types import SimpleNamespace
import requests
from typing import Any

ApiTrail = dict[str, Any]

def get_trails(region: SimpleNamespace) -> list[dict]:

    def filter_attributes(trail: ApiTrail, attribute_map: dict[str, str]) -> ApiTrail:
        return {attribute_map[k]:v for (k, v) in trail.items() if k in attribute_map.keys()}
    
    res = requests.get(region.methodInfo["url"]).json()
    return [filter_attributes(trail, attribute_map=region.methodInfo["attributeMap"]) for trail in res if region.methodInfo["filter"] and trail[region.methodInfo["filter"]] == True]