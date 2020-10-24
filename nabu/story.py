import yaml
import queue
import sys
import threading
from time import sleep

from pathlib import Path
import sounddevice as sd
import soundfile as sf
from pynput import keyboard

from nabu.util import clear_screen, choice, Speed


# key_event = threading.Event()
# def on_press(key):
#     print(f'got a key: {key}')

class Story():

    def __init__(self, story_path, *args, **kwargs):
        self.story_path = story_path
        pages_path = Path(story_path, 'story.yaml')
        if not pages_path.exists():
            raise ValueError(f"The story pages dont exist at location {pages}")
        
        with open(pages_path, 'r') as instream:
            self.pages = yaml.safe_load(instream)
        
        missing_sounds = []
        for page in self.pages.keys():
            if self.pages[page].get('sound'):
                sound_path = Path(story_path, 'sounds', self.pages[page]['sound'])
                if not sound_path.exists():
                    missing_sounds.append(self.pages[page]['sound'])
        
        if missing_sounds:
            print("missing the following sounds:")
            for sound in missing_sounds:
                print(f"\t{sound}")
            print("")
            raise ValueError("missing sounds")

        self.current_page = None
        self.choices = []
        
        self.sound_output_device = sd.query_hostapis()[0]['default_output_device']
        
        # self.key_listener = keyboard.Listener(
        #     on_press=on_press)
        # self.key_listener.start()
        return
    
    def key_press(self, key):
        import ipdb; ipdb.set_trace()
        pass
    
    def start(self):
        # TODO: Add nice title screen
        self.current_page = 'title'
        self.choices = []
        self.read_page(self.current_page)
        return
    
    def read_page(self, pagename):
        clear_screen()
        page = self.pages[pagename]
        text_speed = page.get('text_speed')
        if text_speed:
            text_speed = Speed[text_speed].value
        
        sound_speed = page.get('sound_speed')
        sound = page.get('sound')
        # if sound:
        #     sound_path = Path(self.story_path, 'sounds', sound)
        #     sound_thread = threading.Thread(target=self.play_sound, args=(sound_path))
            # self.play_sound()
        
        for char in page['contents']:
            print(char, end="", flush=True)
            if text_speed:
                sleep(text_speed/1000)
        
        if page.get('choices'):
            selection = choice(page['choices'])
        else:
            i = input("\n\nContinue")
            selection = page['goto']
        if selection == -1:
            return
        self.read_page(selection)
        return
    
    def goto_page(self, pagename):
        return
    
    def play_sound(self, filename):
        print("starting playback")
        buffersize = 20
        blocksize = 2048
        q = queue.Queue(maxsize=buffersize)
        event = threading.Event()

        def callback(outdata, frames, time, status):
            assert frames == blocksize
            if status.output_underflow:
                print('Output underflow: increase blocksize?')
                raise sd.CallbackAbort
            assert not status
            try:
                data = q.get_nowait()
            except queue.Empty as e:
                print('Buffer is empty: increase buffersize?')
                raise sd.CallbackAbort from e
            if len(data) < len(outdata):
                outdata[:len(data)] = data
                outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
                raise sd.CallbackStop
            else:
                outdata[:] = data

        try:
            while True:
                with sf.SoundFile(filename) as f:
                    for _ in range(buffersize):
                        data = f.buffer_read(blocksize, dtype='float32')
                        if not data:
                            break
                        q.put_nowait(data)  # Pre-fill queue
                    stream = sd.RawOutputStream(
                        samplerate=f.samplerate, blocksize=blocksize,
                        device=self.sound_output_device, channels=f.channels, dtype='float32',
                        callback=callback, finished_callback=event.set)
                    with stream:
                        timeout = blocksize * buffersize / f.samplerate
                        while data:
                            data = f.buffer_read(blocksize, dtype='float32')
                            q.put(data, timeout=timeout)
                        event.wait()  # Wait until playback is finished
        except KeyboardInterrupt:
            sys.exit(1)
        except queue.Full:
            # A timeout occurred, i.e. there was an error in the callback
            sys.exit(1)
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))
            sys.exit(1)