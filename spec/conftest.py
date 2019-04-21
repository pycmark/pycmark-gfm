"""
    conftest
    ~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from urllib.request import urlopen
from xml.etree import ElementTree

import html5lib


BLACKLIST = [
    'example-140',
    'example-141',
    'example-142',
    'example-145',
    'example-147',
    'example-610',
    'example-616',
    'example-619',
    'example-620',
]


def pytest_generate_tests(metafunc):
    if 'gfmspec' in metafunc.fixturenames:
        gfmspec = fetch_gfmspec()
        metafunc.parametrize('gfmspec', list(gfmspec))


def fetch_gfmspec():
    def elem2code(elem):
        code = ElementTree.tostring(elem, encoding="utf-8", method="text").decode('utf-8')
        code = code.rstrip("\n")
        code = code.replace("→", "\t")
        return code

    with urlopen("https://github.github.com/gfm/") as f:
        document = html5lib.parse(f, transport_encoding=f.info().get_content_charset(),  # type: ignore
                                  namespaceHTMLElements=False)

    for example in document.findall('.//div[@class="example"]'):
        example_id = example.attrib['id']
        source = example.find('.//pre/code[@class="language-markdown"]')
        output = example.find('.//pre/code[@class="language-html"]')

        if example_id not in BLACKLIST:
            yield (example_id, elem2code(source) + "\n", elem2code(output))
