import requests
from bs4 import BeautifulSoup
import logging
import re
from documents.documents import db

logging.basicConfig(level=20)


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
    logging.info("Updating trails in Trailforks regions...")
    for activity, locations in db.regions.find_one()["activities"].items():
        for region_ID, region in locations.items():
            for park_ID, park in region["parks"].items():
                try:
                    trailforksID = park["methodInfo"]["regionID"]
                except KeyError: continue
                regionIDs = trailforksID if type(trailforksID) is list else [trailforksID]
                
                for regionID in regionIDs:
                    try:
                        trailforks_region = db.trailforks_region.find_one({"str_ID": regionID})
                        existing_trails = set(trailforks_region["trails"])
                    except IndexError:
                        trailforks_region = db.trailforks_region.find_one({"str_ID": regionID})
                        existing_trails = set()
                    
                    new_trails = get_trail_ids(regionID)
                    trailforks_region["trails"] = new_trails
                    trailforks_region["num_ID"] = get_numeric_id(regionID)

                    new_trails = set(new_trails)

                    logging.info(
                        f"Updated trails for {regionID} "
                        f"({len(existing_trails ^ new_trails)} modified: "
                        f"{', '.join(str(trailID) for trailID in existing_trails ^ new_trails)})"
                    )
                    db.trailforks_region.update_one({"_id": trailforks_region["_id"]}, {"$set": trailforks_region})

    logging.info("Done.")