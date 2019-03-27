from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()


setup(
    name='pycmark-gfm',
    version='0.9.0',
    url='https://github.com/tk0miya/pycmark-gfm',
    download_url='https://pypi.org/project/pycmark-gfm',
    license='Apache License 2.0',
    author='Takeshi KOMIYA',
    author_email='i.tkomiya@gmail.com',
    description='A GitHub Flavored Markdown parser for docutils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Documentation',
    ],
    platforms='any',
    python_requires=">=3.7",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pycmark>=0.9.3',
    ],
    extras_require={
        'test': [
            'tox',
            'flake8',
            'flake8-import-order',
            'pytest',
            'mypy',
            'html5lib',
        ],
    },
)
