from typing import ChainMap
import yaml
from pathlib import Path
from jinja2 import Template
from weasyprint import HTML, CSS
# from xhtml2pdf import pisa

class Story():

    def __init__(self, story_path, story_name, template_path, *args, **kwargs):
        self.template_path = template_path
        self.story_path = story_path
        self.story_name = story_name
    
    def render(self, outpath):
        # first render the html
        with open(self.template_path, "r") as fp:
            story_template = Template(fp.read())
        
        with open(Path(self.story_path, "story.yaml")) as fp:
            story_data = yaml.load(fp, Loader=yaml.SafeLoader)

        # replace the image paths with the full path
        for chapter in story_data['chapters']:
            if 'image' in chapter:
                chapter['image'] = Path(self.story_path, chapter['image'])
            if 'mini_image' in chapter:
                chapter['mini_image'] = Path(self.story_path, chapter['mini_image'])
            for page in chapter['pages']:
                if 'image' in page:
                    page['image'] = Path(self.story_path, page['image'])

        story_html = story_template.render(
            cover_image=Path(self.story_path, story_data["cover_image"]),
            title=story_data["title"],
            author_name=story_data["author_name"],
            author_contact=story_data["author_contact"],
            chapters=story_data["chapters"])
        with open(Path(self.story_path, f"{self.story_name}.html"), 'w') as fp:
            fp.write(story_html)
        
        # now render the css
        css_path = Path("nabu", "styles", "default.css.jinja")
        with open(css_path, "r") as fp:
            css_template = Template(fp.read())
        
        story_css = css_template.render(
            chapters=story_data["chapters"])
        with open(Path(self.story_path, f"{self.story_name}.css"), 'w') as fp:
            fp.write(story_css)
        
        # finally, write out the pdf
        h = HTML(string=story_html)
        c = CSS(string=story_css)
        h.write_pdf(outpath, stylesheets=[c])



