"""
    pycmark_gfm
    ~~~~~~~~~~~

    GitHub Flavored Markdown parser for docutils.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from typing import List, Type

from docutils import nodes
from docutils.parsers import Parser
from docutils.transforms import Transform
from pycmark.blockparser import BlockParser, BlockProcessor
from pycmark.blockparser.container_processors import BlockQuoteProcessor
from pycmark.blockparser.html_processors import (
    ScriptHTMLBlockProcessor,
    CommentHTMLBlockProcessor,
    ProcessingInstructionHTMLBlockProcessor,
    DeclarationHTMLBlockProcessor,
    CdataHTMLBlockProcessor,
    CompleteTagsHTMLBlockProcessor,
)
from pycmark.blockparser.std_processors import (
    ThematicBreakProcessor,
    ATXHeadingProcessor,
    SetextHeadingProcessor,
    IndentedCodeBlockProcessor,
    BlankLineProcessor,
    BacktickFencedCodeBlockProcessor,
    TildeFencedCodeBlockProcessor,
    ParagraphProcessor,
)
from pycmark.inlineparser import InlineProcessor
from pycmark.inlineparser.link_processors import LinkOpenerProcessor
from pycmark.inlineparser.std_processors import (
    BackslashEscapeProcessor,
    CodeSpanProcessor,
    EmphasisProcessor,
    URIAutolinkProcessor,
    EmailAutolinkProcessor,
    RawHTMLProcessor,
    HardLinebreakProcessor,
    SoftLinebreakProcessor,
)
from pycmark.readers import LineReader
from pycmark.transforms import (
    TightListsDetector,
    TightListsCompactor,
    BlanklineFilter,
    LinebreakFilter,
    SectionTreeConstructor,
    InlineTransform,
    SparseTextConverter,
    EmphasisConverter,
    BracketConverter,
    TextNodeConnector,
)

from pycmark_gfm.blockparser.container_processors import (
    BulletListProcessor,
    NonEmptyBulletListProcessor,
    OrderedListProcessor,
    OneBasedOrderedListProcessor,
)
from pycmark_gfm.blockparser.html_processors import StandardTagsHTMLBlockProcessor
from pycmark_gfm.blockparser.table_processors import TableProcessor
from pycmark_gfm.inlineparser.link_processors import LinkCloserProcessor
from pycmark_gfm.inlineparser.std_processors import (
    DisallowedRawHTMLProcessor,
    EntityReferenceProcessor,
    StrikethroughProcessor,
    TaskListItemProcessor,
    WWWAutolinkProcessor,
    URLAutolinkProcessor,
    EmailAutolinkProcessor as ExtendedEmailAutolinkProcessor,
)
from pycmark_gfm.transforms import (
    DisallowedRawHTMLTransform,
    LinkReferenceDefinitionDetector,
    StrikethroughConverter,
    TaskListItemConverter,
)


class GFMParser(Parser):
    """GitHub Flavored Markdown parser for docutils."""

    supported = ('markdown', 'md')

    def get_block_processors(self) -> List[Type[BlockProcessor]]:
        """Returns block processors. Overrided by subclasses."""
        return [
            ThematicBreakProcessor,
            ATXHeadingProcessor,
            SetextHeadingProcessor,
            IndentedCodeBlockProcessor,
            BlankLineProcessor,
            BacktickFencedCodeBlockProcessor,
            TildeFencedCodeBlockProcessor,
            ScriptHTMLBlockProcessor,
            CommentHTMLBlockProcessor,
            ProcessingInstructionHTMLBlockProcessor,
            DeclarationHTMLBlockProcessor,
            CdataHTMLBlockProcessor,
            StandardTagsHTMLBlockProcessor,
            CompleteTagsHTMLBlockProcessor,
            BlockQuoteProcessor,
            BulletListProcessor,
            NonEmptyBulletListProcessor,
            OrderedListProcessor,
            OneBasedOrderedListProcessor,
            TableProcessor,
            ParagraphProcessor,
        ]

    def get_inline_processors(self) -> List[Type[InlineProcessor]]:
        """Returns inline processors. Overrided by subclasses."""
        return [
            BackslashEscapeProcessor,
            EntityReferenceProcessor,
            CodeSpanProcessor,
            EmphasisProcessor,
            TaskListItemProcessor,
            LinkOpenerProcessor,
            LinkCloserProcessor,
            URIAutolinkProcessor,
            EmailAutolinkProcessor,
            DisallowedRawHTMLProcessor,
            RawHTMLProcessor,
            HardLinebreakProcessor,  # TODO: docutils does not support hardline break
            SoftLinebreakProcessor,
            StrikethroughProcessor,
            WWWAutolinkProcessor,
            URLAutolinkProcessor,
            ExtendedEmailAutolinkProcessor,
        ]

    def get_transforms(self) -> List[Type[Transform]]:
        return [
            TightListsDetector,
            TightListsCompactor,
            BlanklineFilter,
            LinebreakFilter,
            SectionTreeConstructor,
            LinkReferenceDefinitionDetector,
            InlineTransform,
            SparseTextConverter,
            EmphasisConverter,
            StrikethroughConverter,
            BracketConverter,
            TextNodeConnector,
            TaskListItemConverter,
            DisallowedRawHTMLTransform,
        ]

    def create_block_parser(self) -> BlockParser:
        """Creates a block parser and returns it.

        Internally, ``get_block_processors()`` is called to create a parser.
        So you can change the processors by subclassing.
        """
        parser = BlockParser()
        for processor in self.get_block_processors():
            parser.add_processor(processor(parser))
        return parser

    def parse(self, inputtext: str, document: nodes.document) -> None:
        """Parses a text and build document."""
        document.settings.inline_processors = self.get_inline_processors()
        reader = LineReader(inputtext.splitlines(True), source=document['source'])
        block_parser = self.create_block_parser()
        block_parser.parse(reader, document)
