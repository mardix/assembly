"""
Custom Jinja filters
"""
import re
from jinja2 import Markup
from . import md
from flask import url_for
import humanize
import arrow
from flasik import (init_app,
                     config,
                     format_datetime,
                     utils)


def nl2br(s):
    """
    {{ s | nl2br }}

    Convert newlines into <p> and <br />s.
    """
    if not isinstance(s, basestring):
        s = str(s)
    s = re.sub(r'\r\n|\r|\n', '\n', s)
    paragraphs = re.split('\n{2,}', s)
    paragraphs = ['<p>%s</p>' % p.strip().replace('\n', '<br />') for p in
                  paragraphs]
    return '\n\n'.join(paragraphs)


def oembed(url, class_=""):
    """
    Create OEmbed link

    {{ url | oembed }}
    :param url:
    :param class_:
    :return:
    """
    o = "<a href=\"{url}\" class=\"oembed {class_}\" ></a>".format(url=url,
                                                                   class_=class_)
    return Markup(o)


def img_src(url, class_="", responsive=False, lazy_load=False, id_=""):
    """
    Create an image src

    {{ xyz.jpg | img_src }}

    :param url:
    :param class_:
    :param responsive:
    :param lazy_load:
    :param id_:
    :return:
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = static_url(url)

    data_src = ""
    if responsive:
        class_ += " responsive"
    if lazy_load:
        data_src = url
        # 1x1 image
        url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
        class_ += " lazy"

    img = "<img src=\"{src}\" class=\"{class_}\" id=\"{id_}\" data-src={data_src}>" \
        .format(src=url, class_=class_, id_=id_, data_src=data_src)
    return Markup(img)


def static_url(url):
    """
    {{ url | static }}
    :param url:
    :return:
    """
    return url_for('static', filename=url)


FILTERS = {
    "slug": utils.slugify,  # slug
    "int_comma": humanize.intcomma,  # Transform an int to comma
    "strip_decimal": lambda d: d.split(".")[0],
    "markdown": lambda text: Markup(md.html(text)),  # Return a markdown to HTML
    "nl2br": nl2br,
    "format_datetime": format_datetime,
    "time_since": lambda dt: format_datetime(dt, False).humanize(),
    "oembed": oembed,
    "img_src": img_src,
    "static": static_url
}


def jinja_helpers(app):
    app.jinja_env.filters.update(FILTERS)


init_app(jinja_helpers)
