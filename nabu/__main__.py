import os
import sys
import argparse
from pathlib import Path
from story import Story


def main():

    default_lib_path = Path(os.environ['PWD'], 'stories')
    default_story = "stormy_night"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--library', 
        default=default_lib_path,
        help=f"Path to library directory, default is {default_lib_path}")
    parser.add_argument(
        '-s', '--story', 
        default=default_story,
        help=f"The name of the story you would like to render, the default is the sample story 'stormy_night'")
    parser.add_argument(
        '-o', '--output',
        help=f"The path to where the output should be saved, default is {default_lib_path}/<STORY_NAME>.pdf")
    args = parser.parse_args()
    lib_path = Path(args.library)
    story_path = Path(lib_path, args.story)
    if not story_path.exists():
        print("The requested story does not exist")
        return -1
    if not Path(story_path, "story-cover.jpg").exists():
        print("The story doesnt have a cover page image")
        return -1
    if not Path(story_path, "story.yaml").exists():
        print("The story doesnt have its contents defined")
        return -1
    
    story = Story(story_path)
    story.render(args.story, args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
