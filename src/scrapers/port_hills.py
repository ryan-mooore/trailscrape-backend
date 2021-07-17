area_trails = [
    "Anaconda",
    "Bowenvale Traverse",
    "Bowenvale Downhill",
    "Bridle Path",
    "Captain Thomas",
    "Castle Rock",
    "Godley Head",
    "Greenwood Park",
    "John Britten",
    "V Twin",
    "Lava Flow",
    "Flying Nun",
    "Mt Vernon Track",
    "Taramea",
    "Witch Hill"
]

def get_trails(soup):
    
    trails = []
    trail_id = 0
    table = soup.table.tbody.find_all('tr')
    for tr in table:
        for t in area_trails:
            if t in tr.find('td').a.text:
                name = t
                raw_status = tr.find_all('td')[1].text.upper()
        
                if raw_status == "OPEN":
                    status = True

                if raw_status == "CLOSED":
                    status = False

                # Return #
                trails.append({
                    "id": trail_id,
                    "name": name,
                    "grade": None,
                    "isOpen": status
                })

                trail_id += 1

    return trails