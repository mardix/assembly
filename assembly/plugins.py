# -*- coding: utf-8 -*-
"""
Assembly: plugins
"""

import os
import re
import markdown
from . import extends
from jinja2 import Markup
from jinja2.ext import Extension
from jinja2.nodes import CallBlock
from jinja2 import TemplateSyntaxError
from jinja2.lexer import Token, describe_token

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


@extends
def setup_markdown(app):
    app.jinja_env.add_extension(MarkdownTagExtension)
    app.jinja_env.add_extension(MarkdownExtension)

    app.jinja_env.filters.update({
        "markdown": lambda text: Markup(convert(text))
    })

# --------


"""
  -- jinja2-htmlcompress

    a Jinja2 extension that removes whitespace between HTML tags.

    Example usage:

      env = Environment(extensions=['htmlcompress_ext.HTMLCompress'])

    How does it work?  It throws away all whitespace between HTML tags
    it can find at runtime.  It will however preserve pre, textarea, style
    and script tags because this kinda makes sense.  In order to force
    whitespace you can use ``{{ " " }}``.

    Unlike filters that work at template runtime, this remotes whitespace
    at compile time and does not add an overhead in template execution.

    What if you only want to selective strip stuff?

      env = Environment(extensions=['htmlcompress_ext.SelectiveHTMLCompress'])

    And then mark blocks with ``{% strip %}``:

      {% strip %} ... {% endstrip %}

"""



gl_tag_re = re.compile(r'(?:<(/?)([a-zA-Z0-9_-]+)\s*|(>\s*))(?s)')
gl_ws_normalize_re = re.compile(r'[ \t\r\n]+')


class StreamProcessContext(object):
    def __init__(self, stream):
        self.stream = stream
        self.token = None
        self.stack = []

    def fail(self, message):
        raise TemplateSyntaxError(message, self.token.lineno, self.stream.name,
                                  self.stream.filename)


def _make_dict_from_listing(listing):
    rv = {}
    for keys, value in listing:
        for key in keys:
            rv[key] = value
    return rv


class HTMLCompress(Extension):
    isolated_elements = set(['script', 'style', 'noscript', 'textarea', 'pre'])
    void_elements = set(['br', 'img', 'area', 'hr', 'param', 'input',
                         'embed', 'col'])
    block_elements = set(['div', 'p', 'form', 'ul', 'ol', 'li', 'table', 'tr',
                          'tbody', 'thead', 'tfoot', 'tr', 'td', 'th', 'dl',
                          'dt', 'dd', 'blockquote', 'h1', 'h2', 'h3', 'h4',
                          'h5', 'h6'])
    breaking_rules = _make_dict_from_listing([
        (['p'], set(['#block'])),
        (['li'], set(['li'])),
        (['td', 'th'], set(['td', 'th', 'tr', 'tbody', 'thead', 'tfoot'])),
        (['tr'], set(['tr', 'tbody', 'thead', 'tfoot'])),
        (['thead', 'tbody', 'tfoot'], set(['thead', 'tbody', 'tfoot'])),
        (['dd', 'dt'], set(['dl', 'dt', 'dd']))
    ])

    def is_isolated(self, stack):
        for tag in reversed(stack):
            if tag in self.isolated_elements:
                return True
        return False

    def is_breaking(self, tag, other_tag):
        breaking = self.breaking_rules.get(other_tag)
        return breaking and (tag in breaking or (
        '#block' in breaking and tag in self.block_elements))

    def enter_tag(self, tag, ctx):
        while ctx.stack and self.is_breaking(tag, ctx.stack[-1]):
            self.leave_tag(ctx.stack[-1], ctx)
        if tag not in self.void_elements:
            ctx.stack.append(tag)

    def leave_tag(self, tag, ctx):
        if not ctx.stack:
            ctx.fail(
                'Tried to leave "%s" but something closed it already' % tag)
        if tag == ctx.stack[-1]:
            ctx.stack.pop()
            return
        for idx, other_tag in enumerate(reversed(ctx.stack)):
            if other_tag == tag:
                for num in range(idx + 1):
                    ctx.stack.pop()
            elif not self.breaking_rules.get(other_tag):
                break

    def normalize(self, ctx):
        pos = 0
        buffer = []

        def write_data(value):
            if not self.is_isolated(ctx.stack):
                value = gl_ws_normalize_re.sub(' ', value)
            buffer.append(value)

        for match in gl_tag_re.finditer(ctx.token.value):
            closes, tag, sole = match.groups()
            preamble = ctx.token.value[pos:match.start()]
            write_data(preamble)
            if sole:
                write_data(sole)
            else:
                buffer.append(match.group())
                (closes and self.leave_tag or self.enter_tag)(tag, ctx)
            pos = match.end()

        write_data(ctx.token.value[pos:])
        return ''.join(buffer)

    def filter_stream(self, stream):
        ctx = StreamProcessContext(stream)
        for token in stream:
            if token.type != 'data':
                yield token
                continue
            ctx.token = token
            value = self.normalize(ctx)
            yield Token(token.lineno, 'data', value)


class SelectiveHTMLCompress(HTMLCompress):
    def filter_stream(self, stream):
        ctx = StreamProcessContext(stream)
        strip_depth = 0
        while True:
            if stream.current.type == 'block_begin':
                if stream.look().test('name:strip') or stream.look().test(
                        'name:endstrip'):
                    stream.skip()
                    if stream.current.value == 'strip':
                        strip_depth += 1
                    else:
                        strip_depth -= 1
                        if strip_depth < 0:
                            ctx.fail('Unexpected tag endstrip')
                    stream.skip()
                    if stream.current.type != 'block_end':
                        ctx.fail(
                            'expected end of block, got %s' % describe_token(
                                stream.current))
                    stream.skip()
            if strip_depth > 0 and stream.current.type == 'data':
                ctx.token = stream.current
                value = self.normalize(ctx)
                yield Token(stream.current.lineno, 'data', value)
            else:
                yield stream.current
            next(stream)

@extends 
def setup_compress_html(app):
    if app.config.get("COMPRESS_HTML"):
        app.jinja_env.add_extension(HTMLCompress)
            