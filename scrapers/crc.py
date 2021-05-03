import re

def get_park_status(soup):

    status = soup.table.tbody.find((lambda tag: tag.text == "Crocodile MTB Trails")).next_sibling.next_sibling.text.upper()

    if status == "OPEN":
        return True
    if status == "CLOSED":
        return False