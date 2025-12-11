import pygame

# Globale Flags
global music_enabled # Musik global ein/aus
music_enabled = True

def init_music():
    pygame.mixer.init()

def play_music(path, loop=True):
    if not music_enabled:
        return
    pygame.mixer.music.load("sounds/" + path + ".mp3")
    pygame.mixer.music.play(-1 if loop else 0)

def pause_music():
    if music_enabled:
        pygame.mixer.music.pause()

def resume_music():
    if music_enabled:
        pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()

def is_music_playing():
    return pygame.mixer.music.get_busy() and music_enabled

def toggle_music():
    """
    Globales Ein-/Ausschalten der Musik.
    Wenn ausgeschaltet, stoppt alles automatisch.
    """
    global music_enabled
    music_enabled = not music_enabled
    if not music_enabled:
        stop_music()
