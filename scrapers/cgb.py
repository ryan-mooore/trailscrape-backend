import re

def get_trails(soup):

    trails = []
    trail_id = 0
    
    trail_list = soup.find("table", {"id" : "trackStatus"})

    for row in (trail_list.find_all("tr")):
        #skip table header
        if row.th:
            continue
        name = row.find("td").a.string
        status_src = row.find_all("td")[1].img.get("src")

        #closed-icon or open-icon
        raw_status = re.search(
            r".+\/(\w+)-icon.png",
            status_src
        ).group(1).upper()

        parsed_status = None

        if raw_status == "OPEN":
            status = True
        if raw_status == "CLOSED":
            status = False

        trails.append({
            "id": trail_id,
            "name": name,
            "grade": None,
            "isOpen": status
        })

        trail_id += 1

    return trails