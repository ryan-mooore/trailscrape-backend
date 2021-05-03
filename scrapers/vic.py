import re

def get_park_status(soup):

    status = soup.table.tbody.find((lambda tag: tag.text == "Victoria Park Downhill")).next_sibling.next_sibling.text.upper()

    if status.endswith("OPEN"):
        return True
    if status.endswith("CLOSED"):
        return False