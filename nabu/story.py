import yaml
from pathlib import Path
from jinja2 import Template
from weasyprint import HTML, CSS

class Story():

    def __init__(self, story_path, story_name, template_path, *args, **kwargs):
        self.template_path = template_path
        self.story_path = story_path
        self.story_name = story_name
    
    def render(self, outpath):
        with open(self.template_path, "story.html") as fp:
            story_template = Template(fp.read())
        
        with open(Path(self.story_path, self.story_name, "story.yaml")) as fp:
            story_data = yaml.load(fp, Loader=yaml.SafeLoader)

        story_html = story_template.render(
            title=story_data.title,
            author_name=story_data.author_name,
            author_contact=story_data.author_contact,
            pages=story_data.pages)
        
        
        # TODO: this bit

        style_obj = _get_style(style)
        html = self.to_html()
        h = HTML(string=html)
        c = CSS(string=style_obj.get_css(font_size))
        h.write_pdf(filename, stylesheets=[c, *style_obj.get_stylesheets()])


    
    