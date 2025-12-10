import random
import time

import data_handler
import ui
from ai_host import host_comment


# Dictionary containing all possible categories
# that can be used to compare the two articles
# and the corresponding functions to retrieve the metadata.
game_categories = {
    1: {"label": "Number of Bytes", "action": data_handler.get_page_length,
        "question": "Which article has the largest number of bytes?"},
    2: {"label": "Number of Available Languages", "action": data_handler.get_language_count,
        "question": "Which article has the largest number of available languages?"},
    3: {"label": "Number of Edits", "action": data_handler.get_revision_count,
        "question": "Which article has the largest number of edits?"},
    4: {"label": "Year of Creation", "action": data_handler.get_first_revision_year,
        "question": "Which article was created most recently?"},
    5: {"label": "Number of Images", "action": data_handler.get_image_count,
        "question": "Which article has the largest number of images?"},
    6: {"label": "Number of Internal Links", "action": data_handler.get_internal_link_count,
        "question": "Which article has the largest number of internal links?"},
    7: {"label": "Number of External Links", "action": data_handler.get_external_link_count,
        "question": "Which article has the largest number of external links?"}
}


def pick_two_random_titles():
    """Random titles are selected from the Wikipedia library."""
    title1 = data_handler.get_random_title()
    title2 = data_handler.get_random_title()
    return title1, title2


def pick_random_game_category():
    return random.choice(list(game_categories.values()))


def ask_user_for_name():
    user_name = input("  👉 Enter Player Name: ")
    return user_name


def ask_player_choice(question: str = ""):
    """Ask the player to choose A or B, validate input."""
    while True:
        user_choice = input(f"🤔 {question} (A/B) ")
        if user_choice.lower() in ("a", "b"):
            return user_choice
        print("❌ Invalid input. (expected A or B as input!)")


def check_correct_option(title1, title2, category):
    """Compares the values of both articles based on the selected category."""
    action = category["action"]
    meta1 = action(title1)
    meta2 = action(title2)

    if meta1 > meta2:
        return "A"
    else:
        return "B"


def print_answers(title1, title2, title1_info, title2_info):
    print("Answers:")
    print(f"{title1}: {title1_info}")
    print(f"{title2}: {title2_info}")


def sudden_death(name, highscore):
    """Sudden Death mode: one mistake ends the run."""
    score = 0

    while True:
        ui.print_round_header("Sudden Death", score + 1)

        won = gameplay(
            pause_after=True,
            mode_name="Sudden Death",
            score=score,          # current streak BEFORE updating
            remaining_time=None,
        )

        # update score / highscore
        if won:
            score += 1
            print(f"Score: {score}\n")

            if score > highscore:
                highscore = score
                print(f"New highscore: {highscore}\n")
                print("=" * 60)
        else:
            # game over
            print(ui.bad(f"\nGAME OVER {name}"))
            print(f"Current score: {score}")
            print(ui.info(f"Your highscore: {highscore}"))
            print("=" * 60)

            again = input("Play again? (yes/no): ").strip().lower()
            print()

            if again in ["yes", "y", "ja", "j"]:
                score = 0  # reset score, keep highscore
                continue
            return highscore


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

    print("=" * 60)
    print(f"Speed Mode – {time_limit_seconds} seconds for {name}")
    print("Answer as many questions as you can. Wrong answers do NOT end the game.")
    print("Clock is ticking... Good luck!\n")
    print("=" * 60)

    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        remaining = int(time_limit_seconds - elapsed)

        if remaining <= 0:
            print("\n⏰ Time's up!")
            break

        ui.print_round_header(
            "Speed Run",
            total_questions + 1,
            extra=f"⏳ Remaining time: {remaining} seconds"
        )

        # For now: no AI host in speed mode
        won = gameplay(
            pause_after=False,
            mode_name="Speed Run",
            score=score,
            remaining_time=remaining,
        )
        total_questions += 1

        if won:
            score += 1
            print(f"✅ Correct! Current Speed Score: {score}")
        else:
            print(f"❌ Wrong. Current Speed Score: {score}")

    print("\n" + "=" * 60)
    print(ui.header(f"Speed Mode finished, {name}!"))
    print(f"Correct answers: {score}")
    print(f"Total questions: {total_questions}")

    if total_questions > 0:
        accuracy = (score / total_questions) * 100
        print(f"Accuracy: {accuracy:.1f}%")
    else:
        print("No questions answered 🤷‍♂️")

    # update highscore
    if score > best_speed_score:
        print(f"\n🎉 New Speed Highscore! Old: {best_speed_score} → New: {score}")
        best_speed_score = score
    else:
        print(f"\nSpeed Highscore remains: {best_speed_score}")

    print("=" * 60)
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
    print(f"Game category: {random_game_category['label']}")
    print()
    print(f"A: {title1}\nB: {title2}\n")

    # player choice
    user_choice = ask_player_choice(random_game_category['question'])

    # determine correct option
    correct = check_correct_option(title1, title2, random_game_category)
    was_correct = user_choice.lower() == correct.lower()

    # result
    if was_correct:
        print(ui.good("Correct!"))
    else:
        print(ui.bad("False!"))

    print("=" * 60)
    print_answers(title1, title2, title1_info, title2_info)
    print("=" * 60)

    # ---- AI HOST COMMENTARY: ONLY FOR SUDDEN DEATH ----
    if mode_name == "Sudden Death":
        winner_title = title1 if correct == "A" else title2
        comment = host_comment(
            mode=mode_name,
            category_label=random_game_category["label"],
            title_a=title1,
            title_b=title2,
            winner=winner_title,
            was_correct=was_correct,
            score=score if score is not None else 0,
            remaining_time=remaining_time,
        )
        if comment:
            print()
            print(ui.info(comment))
            print()

    if pause_after:
        ui.wait_for_enter()

    return was_correct
