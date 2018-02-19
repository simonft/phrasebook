from setuptools import setup

setup(
    name='phrasebook',
    version='0.1',
    py_modules=['phrasebook'],
    install_requires=[
        'click',
        'pyqt5',
        'pycryptodome',
    ],
    entry_points='''
        [console_scripts]
        phrasebook=phrasebook:main
    ''',
)
