# -*- coding: utf-8 -*-

from pprint import pprint
import re

import markdown
import mdx_linkify


def parse_to_markdown(markdown_text):
    """Parse Markdown text to HTML

    Arguments:
    markdown_text -- String to be parsed into HTML format
    """

    extensions_list = ['linkify','markdown.extensions.tables','markdown.extensions.fenced_code']

    try:
        parsed_text = markdown.markdown(markdown_text.decode('utf-8'), extensions=extensions_list)

    except (UnicodeEncodeError, UnicodeDecodeError) as encoding_error:
        parsed_text = markdown.markdown(markdown_text, extensions=extensions_list)

    return parsed_text


def get_links_from_description(description):
    """Find via regex all the links in a description string"""

   
    html_link_regex = re.compile(r"\<a href=\"(?P<linkRef>.*)\"\>(?P<linkText>[^\<]*)\</a>")

    links = []

    
    link_matches = html_link_regex.findall(description)
    if link_matches:
        for link_match in link_matches:
            link = {}
            link['title'] = link_match[1]
            link['url'] = link_match[0]

            links.append(link)

    return links


text = """ <http://autolink-in-abstract.com>.

ETC ETC ETC ETC ETC ETC ETC ETC ETC ETC http://link-with-quotes.com?id='&quotweird-id&quot' ETC ETC ETC"""

print parse_to_markdown(text)


pprint(get_links_from_description(parse_to_markdown(text)))
