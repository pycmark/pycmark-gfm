"""
    test_blockparser_container
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_example_191():
    text = ("- a\n"
            " - b\n"
            "  - c\n"
            "   - d\n"
            "    - e\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, "a"],
                                                             [nodes.list_item, "b"],
                                                             [nodes.list_item, "c"],
                                                             [nodes.list_item, "d\n- e"])])
