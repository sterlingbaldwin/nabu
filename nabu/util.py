from pathlib import Path
from enum import Enum


class Speed(Enum):
    fast = 10
    medium = 20
    slow = 30


def load_story(library_path, story_name):
    story = Story(Path(library_path, story_name))
    return story

def choice(options: list):
    while True:
        invalid = False
        print('\n')
        for idx, option in enumerate(options):
            print(f"\t{idx + 1}: {option['option']}")
        selection = input(f"\npick an option: " )
        if selection == 'q':
            return -1
        else:
            try:
                selection = int(selection)
            except:
                invalid = True
                continue
            if selection > len(options):
                invalid = True
        
        if invalid:
            print(f"You choose {selection}, but valid choices are {' '.join(str(i+1) for i, _ in enumerate(options))}")
        else:
            return options[selection-1]['target']

def clear_screen():
    print("\033[H\033[J")

from nabu.story import Story