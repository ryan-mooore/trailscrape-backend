def get_park_status(soup):

    status = soup.find("aside", {"id": "text-4"}).find("div", class_="textwidget").find("p").find("span").string

    if status.startswith("OPEN"):
        return True
    if status.startswith("CLOSED"):
        return False
    return None