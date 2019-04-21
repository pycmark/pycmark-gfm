"""
    pycmark_gfm
    ~~~~~~~~~~~

    GitHub Flavored Markdown parser for docutils.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from typing import List, Type

from docutils import nodes
from docutils.transforms import Transform
from pycmark import CommonMarkParser
from pycmark.blockparser import BlockProcessor
from pycmark.blockparser.html_processors import StandardTagsHTMLBlockProcessor
from pycmark.inlineparser import InlineProcessor
from pycmark.readers import LineReader

from pycmark_gfm.blockparser.html_processors import (
    StandardTagsHTMLBlockProcessor as StandardTagsHTMLBlockProcessorEx
)
from pycmark_gfm.blockparser.table_processors import TableProcessor
from pycmark_gfm.inlineparser.std_processors import (
    DisallowedRawHTMLProcessor,
    StrikethroughProcessor,
    TaskListItemProcessor,
    WWWAutolinkProcessor,
    URLAutolinkProcessor,
    EmailAutolinkProcessor,
)
from pycmark_gfm.transforms import (
    DisallowedRawHTMLTransform,
    StrikethroughConverter,
    TaskListItemConverter,
)


class GFMParser(CommonMarkParser):
    """GitHub Flavored Markdown parser for docutils."""

    supported = ('markdown', 'md')

    def get_block_processors(self) -> List[Type[BlockProcessor]]:
        """Returns block processors. Overrided by subclasses."""
        processors = super().get_block_processors()
        processors.remove(StandardTagsHTMLBlockProcessor)
        processors.append(StandardTagsHTMLBlockProcessorEx)
        processors.append(TableProcessor)
        return processors

    def get_inline_processors(self) -> List[Type[InlineProcessor]]:
        """Returns inline processors. Overrided by subclasses."""
        processors = super().get_inline_processors()
        processors.append(DisallowedRawHTMLProcessor)
        processors.append(EmailAutolinkProcessor)
        processors.append(StrikethroughProcessor)
        processors.append(TaskListItemProcessor)
        processors.append(URLAutolinkProcessor)
        processors.append(WWWAutolinkProcessor)
        return processors

    def get_transforms(self) -> List[Type[Transform]]:
        transforms = super().get_transforms()
        transforms.append(DisallowedRawHTMLTransform)
        transforms.append(StrikethroughConverter)
        transforms.append(TaskListItemConverter)
        return transforms

    def parse(self, inputtext: str, document: nodes.document) -> None:
        """Parses a text and build document."""
        document.settings.inline_processors = self.get_inline_processors()
        reader = LineReader(inputtext.splitlines(True), source=document['source'])
        block_parser = self.create_block_parser()
        block_parser.parse(reader, document)
