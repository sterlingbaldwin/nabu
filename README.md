# Nabu
A python tool for writing interactive fiction. 

THIS IS A WORK IN PROGRESS AND MAY NOT WORK

## Design

Nabu uses Jinja templates to create an HTML document from the supplied story yaml file, and then renders it out to a PDF with internal links for the readers choices.

## Installation

first clone the repo

    git clone git@github.com:sterlingbaldwin/nabu.git

install dependencies

    pip install -r requirements.txt

install the package

    pip install -e .

## Story 

The story is described via a yaml document, with each page consisting of a block of content, and then a set of choices. Each story has three mandatory elements, a title page, a start page, and an end page. They should look something like:

    title:
        title: A Dark and Stormy Night
        author_name: Sterling Baldwin
        author_contact: https://github.com/sterlingbaldwin

    start:
        contents: "It was a dark and stormy night, the the waves beat themselves across the beach
            and the wind lashed my hair across my face. I could taste bitter salt dropplets from the ocean
            with a thousand microscopic sea creatures in my mouth."
        choices: 
            - 
                description: Where to next?
                target: first choice
    
    end:
        contents: "FIN"

The "title" will be the first page and link to the "start". The "start" page will be the entry point to the story, and any page without a "choices" section will link to the end page. 

The contents of the page can be either a single string, or a list of paragraphs. 

Each story should also have a "story-cover.jpg" file to use as the background of the title page.
