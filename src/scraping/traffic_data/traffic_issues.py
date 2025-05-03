from scraping.traffic_data.traffic_germany import get_all_traffic_warnings, get_all_constructions


def traffic_issues():
    """
    Function to scrape traffic issues from the website.
    """
    return get_all_traffic_warnings()

def get_construction_data():
    """
    Function to scrape construction data from the website.
    """
    return get_all_constructions()