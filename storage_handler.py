import os
import json

HIGH_SCORE_FILE = "data/highscores.json"
FEATURED_ARTICLES_FILE = "data/featured_articles.json"

if not os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, "w", encoding='utf-8') as handle:
        data = {}
        json.dump(data, handle)


def load_featured_articles():
    """
    Returns the featured article list from a file
    """
    if not os.path.exists(FEATURED_ARTICLES_FILE):
        return None

    with open(FEATURED_ARTICLES_FILE, "r", encoding='utf-8') as handle:
        return json.load(handle)


def save_featured_articles(featured_articles):
    """
    Saves the featured article list to a file
    """
    with open(FEATURED_ARTICLES_FILE, "w", encoding='utf-8') as handle:
        return json.dump(featured_articles, handle)


def load_high_scores():
    """
    Returns a dictionary with user name as keys, the values are
    dictionaries with a key/value pair for each game_mode/highscore
    """
    with open(HIGH_SCORE_FILE, "r", encoding='utf-8') as handle:
        return json.load(handle)


def save_high_scores(high_scores):
    """
    Saves the current high score dict to file
    """
    with open(HIGH_SCORE_FILE, "w", encoding='utf-8') as handle:
        json.dump(high_scores, handle)


def get_user_high_scores(name):
    """
    Returns the high score dict for given name
    Returns None if the user has no high score entry
    """
    high_scores = load_high_scores()

    if name in high_scores:
        return high_scores[name]
    else:
        return None


def init_user_high_scores(name):
    """
    Initialises the high score dict for a user name
    Returns the empty high score dict
    """
    high_scores = load_high_scores()

    high_scores[name] = {}
    high_scores[name]["death"] = 0
    high_scores[name]["speed"] = 0

    save_high_scores(high_scores)


def update_user_high_score(name, user_high_scores):
    """
    Updates high score value for given game mode
    """
    high_scores = load_high_scores()

    high_scores[name] = user_high_scores

    save_high_scores(high_scores)


def delete_user_high_score(name):
    """
    Deletes high score values for user name
    """
    high_scores = load_high_scores()

    high_scores.pop(name)

    save_high_scores(high_scores)


def main():
    if not get_user_high_scores("test"):
        print("No data yet!")
    init_user_high_scores("test")
    if get_user_high_scores("test"):
        print("High scores initialised!")
    update_user_high_score("test", "death", 666)
    print(f"Updated death score: {get_user_high_scores("test")["death"]}")
    update_user_high_score("test", "speed", 1000)
    print(f"Updated speed score: {get_user_high_scores("test")["speed"]}")
    delete_user_high_score("test")
    if not get_user_high_scores("test"):
        print("Data deleted!")


if __name__ == "__main__":
    main()
