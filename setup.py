from setuptools import setup

setup(
    name='phrasebook',
    version='0.1',
    py_modules=['phrasebook'],
    install_requires=[
        'click',
        'pyqt5',
        'qtawesome',
        'babel',
    ],
    entry_points='''
        [console_scripts]
        phrasebook=phrasebook.cli:main
    ''',
)
