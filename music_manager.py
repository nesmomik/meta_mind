from audioplayer import AudioPlayer
import threading
import time

class MusicManager:
    def __init__(self):
        self.player = None
        self.thread = None
        self.playing_event = threading.Event()

    def play(self, track, loop=True):
        """Spielt eine MP3-Datei in Endlosschleife ab (loop=True)."""
        self.stop()  # alte Musik stoppen
        self.playing_event.set()

        def _play_thread():
            self.player = AudioPlayer(track)
            self.player.volume = 10
            self.player.play(loop=loop)
            while self.playing_event.is_set():
                time.sleep(0.1)
            self.player.stop()

        self.thread = threading.Thread(target=_play_thread, daemon=True)
        self.thread.start()

    def stop(self):
        """Stoppt die aktuelle Musik."""
        self.playing_event.clear()
        if self.thread and self.thread.is_alive():
            self.thread.join()
        self.player = None


music_manager = MusicManager()

def play_music(track = "", loop = True):
    music_manager.play(f"{track}.mp3", loop)

def stop_music():
    music_manager.stop()

# If we have enough time, implement sublte soundeffects!
# sound_effect_manager = MusicManager()