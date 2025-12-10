import os
import shutil
from subprocess import call
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

def center(text: str) -> str:
    """Return the text centered based on current terminal width."""
    try:
        width = shutil.get_terminal_size().columns
    except OSError:
        width = 80
    return text.center(width)


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

def print_round_header(mode, q_num=None, extra=""):
    clear_screen()
    title = f"{mode} – Question {q_num}" if q_num else mode

    print()
    print(center(color("✦ " + title + " ✦", Colors.MAGENTA)))
    print(center("┈" * 60))
    print()




def print_message(message):
    """prints message in the middle of the ui"""
    clear_screen()
    print_title()

    print(f"\n\n  {message}\n\n\n")


def wait_for_enter():
    """pause until press of enter key"""
    input("  Press the Enter key to continue!\n")


def clear_screen():
    """empties the terminal in unix and windows"""
    os.system("cls" if os.name == "nt" else "clear")


def print_title():
    """print the ascii art title"""
    title = r"""
                 _                      _           _ 
  _ __ ___   ___| |_ __ _     _ __ ___ (_)_ __   __| |
 | '_ ` _ \ / _ \ __/ _` |   | '_ ` _ \| | '_ \ / _` |
 | | | | | |  __/ || (_| |   | | | | | | | | | | (_| |
 |_| |_| |_|\___|\__\__,_|___|_| |_| |_|_|_| |_|\__,_|
                        |_____|                       
"""
    for line in title.splitlines():
        if line.strip():
            print(center(Colors.MAGENTA + Colors.BOLD + line + Colors.RESET))
        else:
            print()
    print()



def print_goodbye():
    """print the ascii art goodbye"""
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
    """print intro screen"""
    clear_screen()
    print_title()

    print(f"  {Colors.BLUE}Welcome to meta_mind{Colors.RESET}")
    print("  Two articles. One duel. Live data in real time.")
    print("  Can you beat the high score? Find out.\n")

    loading_line("Loading featured articles")

    #print("  Loading Featured Articles List ...\n")



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
    """print exit screen"""
    clear_screen()
    print_goodbye()
    print()
    print(center("Thank you for playing meta_mind."))
    print(center("See you in the knowledge arena again.\n"))



def print_menu(sudden_death_hs: int = 0, speed_hs: int = 0):
    """print the main meta_mind menu"""
    clear_screen()
    print_title()

    print(center(color("meta_mind main menu", Colors.BOLD)))
    print()

    print(center(
        f"{color('1.', Colors.YELLOW)} Sudden Death      "
        f"{Colors.GREY}(Highscore: {sudden_death_hs}){Colors.RESET}"
    ))
    print(center(
        f"{color('2.', Colors.YELLOW)} Speed Mode – 60s  "
        f"{Colors.GREY}(Highscore: {speed_hs}){Colors.RESET}"
    ))
    print()
    print(center(f"{color('3.', Colors.CYAN)} Help"))
    print(center(f"{color('4.', Colors.CYAN)} Highscore List"))
    print(center(f"{color('5.', Colors.RED)} Quit"))
    print()



