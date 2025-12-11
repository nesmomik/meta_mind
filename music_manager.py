import pygame


def init_music():
    pygame.mixer.init()
    set_volume(0.2)

def play_music(path, loop=False):
    pygame.mixer.music.load("sounds/"+path+".mp3")
    pygame.mixer.music.play(-1 if loop else 0)

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def set_volume(v):
    pygame.mixer.music.set_volume(v)  # 0.0 – 1.0

def stop_music():
    pygame.mixer.music.stop()

def is_music_playing():
    return pygame.mixer.music.get_busy()
