import os
import time
from getkey import getkey

from music_manager import is_music_playing

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GREY = '\033[90m'


def separator(char: str = "-", length: int = 60) -> str:
    """Return a horizontal separator line."""
    return char * length


def color(text, color):
    return f"{color}{text}{Colors.RESET}"


def good(text):
    return color(text, Colors.GREEN)


def bad(text):
    return color(text, Colors.RED)


def warn(text):
    return color(text, Colors.YELLOW)


def info(text):
    return color(text, Colors.CYAN)


def header(text):
    return color(text, Colors.MAGENTA)

def print_question(category, title1, title2):
    print(f"  Game category: {Colors.CYAN}{category}{Colors.RESET}")
    print()
    print(f"    A: {title1}\n\n    B: {title2}\n\n\n")


def print_answers(category, title1, title2, title1_info, title2_info):
    print(f"  The data: {Colors.CYAN}{category}{Colors.RESET}")
    print()
    print(f"    A: {title1_info}\n")
    print(f"    B: {title2_info}\n\n")


def print_highscores(
        name,
        death_score,
        speed_score,
        max_death_score_name,
        max_speed_score_name,
        max_death_score_value,
        max_speed_score_value
        ):
    """Print the ascii art title (left aligned)."""
    clear_screen()

    title = r"""
  _     _       _
 | |__ (_) __ _| |__  ___  ___ ___  _ __ ___  ___ 
 | '_ \| |/ _` | '_ \/ __|/ __/ _ \| '__/ _ \/ __|
 | | | | | (_| | | | \__ \ (_| (_) | | |  __/\__ \
 |_| |_|_|\__, |_| |_|___/\___\___/|_|  \___||___/
          |___/
"""
    print(Colors.YELLOW + Colors.BOLD + title + Colors.RESET)

    print(color("\n\t\t ✦ 'user': " + name + " ✦", Colors.CYAN))

    print(f"  Your highscores:")
    print(f"  💥 Sudden Death: {death_score}")
    print(f"  🕑 Speed Mode Highscore: {speed_score}\n")
    print(f"  Total {Colors.YELLOW}highscores{Colors.RESET}:")
    print(f"  💥 Sudden Death: {max_death_score_value}"
          + f" ({Colors.YELLOW}{max_death_score_name}{Colors.RESET})")
    print(f"  🕑 Speed Mode Highscore: {max_speed_score_value}"
          + f" ({Colors.YELLOW}{max_speed_score_name}{Colors.RESET})")


def print_header(mode, question_num=None, correct=None, won=None):
    """
    Clear the screen and print a round header like:
    ✦ Sudden Death – Question 3 ✦
    """
    clear_screen()

    if mode == "Sudden Death":
        header = r"""
             _    _               _          _   _    
  ____  _ __| |__| |___ _ _    __| |___ __ _| |_| |_  
 (_-< || / _` / _` / -_) ' \  / _` / -_) _` |  _| ' \ 
 /__/\_,_\__,_\__,_\___|_||_|_\__,_\___\__,_|\__|_||_|
                           |___|                      
"""
    else:
        header = r"""
                         _                 _     
     ____ __  ___ ___ __| |  _ __  ___  __| |___ 
    (_-< '_ \/ -_) -_) _` | | '  \/ _ \/ _` / -_)
    /__/ .__/\___\___\__,_|_|_|_|_\___/\__,_\___|
       |_|               |___|                   
       """

    print(Colors.MAGENTA + Colors.BOLD + header + Colors.RESET)

    if question_num and correct is None and not mode == "Speed Mode" and won is None:
        title = f"Question {question_num}"
        print(color("\n\t\t    ✦ " + title + " ✦\n", Colors.MAGENTA))
        return

    if correct == True:
        print(color("\n\t\t  ✦ " + "✅ Correct Answer!" + " ✦\n", Colors.GREEN))
        if mode == "Speed Mode":
            print(f"  Current run Speed Score: {question_num}")
        return
    elif correct == False:
        print(color("\n\t\t  ✦ " + "❌ Wrong Answer!" + " ✦\n", Colors.RED))
        if mode == "Speed Mode":
            print(f"  Current Speed Score: {question_num}\n")
        return

    if won == False:
        print(color("\n\t\t    ✦ " + "Game Over!" + " ✦\n", Colors.RED))
    elif won == True:
        print(color("\n\t\t    ✦ " + "New Highscore!" + " ✦\n", Colors.YELLOW))





