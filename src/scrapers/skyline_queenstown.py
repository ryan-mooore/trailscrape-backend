import re

def get_trails(soup):
    
    trails = []
    trail_id = 0
    table = soup.find("ul", {"class" : "c-accordion o-list--reset js-expand-collapse"})
    for row in table.find_all("li")[1:]:

        name = row.find("h3").text

        raw_grade = row.find("div", {"class": "c-body-text"}).text
        
        res = re.search(r"Grade:.*(\d)\s\w+", raw_grade)
        if res:
            grade = int(res.group(1))
        else:
            grade = None

        trails.append({
            "id": trail_id,
            "name": name,
            "grade": grade,
        })

        trail_id += 1

    return trails