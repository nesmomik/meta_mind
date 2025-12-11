import time
from getkey import getkey

import data_handler
import storage_handler
import ui
import game_logic
from music_manager import *

def main():

    init_music()
    play_music("menu")

    # Intro-Bildschirm
    ui.print_intro()
    # initialising featured article data
    data_handler.get_featured_articles()
    ui.wait_for_any_key()

    ui.clear_screen()
    ui.print_title()
    name = game_logic.ask_user_for_name()
    ui.print_message(f"  👋 Welcome, {name}! 👋")
    time.sleep(1)

    # try to get high scores for user
    high_scores = storage_handler.get_user_high_scores(name)
    # if no high_scores yet, initialize them
    if not high_scores:
        storage_handler.init_user_high_scores(name)
        high_scores = storage_handler.get_user_high_scores(name)

    while True:
        # Menü anzeigen
        ui.clear_screen()
        ui.print_menu(high_scores["death"], high_scores["speed"])
        print("  👉 Choose an option (1–6): ")
        choice = getkey()

        if choice == "1":
            # Sudden Death Mode – gibt neuen Highscore zurück
            play_music("sudden_death")
            high_scores["death"] = game_logic.sudden_death(name, high_scores["death"])
            storage_handler.update_user_high_score(name, high_scores)
            ui.wait_for_any_key()
            play_music("menu")

        elif choice == "2":
            # Speed Mode: so viele Fragen wie möglich in gegebener Zeit
            play_music("speedmode", False)
            high_scores["speed"] = game_logic.speed_mode(name, high_scores["speed"])
            storage_handler.update_user_high_score(name, high_scores)
            ui.wait_for_any_key()
            play_music("menu")

        elif choice == "3":
            # Help / Anleitung
            ui.display_game_instructions()
            ui.wait_for_any_key()

        elif choice == "4":
            # Highscore-Liste anzeigen
            all_scores = storage_handler.get_all_high_scores()
            max_death_score_name = max(all_scores, key=lambda k: all_scores[k]["death"])
            max_death_score_value = all_scores[max_death_score_name]["death"]
            max_speed_score_name = max(all_scores, key=lambda k: all_scores[k]["speed"])
            max_speed_score_value = all_scores[max_speed_score_name]["speed"]

            ui.print_highscores(
                name,
                high_scores['death'],
                high_scores['speed'],
                max_death_score_name,
                max_speed_score_name,
                max_death_score_value,
                max_speed_score_value
            )
            ui.wait_for_any_key()
        elif choice == "5":
            toggle_music()
            if music_enabled:
                play_music("menu")

        elif choice == "6":
            stop_music()
            ui.print_exit()
            break

        else:
            ui.print_message("❌ Invalid choice. Please select 1–5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()