def print_round_header(mode, q_num=None, extra: str = ""):
    """
    Clear the screen and print a round header like:
    ✦ Sudden Death – Question 3 ✦
    """
    clear_screen()
    title = f"{mode} – Question {q_num}" if q_num else mode

    print()
    print(color("✦ " + title + " ✦", Colors.MAGENTA))
    if extra:
        print(extra)
    print("┈" * 60)
    print()


def print_message(message):
    """Prints a message after clearing the UI, with title on top."""
    clear_screen()
    print_title()
    print(f"\n\n\n  {message}\n\n\n")


def wait_for_any_key():
    """Pause until press of Enter key."""
    print("\n  Press any key to continue!\n")
    getkey()


def wait_for_enter():
    """Pause until press of Enter key."""
    input("\n  Press the Enter key to continue!\n")


def clear_screen():
    """Clears the terminal in Unix and Windows."""
    os.system("cls" if os.name == "nt" else "clear")


def print_title():
    """Print the ascii art title (left aligned)."""
    title = r"""
                 _                      _           _ 
  _ __ ___   ___| |_ __ _     _ __ ___ (_)_ __   __| |
 | '_ ` _ \ / _ \ __/ _` |   | '_ ` _ \| | '_ \ / _` |
 | | | | | |  __/ || (_| |   | | | | | | | | | | (_| |
 |_| |_| |_|\___|\__\__,_|___|_| |_| |_|_|_| |_|\__,_|
                        |_____|                       
"""
    print(Colors.MAGENTA + Colors.BOLD + title + Colors.RESET)


def print_goodbye():
    """Print the ascii art goodbye."""
    title = r"""
                        _ _                _ 
   __ _  ___   ___   __| | |__  _   _  ___| |
  / _` |/ _ \ / _ \ / _` | '_ \| | | |/ _ \ |
 | (_| | (_) | (_) | (_| | |_) | |_| |  __/_|
  \__, |\___/ \___/ \__,_|_.__/ \__, |\___(_)
  |___/                         |___/        
      """
    print(Colors.MAGENTA + Colors.BOLD + title + Colors.RESET)


def loading_line(message: str, steps: int = 5, delay: float = 0.1):
    """Simple fake loading animation."""
    for i in range(steps):
        dots = "." * (i + 1)
        print(f"  {message}{dots}", end="\r", flush=True)
        time.sleep(delay)
    print(f"  {message}{'.' * steps}")  # final line


def print_intro():
    """Print intro screen."""
    clear_screen()
    print_title()

    print("\n")
    print(f"  {Colors.BLUE}Welcome to meta_mind!{Colors.RESET}")
    print("\n")
    print("  Two articles. One duel. Live data in real time.")
    print(f"  Can you beat the {Colors.YELLOW}highscore{Colors.RESET}?\n")

    loading_line("Loading featured articles")


def display_game_instructions():
    """Print game manual."""
    clear_screen()
    print_title()

    print(
        "\n  In meta_mind, Two Wikipedia Featured Articles face"
        "\n  off in a fast-paced metadata duel. Choose the winner"
        "\n  in categories like pageviews, size, age, edit count"
        "\n  and more ...\n"
        "\n  Trust your instincts, make your pick, and then see how the "
        "\n  metadata decides!\n"
    )


def print_exit():
    """Print exit screen."""
    clear_screen()
    print_goodbye()
    print()
    print("\n\n  Thank you for playing meta_mind.")
    print("  See you again in the knowledge arena.\n\n\n")


def print_menu(sudden_death_hs: int = 0, speed_hs: int = 0):
    """Print the main meta_mind menu."""
    clear_screen()
    print_title()

    print(color("  main menu:", Colors.BOLD))
    print()

    print(
        f"  {color('1.', Colors.YELLOW)} Sudden Death      "
        f"{Colors.GREY}(Highscore: {sudden_death_hs}){Colors.RESET}"
    )
    print(
        f"  {color('2.', Colors.YELLOW)} Speed Mode – 60s  "
        f"{Colors.GREY}(Highscore: {speed_hs}){Colors.RESET}"
    )
    print()
    print(f"  {color('3.', Colors.CYAN)} Help")
    print(f"  {color('4.', Colors.CYAN)} Highscore List")
    print(f"  {color('5.', Colors.CYAN)} Music {'On' if is_music_playing() else 'Off'}")
    print(f"  {color('6.', Colors.RED)} Quit")
    print()
