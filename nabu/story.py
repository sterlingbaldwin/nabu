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
        with open(self.template_path, "r") as fp:
            story_template = Template(fp.read())
        
        with open(Path(self.story_path, "story.yaml")) as fp:
            story_data = yaml.load(fp, Loader=yaml.SafeLoader)
        
        
        # import ipdb; ipdb.set_trace()

        story_html = story_template.render(
            title=story_data["title"],
            author_name=story_data["author_name"],
            author_contact=story_data["author_contact"],
            pages=story_data["pages"])
        
        style_string = self.get_style("default_working")
        h = HTML(string=story_html)
        h.write_pdf(outpath, stylesheets=[CSS(string=style_string)])
        # with open(outpath, 'w+b') as outstream:
        #     pisa.CreatePDF(
        #         story_html,
        #         dest=outstream)
        
        with open(str(outpath).replace('pdf', 'html'), 'w') as outstream:
            outstream.write(story_html)
    
    def get_style(self, style="default"):
        with open(Path("nabu", "styles", f"{style}.css")) as fp:
            return fp.read()


    
    