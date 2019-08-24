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
from jinja2.ext import Extension
from jinja2.lexer import Token, describe_token
from jinja2 import TemplateSyntaxError
import re

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
