from bs4 import BeautifulSoup
import re, requests

def get_table(region_id):
    url = f"https://www.trailforks.com/region/{region_id}/status"
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html.parser")
    try:
        return soup.find("section", {"id" : "main"})\
                    .find_all("div")[1]\
                        .table\
                            .tbody
    except AttributeError:
        raise ConnectionError("Website could not be reached")

def scrape(region_ids):
    grade_helper = [
        "EASIEST",
        "EASY", 
        "INTERMEDIATE",
        "ADVANCED",
        "VERY DIFFICULT",
        "EXTREMELY DIFFICULT",
        "PROS ONLY"
    ]

    trails = []
    
    if type(region_ids) == str:
        region_ids = [region_ids]
    for region_id in region_ids:
        table = get_table(region_id)
        id = 0

        for row in table.find_all("tr"):
            a = row.find_all("td")[1].a
            
            name = a.string
            trail_url = a.get("href")

            tf_id = None
            try: 
                tf_id = int(re.match(r"#(\d+) - ", BeautifulSoup(requests.get(trail_url).text, "html.parser").find("li", class_="grey2 small").text).group(1))
            except Exception:
                print(name, "has no trail id")

            raw_grade = row.find_all("td")[0].span.get("title").upper()
            res = re.match(r"(?:(.+)\s\/.+|(.+):\s.+)|,\s(.+)", raw_grade)
            if res:
                grade = filter(None, res.groups())
                for result in grade: grade = grade_helper.index(result) + 1
            else:
                grade = None

            report = row.find_all("td")[2]
            status = report.span.get("title").upper() != "CLOSED / RED"

            trails.append({
                "id": id,
                "name": name,
                "grade": grade,
                "isOpen": status,
                "trailforksID": tf_id
            })
            id += 1

    return trails