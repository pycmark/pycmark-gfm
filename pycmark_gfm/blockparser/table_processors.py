"""
    pycmark_gfm.blockparser.table_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Table processor classes for BlockParser.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from typing import Generator, List, Tuple

from docutils import nodes
from docutils.nodes import Element
from pycmark.blockparser import PatternBlockProcessor
from pycmark.readers import LineReader
from pycmark.utils import unescape


def align(delimiter: str) -> str:
    if delimiter.startswith(':') and delimiter.endswith(':'):
        return 'center'
    elif delimiter.startswith(':'):
        return 'left'
    elif delimiter.endswith(':'):
        return 'right'
    else:
        return None


def split_row(text: str) -> Generator[str, None, None]:
    i = 0
    while i < len(text):
        if text[i] == '|':
            yield unescape(text[0:i].strip())
            text = text[i + 1:]
            i = 0
        elif text[i] == '\\':
            i += 2
        else:
            i += 1

    if text:
        yield unescape(text.strip())


# 4.10 Tables
class TableProcessor(PatternBlockProcessor):
    priority = 750
    pattern = re.compile(r'^ {0,3}\S+')
    delimiter_pattern = re.compile(r'^ {0,3}(\|\s*)?:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$')
    sidewall_pattern = re.compile(r'^ {0,3}\|(.*)\|\s*$')

    def run(self, reader: LineReader, document: Element) -> bool:
        location = reader.get_source_and_line(incr=1)
        header_row, aligns = self.read_table_header(reader)
        if header_row is None:
            return False
        body_rows = self.read_table_body(reader, aligns)

        colspecs = [nodes.colspec('', colwidth=int(100 / len(aligns))) for _ in aligns]
        thead = nodes.thead('', header_row)
        tgroup = nodes.tgroup('', *colspecs, thead, cols=len(aligns))
        if body_rows:
            tgroup += nodes.tbody('', *body_rows)
        table = nodes.table('', tgroup)
        location.set_source_info(table)
        document += table
        return True

    def read_table_header(self, reader: LineReader) -> Tuple[nodes.row, List[str]]:
        try:
            location = reader.get_source_and_line(incr=1)
            header = self.parse_row(reader.readline())
            if self.parser.is_interrupted(reader):
                raise IOError
            elif not self.delimiter_pattern.match(reader.next_line):
                raise IOError

            delimiters = self.parse_row(reader.next_line)
            aligns = [align(d) for d in delimiters]
            if len(header) != len(delimiters):
                raise IOError
        except IOError:
            reader.step(-1)
            return None, None

        reader.step()

        row = nodes.row()
        for i, cell in enumerate(header):
            text = cell.strip()
            entry = nodes.entry()
            location.set_source_info(entry)
            if text:
                entry += nodes.paragraph(text, text)
            if aligns[i]:
                entry['align'] = aligns[i]
            row += entry
        return row, aligns

    def read_table_body(self, reader: LineReader, aligns: List[str]) -> List[nodes.row]:
        try:
            rows = []
            while True:
                if self.parser.is_interrupted(reader):
                    break
                else:
                    row = self.parse_row(reader.readline())
                    if len(row) == 1 and row[0] == '':
                        reader.step(-1)
                        break

                    entries = []
                    for i, align in enumerate(aligns):
                        try:
                            text = row[i].strip()
                        except IndexError:
                            text = ''

                        entry = nodes.entry()
                        if text:
                            entry += nodes.paragraph(text, text)
                        entry.source, entry.line = reader.get_source_and_line()
                        if align:
                            entry['align'] = align
                        entries.append(entry)
                    rows.append(nodes.row('', *entries))
        except IOError:
            pass

        return rows

    def parse_row(self, line: str) -> List[str]:
        line = self.sidewall_pattern.sub(r'\1', line)
        return list(split_row(line))
