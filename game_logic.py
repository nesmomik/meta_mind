import random
import time
from getkey import getkey

import data_handler
import ui


# Dictionary containing all possible categories
# that can be used to compare the two articles
# and the corresponding functions to retrieve the metadata.
game_categories = {
    1: {"label": "Number of Bytes", "action": data_handler.get_page_length,
        "question": "Which article has more bytes?"},
    2: {"label": "Number of Available Languages", "action": data_handler.get_language_count,
        "question": "Which article has more languages?"},
    3: {"label": "Number of Edits", "action": data_handler.get_revision_count,
        "question": "Which article has more edits?"},
    4: {"label": "Year of Creation", "action": data_handler.get_first_revision_year,
        "question": "Which article is newer?"},
    5: {"label": "Number of Images", "action": data_handler.get_image_count,
        "question": "Which article has more images?"},
    6: {"label": "Number of Internal Links", "action": data_handler.get_internal_link_count,
        "question": "Which article has more internal links?"},
    7: {"label": "Number of External Links", "action": data_handler.get_external_link_count,
        "question": "Which article has more external links?"}
}


def pick_two_random_titles():
    """Random titles are selected from the Wikipedia library."""
    title1 = data_handler.get_random_title()
    title2 = data_handler.get_random_title()
    return title1, title2


def pick_random_game_category():
    return random.choice(list(game_categories.values()))

def ask_user_for_name():
    user_name = input("\n\n\n  👉 Enter Player Name: ")
    return user_name


def ask_player_choice(question: str = ""):
    """Ask the player to choose A or B, validate input."""
    while True:
        print(f" 🤔 {question} (A/B) ")
        key = getkey()
        if key in ("a", "b"):
            return key
        print("  ❌ Invalid input. (expected A or B as input!)")


def check_correct_option(title1_info, title2_info):
    """Compares the values of both articles."""
    if title1_info > title2_info:
        return "A"
    else:
        return "B"


def sudden_death(name, highscore):
    """Sudden Death mode: one mistake ends the run."""
    score = 0

    while True:
        ui.print_header("Sudden Death", score + 1)

        won = gameplay(
            pause_after=True,
            mode_name="Sudden Death",
            score=score,          # current streak BEFORE updating
            remaining_time=None,
        )

        # update score / highscore
        if won:
            score += 1
        else:
            # game over
            if score > highscore:
                ui.print_header("Sudden Death", won=True)
                print(f"  WOW!")
                print()
                print(f"    Your new highscore: {score}\n")
            else:
                ui.print_header("Sudden Death", won=False)
                print(f"  Nice try!")
                print()
                print(f"    Your score: {score}\n")
                print(f"    Your highscore: {highscore}\n\n")

            return score


def speed_mode(name, best_speed_score, time_limit_seconds: int = 60):
    """
    Speed Mode:
    - unlimited questions within a fixed time limit (default: 60 seconds)
    - every question counts, correct or not
    - score = number of correct answers
    - updates and returns new highscore if needed
    """
    score = 0           # correct answers
    total_questions = 0

    start_time = time.time()

    while True:
        ui.print_header("Speed Mode", question_num=score)
        elapsed = time.time() - start_time
        remaining = int(time_limit_seconds - elapsed)


        if remaining <= 0:
            print("\n  ⏰ Time's up!\n")
            break
        else:
            print(f"\n  ⏳ Remaining time: {remaining} seconds\n")

        won = gameplay(
            pause_after=False,
            mode_name="Speed Mode",
            score=score,
            remaining_time=remaining,
        )

        total_questions += 1

        if won:
            score += 1
            ui.print_header("Speed Mode", question_num=score, correct=True)
        else:
            ui.print_header("Speed Mode", question_num=score, correct=False)

    print(ui.header(f"  Speed Mode finished, {name}!\n"))
    print(f"  Correct answers: {score}")
    print(f"  Total questions: {total_questions}")

    if total_questions > 0:
        accuracy = (score / total_questions) * 100
        print(f"  Accuracy: {accuracy:.1f}%")
    else:
        print("  No questions answered 🤷‍♂️")

    # update highscore
    if score > best_speed_score:
        print(f"\n  🎉 New Speed Highscore! Old: {best_speed_score} → New: {score}")
        best_speed_score = score
    else:
        print(f"\n  Speed Highscore remains: {best_speed_score}")

    return best_speed_score


def gameplay(
    pause_after: bool = True,
    mode_name: str = "Sudden Death",
    score: int | None = None,
    remaining_time: int | None = None,
):
    """
    Plays a single question round.
    Returns True if player was correct, False otherwise.
    """

    # choose a random category
    random_game_category = pick_random_game_category()

    # skip Number of Edits in speed mode
    while (mode_name == "Speed Mode" and \
        random_game_category['label'] == "Number of Edits"):

        random_game_category = pick_random_game_category()

    # choose two random wikipedia titles
    title1, title2 = pick_two_random_titles()

    # function for this game category
    action_function = random_game_category["action"]

    # get metadata
    title1_info = action_function(title1)
    title2_info = action_function(title2)

    # avoid ties by re-drawing
    while title1_info == title2_info:
        title1, title2 = pick_two_random_titles()
        title1_info = action_function(title1)
        title2_info = action_function(title2)

    # show question
    category = random_game_category['label']
    ui.print_question(category, title1, title2)

    # player choice
    user_choice = ask_player_choice(random_game_category['question'])

    # determine correct option
    correct = check_correct_option(title1_info, title2_info)
    was_correct = user_choice.lower() == correct.lower()

    # result
    ui.print_header(mode_name, question_num=score, correct=was_correct)

    ui.print_answers(category, title1, title2, title1_info, title2_info)

    if pause_after:
        ui.wait_for_any_key()

    if mode_name == "Speed Mode":
        time.sleep(1)

    return was_correct
