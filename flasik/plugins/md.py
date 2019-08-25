"""
A utils for Markdown

convert : render markdown to html
get_toc : Get the Table of Content
get_images: Return a list of images, can be used to extract the top image

"""

import os
import markdown
import flasik
from jinja2.nodes import CallBlock
from jinja2.ext import Extension
from jinja2 import Markup

# ------------------------------------------------------------------------------

class MarkdownTagExtension(Extension):
    """
    A simple extension for adding a {% markdown %}{% endmarkdown %} tag to Jinja

    <div> 
    {% markdown %}
        ## Hi
    {% endmarkdown %}
    </div>
    """
    tags = set(['markdown'])
    def __init__(self, environment):
        super(MarkdownTagExtension, self).__init__(environment)
        environment.extend(
            markdowner=markdown.Markdown(extensions=['extra'])
        )

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(
            ['name:endmarkdown'],
            drop_needle=True
        )
        return CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _markdown_support(self, caller):
        block = caller()
        block = self._strip_whitespace(block)
        return self._render_markdown(block)

    def _strip_whitespace(self, block):
        lines = block.split('\n')
        whitespace = ''
        output = ''

        if (len(lines) > 1):
            for char in lines[1]:
                if (char == ' ' or char == '\t'):
                    whitespace += char
                else:
                    break

        for line in lines:
            output += line.replace(whitespace, '', 1) + '\r\n'

        return output.strip()

    def _render_markdown(self, block):
        block = self.environment.markdowner.convert(block)
        return block

class MarkdownExtension(Extension):

    options = {}
    file_extensions = '.md'

    def preprocess(self, source, name, filename=None):
        if (not name or
           (name and not os.path.splitext(name)[1] in self.file_extensions)):
            return source
        return convert(source)

# Markdown
mkd = markdown.Markdown(extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.sane_lists',
    'markdown.extensions.toc'
])

def convert(text):
    '''
    Convert MD text to HTML
    :param text:
    :return:
    '''
    mkd.reset()
    return mkd.convert(text)


@flasik.extends
def setup(app):
    app.jinja_env.add_extension(MarkdownTagExtension)
    app.jinja_env.add_extension(MarkdownExtension)

    app.jinja_env.filters.update({
        "markdown": lambda text: Markup(convert(text))
    })

