import re

import requests
from bs4 import BeautifulSoup

from helpers.setup import db, log


def get_trail_ids(region_name: str) -> dict[int, str]:
    content = requests.get(f"https://www.trailforks.com/region/{region_name}/trails")
    soup = BeautifulSoup(content.text, "html.parser")

    return {
        tr
        .find("div", class_="star-rating")
        .ul
        .get("id")
        .split("_")[1]
        :
        re.match(r"https:\/\/www.trailforks.com\/trails\/(.+)\/",
            tr
            .find("a", class_="green").get("href")
        ).group(1)
        for tr in (
            soup
            .find("table", {"id": "trails_table"})
            .tbody
            .find_all("tr")
        )
    }

def get_numeric_id(region_name: str) -> int:
    content = requests.get(f"https://www.trailforks.com/region/{region_name}/")
    soup = BeautifulSoup(content.text, "html.parser")
    return re.match(r"#(\d+)\s-", soup.find("li", class_="grey2 small").text).group(1)


if __name__ == "__main__":
    log.info("Updating trails in Trailforks regions...").add()
    for activity, locations in db.regions.find_one()["activities"].items():
        for region_ID, region in locations.items():
            for park_ID, park in region["parks"].items():
                try:
                    trailforksID = park["methods"]["trails"]["info"]["regionID"]
                except KeyError: continue
                log.info(f"Finding trailforks regions at {park_ID}...").add()
                trailforks_region_IDs = trailforksID if type(trailforksID) is list else [trailforksID]
                
                for trailforks_region_ID in trailforks_region_IDs:
                    log.info(f"Updating trailforks regionID at {trailforks_region_ID}...").add()
                    try:
                        log.info("Finding existing trails...")
                        trailforks_region = db.trailforks_region.find_one({"str_ID": trailforks_region_ID})
                        existing_trails = set(trailforks_region["trails"])
                    except TypeError:
                        log.info("No existing trails found. Creating new entry...")
                        db.trailforks_region.insert_one({"str_ID": trailforks_region_ID})
                        trailforks_region = db.trailforks_region.find_one({"str_ID": trailforks_region_ID})
                        existing_trails = set()
                    
                    log.info(f"Requesting trails...")
                    new_trails = get_trail_ids(trailforks_region_ID)
                    trailforks_region["trails"] = new_trails
                    trailforks_region["num_ID"] = get_numeric_id(trailforks_region_ID)

                    new_trails = set(new_trails)
                    
                    log.add() 
                    for trailID in existing_trails ^ new_trails:
                        log.info(f"Updated trail {trailID}")
                    log.sub()
                    
                    log.info("Saving to database...")
                    db.trailforks_region.update_one({"_id": trailforks_region["_id"]}, {"$set": trailforks_region})
                    log.sub().info(f"Done. {len(existing_trails ^ new_trails)} trails modified")
                log.sub()

    log.sub().info("Done")