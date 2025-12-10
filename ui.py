import os
import time

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
    print(f"Game category: {category}")
    print()
    print(f"A: {title1}\nB: {title2}\n")


def print_answers(title1, title2, title1_info, title2_info):
    print("Answers:")
    print()
    print(f"{title1}: {title1_info}")
    print(f"{title2}: {title2_info}")


def print_header(mode, question_num=None, correct=None):
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

    if question_num and not correct:
        title = f"Question {question_num}"
        print(color("\n\t\t    ✦ " + title + " ✦\n", Colors.MAGENTA))

    if correct == True:
       print(color("\n\t\t    ✦ " + "Correct!" + " ✦\n", Colors.GREEN))
    elif correct == False:
       print(color("\n\t\t    ✦ " + "False!" + " ✦\n", Colors.RED))


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


def wait_for_key():
    """Pause until press of Enter key."""
    input("Press any key to continue!\n")


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
    print(r"""
                        _ _                _ 
   __ _  ___   ___   __| | |__  _   _  ___| |
  / _` |/ _ \ / _ \ / _` | '_ \| | | |/ _ \ |
 | (_| | (_) | (_) | (_| | |_) | |_| |  __/_|
  \__, |\___/ \___/ \__,_|_.__/ \__, |\___(_)
  |___/                         |___/        
      """)


def loading_line(message: str, steps: int = 5, delay: float = 0.25):
    """Simple fake loading animation."""
    print()
    for i in range(steps):
        dots = "." * (i + 1)
        print(f"  {message}{dots}", end="\r", flush=True)
        time.sleep(delay)
    print(f"  {message}{'.' * steps}")  # final line
    print()


def print_intro():
    """Print intro screen."""
    clear_screen()
    print_title()

    print("\n\n")
    print(f"  {Colors.BLUE}Welcome to meta_mind!{Colors.RESET}")
    print("\n\n")
    print("  Two articles. One duel. Live data in real time.")
    print("  Can you beat the high score? Find out.\n")

    loading_line("Loading featured articles")


def display_game_instructions():
    """Print game manual."""
    clear_screen()
    print_title()

    print(
        "\n  In meta_mind, two Wikipedia articles face off in a fast-paced metadata duel."
        "\n  You’ll see them side by side and choose which one wins in categories like"
        "\n  pageviews, size, age, edits, or internal links."
        "\n  Trust your instincts, make your pick, and then see how the data decides."
        "\n"
    )


def print_exit():
    """Print exit screen."""
    clear_screen()
    print_goodbye()
    print()
    print("Thank you for playing meta_mind.")
    print("See you in the knowledge arena again.\n")


def print_menu(sudden_death_hs: int = 0, speed_hs: int = 0):
    """Print the main meta_mind menu."""
    clear_screen()
    print_title()

    print(color("meta_mind main menu", Colors.BOLD))
    print()

    print(
        f"{color('1.', Colors.YELLOW)} Sudden Death      "
        f"{Colors.GREY}(Highscore: {sudden_death_hs}){Colors.RESET}"
    )
    print(
        f"{color('2.', Colors.YELLOW)} Speed Mode – 60s  "
        f"{Colors.GREY}(Highscore: {speed_hs}){Colors.RESET}"
    )
    print()
    print(f"{color('3.', Colors.CYAN)} Help")
    print(f"{color('4.', Colors.CYAN)} Highscore List")
    print(f"{color('5.', Colors.RED)} Quit")
    print()
