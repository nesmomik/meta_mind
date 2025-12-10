import requests
import random
import storage_handler

API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {'User-Agent': 'meta_mind/0.1 (https://www.masterschool.com/; \
            hackathon@masterschool.com)'}

featured_articles = []

def get_featured_articles():
    """
    Fetch all featured articles
    """
    global featured_articles

    # try to load existing data if no data present
    if not featured_articles:
        featured_articles = storage_handler.load_featured_articles()
        # if data was in file, than exit
        if featured_articles:
            return
        # reset featured_articles to empty list instead of None type
        else:
            featured_articles = []

    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Category:Featured articles",
        "cmlimit": "500",
        "format": "json"
    }

    while True:
        response = requests.get(API_URL, params=params, headers=HEADERS).json()
        members = response["query"]["categorymembers"]

        for member in members:
            if member["ns"] == 0:
                featured_articles.append(member["title"])

        if "continue" not in response:
            break

        params["cmcontinue"] = response["continue"]["cmcontinue"]

    storage_handler.save_featured_articles(featured_articles)


def get_random_title():
    """
    Returns a random title from the featured articles list
    """
    return random.choice(featured_articles)


def get_language_count(title):
    """
    Returns the language count for the given title
    """

    params = {
    "action": "query",
    "titles": title,
    "prop": "langlinks",
    "lllimit": "max",
    "format": "json"
    }

    response = requests.get(API_URL, params=params, headers=HEADERS)
    data = response.json()

    # Extract language links
    pages = data["query"]["pages"]

    (page_id, page_info), = pages.items()
    langlinks = page_info.get("langlinks", [])

    # translations + english language
    return len(langlinks) + 1


def get_image_count(title):
    """
    Returns the count of non svg images for the given title
    """
    params = {
        "action": "query",
        "titles": title,
        "prop": "images",
        "imlimit": "max",
        "format": "json"
    }

    response = requests.get(API_URL, params=params, headers=HEADERS)
    data = response.json()

    # Extract images
    pages = data["query"]["pages"]

    (page_id, page_info), = pages.items()
    images = page_info.get("images", [])

    article_images = []

    for image in images:
        for keyword in ["icon", "decrease2", "arrow", "logo", "symbol"]:
            if keyword in image['title'].lower():
                continue
        else:
            article_images.append(image)

    return len(article_images)


def get_revision_count(title):
    """
    Returns the revision count i.e. number of edits
    """
    params = {
        "action": "query",
        "titles": title,
        "prop": "revisions",
        "rvlimit": "max",  # up to 500 per request
        "format": "json"
    }

    total_revisions = 0
    while True:
        response = requests.get(API_URL, params=params, headers=HEADERS)
        data = response.json()

        pages = data["query"]["pages"]
        for page_id, page_info in pages.items():
            revs = page_info.get("revisions", [])
            total_revisions += len(revs)

        if "continue" in data:
            params["rvcontinue"] = data["continue"]["rvcontinue"]
        else:
            break

    return total_revisions


def get_external_link_count(title):
    """
    Returns the external link count i.e. number of external links
    """
    params = {
        "action": "query",
        "titles": title,
        "prop": "extlinks",
        "ellimit": "max",  # up to 500 per request
        "format": "json"
    }

    all_extlinks = []
    while True:
        response = requests.get(API_URL, params=params, headers=HEADERS)
        data = response.json()

        pages = data["query"]["pages"]
        for page_id, page_info in pages.items():
            extlinks = page_info.get("extlinks", [])
            all_extlinks.extend([link["*"] for link in extlinks])

        # Check if there is a continuation
        if "continue" in data:
            params["elcontinue"] = data["continue"]["elcontinue"]
        else:
            break

    return len(all_extlinks)


def get_first_revision_year(title):
    """
    Returns the first revision year i.e. the creation year
    """
    params = {
        "action": "query",
        "titles": title,
        "prop": "revisions",
        "rvlimit": 1,
        "rvdir": "newer",  # oldest revision
        "rvprop": "timestamp",
        "format": "json"
    }

    response = requests.get(API_URL, params=params, headers=HEADERS)
    data = response.json()

    pages = data["query"]["pages"]
    (page_id, page_info), = pages.items()
    revs = page_info.get("revisions", [])

    creation_date = revs[0]["timestamp"]

    return creation_date[:4]


def get_internal_link_count(title):
    """
    Returns the internal link count
    """
    params = {
        "action": "query",
        "titles": title,
        "prop": "links",
        "pllimit": "max",
        "format": "json"
    }

    all_links = []
    while True:
        response = requests.get(API_URL, params=params, headers=HEADERS)
        data = response.json()

        pages = data["query"]["pages"]
        for page_id, page_info in pages.items():
            links = page_info.get("links", [])
            all_links.extend([link["title"] for link in links])

        # Check if there is a continuation
        if "continue" in data:
            params["plcontinue"] = data["continue"]["plcontinue"]
        else:
            break

    return len(all_links)


def get_page_length(title):
    """
    Returns the page length in bytes
    """
    params = {
        "action": "query",
        "titles": title,
        "prop": "info",
        "format": "json"
    }

    response = requests.get(API_URL, params=params, headers=HEADERS)
    data = response.json()

    # Extract page length
    pages = data["query"]["pages"]
    (page_id, page_info), = pages.items()

    # bytes
    return page_info['length']


def get_total_view_count(title):
    """
    Returns the total number of views for the article.
    Recorded since 2015
    """
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{title}/monthly/20150701/20251201"

    response = requests.get(url, headers=HEADERS)
    data = response.json()

    total_views = sum(item["views"] for item in data["items"])

    return total_views
