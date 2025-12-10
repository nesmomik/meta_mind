import random
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
    ui.wait_for_enter()

    ui.clear_screen()
    ui.print_title()
    name = game_logic.ask_user_for_name()
    ui.print_message(f"👋 Welcome, {name}! 👋")
    ui.wait_for_enter()

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
        choice = input("👉 Choose an option (1–5): ").strip()

        if choice == "1":
            pause_music()
            # Sudden Death Mode – gibt neuen Highscore zurück
            # play_music("sudden_death")
            high_scores["death"] = functions.sudden_death(name, high_scores["death"])
            storage_handler.update_user_high_score(name, high_scores)
            ui.wait_for_enter()
            resume_music()

        elif choice == "2":
            pause_music()
            # Speed Mode: so viele Fragen wie möglich in gegebener Zeit
            # play_music("speedmode")
            high_scores["speed"] = functions.speed_mode(name, high_scores["speed"])
            storage_handler.update_user_high_score(name, high_scores)
            ui.wait_for_enter()
            resume_music()

        elif choice == "3":
            # Help / Anleitung
            ui.display_game_instructions()
            ui.wait_for_enter()

        elif choice == "4":
            # Highscore-Liste anzeigen
            msg = (
                f"\n💥 Sudden Death Highscore: {high_scores['death']} by {name}"
                f"\n🕑 Speed Mode Highscore:   {high_scores['speed']} by {name}"
            )
            ui.print_message(msg)
            ui.wait_for_enter()

        
        elif choice == "5":
            if is_music_playing():
                pause_music()
            else:
                resume_music()
            ui.print_exit()

        elif choice == "6":
            stop_music()
            ui.print_exit()
            break

        else:
            ui.print_message("❌ Invalid choice. Please select 1–5.")
            ui.wait_for_enter()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()