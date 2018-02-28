from setuptools import setup
from setuptools.command.sdist import sdist

NAME = 'phrasebook'
DESCRIPTION = 'Multilingual desktop application for generating secure passphrases using a wordlist.'
URL = 'https://github.com/simonft/phrasebook'
EMAIL = 'simonft@riseup.net'
AUTHOR = 'Simon Fondrie-Teitler'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1-dev'

REQUIRED = [
    'click',
    'pyqt5',
]


class Sdist(sdist):
    """Custom ``sdist`` command to ensure that mo files are always created."""
    def run(self):
        self.run_command('compile_catalog')
        sdist.run(self)


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['phrasebook'],
    install_requires=REQUIRED,
    cmdclass={'sdist': Sdist},
    extras_require={
        'dev': [
            'babel',
        ]
    },
    entry_points={
        'console_scripts': [
            'phrasebook=phrasebook.cli:main'
        ]
    },
    package_data={
        'phrasebook': ['wordlists/*.txt', 'images/*'],
    },
    license='GPLv3+',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
