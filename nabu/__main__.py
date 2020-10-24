import os
import sys
import argparse
from pathlib import Path
from nabu.util import load_story, choice, clear_screen


def load_library(library_path: Path):
    """return the set of stories available"""
    print("Select a story from your library")
    stories = []
    for story in library_path.iterdir():
        stories.append(Path(library_path, story))
    return stories


def main():

    default_lib_path = Path(os.environ['PWD'], 'stories')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--library', help=f"Path to library directory, default is {default_lib_path}", default=default_lib_path)
    args = parser.parse_args()
    lib_path = Path(args.library)

    clear_screen()
    stories = []
    for story in load_library(lib_path):
        stories.append({
            'option': story.name,
            'target': story
        })

    selection = choice(stories)
    if selection == -1:
        print("Exiting")
        return 0
    
    story = load_story(lib_path, selection)
    story.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
