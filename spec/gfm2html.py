"""
    gfm2html
    ~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import html
import re
import sys

from docutils import nodes
from docutils.core import publish_string
from docutils.readers import standalone
from docutils.transforms import Transform
from docutils.transforms.misc import Transitions
from docutils.writers.html5_polyglot import Writer, HTMLTranslator
from pycmark.transforms import LinebreakFilter, SectionTreeConstructor

from pycmark_gfm import addnodes
from pycmark_gfm import Parser
from pycmark_gfm.inlineparser.std_processors import DisallowedRawHTMLProcessor
from pycmark_gfm.transforms import TaskListItemConverter


class HTMLWriter(Writer):
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = SmartHTMLTranslator

    def apply_template(self):
        subs = self.interpolation_dict()
        return subs.get('body')


class SmartHTMLTranslator(HTMLTranslator):
    special_characters = {
        ord('&'): '&amp;',
        ord('<'): '&lt;',
        ord('"'): '&quot;',
        ord('>'): '&gt;',
    }

    def __init__(self, document):
        super().__init__(document)
        self.in_strikethrough = False
        self.initial_header_level = 1

    def depart_Text(self, node):
        pos = node.parent.index(node)
        if isinstance(node.parent, nodes.list_item) and len(node.parent) > pos + 1:
            self.body.append('\n')

    def visit_paragraph(self, node):
        if not isinstance(node.parent, nodes.entry):
            self.body.append('<p>')

    def depart_paragraph(self, node):
        if not isinstance(node.parent, nodes.entry):
            self.body.append('</p>\n')

    def visit_section(self, node):
        self.section_level = node.get('depth', 1)

    def depart_section(self, node):
        self.section_level -= 1

    def visit_target(self, node):
        raise nodes.SkipNode

    def visit_transition(self, node):
        self.body.append(self.emptytag(node, 'hr'))

    def depart_colspec(self, node):
        pass

    def visit_row(self, node):
        self.body.append('\n<tr>\n')
        node.column = 0

    def depart_row(self, node):
        self.body.append('</tr>')

    def visit_entry(self, node):
        if 'align' in node:
            align = ' align="%s"' % node['align']
        else:
            align = ''

        if isinstance(node.parent.parent, nodes.thead):
            self.body.append('<th%s>' % align)
            self.context.append('</th>\n')
        else:
            self.body.append('<td%s>' % align)
            self.context.append('</td>\n')

    def visit_thead(self, node):
        self.body.append('<thead>')

    def depart_thead(self, node):
        self.body.append('\n</thead>')

    def visit_tbody(self, node):
        self.body.append('\n<tbody>')

    def depart_tbody(self, node):
        self.body.append('\n</tbody>')

    def depart_table(self, node):
        self.body.append('\n</table>\n')

    def visit_enumerated_list(self, node):
        if node.get('start') != 1:
            self.body.append('<ol start="%s">\n' % node['start'])
        else:
            self.body.append('<ol>\n')

    def visit_list_item(self, node):
        if len(node) == 0:
            self.body.append('<li>')
        elif isinstance(node[0], (nodes.Text, addnodes.checkbox)):
            self.body.append('<li>')
        else:
            self.body.append('<li>\n')

    def visit_literal(self, node):
        self.body.append('<code>')

    def depart_literal(self, node):
        self.body.append('</code>')

    def visit_inline(self, node):
        if 'strikethrough' in node['classes']:
            self.body.append('<del>')
        else:
            super().visit_inline(node)

    def depart_inline(self, node):
        if 'strikethrough' in node['classes']:
            self.body.append('</del>')
        else:
            super().depart_inline(node)

    def visit_literal_block(self, node):
        if len(node['classes']) > 1:
            self.body.append('<pre><code class="%s">' % html.escape(node['classes'][1]))
        else:
            self.body.append('<pre><code>')

    def depart_literal_block(self, node):
        self.body.append('</code></pre>\n')

    def visit_reference(self, node):
        atts = []
        if 'refuri' in node:
            atts.append('href="%s"' % html.escape(node['refuri']))
        else:
            atts.append('href="#%s"' % html.escape(node['refid']))
        if 'reftitle' in node:
            atts.append('title="%s"' % html.escape(node['reftitle']))
        self.body.append('<a %s>' % ' '.join(atts))

    def visit_image(self, node):
        atts = ['src="%s"' % html.escape(node['uri'])]
        if 'alt' in node:
            atts.append('alt="%s"' % html.escape(node['alt']))
        if 'title' in node:
            atts.append('title="%s"' % html.escape(node['title']))
        self.body.append('<img %s />' % ' '.join(atts))

    def visit_linebreak(self, node):
        self.body.append('<br />\n')

    def depart_linebreak(self, node):
        pass

    def visit_strikethrough(self, node):
        if self.in_strikethrough is False:
            self.body.append('<del>')
            self.in_strikethrough = True
        else:
            self.body.append('</del>')
            self.in_strikethrough = False

        raise nodes.SkipNode

    def visit_checkbox(self, node):
        if node['checked']:
            self.body.append('<input checked="" disabled="" type="checkbox">')
        else:
            self.body.append('<input disabled="" type="checkbox">')

        raise nodes.SkipNode


class TestReader(standalone.Reader):
    def get_transforms(self):
        transforms = super().get_transforms()
        transforms.remove(Transitions)
        return transforms


class DisabledRawHTMLTransform(Transform):
    default_priority = 201

    def apply(self, **kwargs):
        pattern = re.compile(DisallowedRawHTMLProcessor.DISALLOWED_TAGS)
        for text in list(self.document.findall(nodes.Text)):
            if pattern.match(text):
                html = '&lt;' + text[1:]
                text.parent.replace(text, nodes.raw('', html, format='html'))


class TestGFMParser(Parser):
    def get_transforms(self):
        transforms = super().get_transforms()
        transforms.remove(LinebreakFilter)
        transforms.remove(SectionTreeConstructor)
        transforms.remove(TaskListItemConverter)
        transforms.append(DisabledRawHTMLTransform)
        return transforms


def convert(source):
    html = publish_string(source=source,
                          source_path='dummy.md',
                          reader=TestReader(),
                          parser=TestGFMParser(),
                          writer=HTMLWriter(),
                          settings_overrides={'embed_stylesheet': False,
                                              'compact_lists': False,
                                              'doctitle_xform': False,
                                              'report_level': 999})
    return html.decode('utf-8')


if __name__ == '__main__':
    result = convert(sys.stdin.read().encode('utf-8'))
    if result:
        print(result)
