"""Parse arguments."""
import argparse

from celestine.keyword.main import CELESTINE


from celestine.keyword.main import LANGUAGE
from celestine.keyword.main import language

from celestine.keyword.main import PYTHON
from celestine.keyword.main import python

from celestine.keyword.main import APPLICATION
from celestine.keyword.main import application


parser = argparse.ArgumentParser(prog=CELESTINE)

parser.add_argument(
    APPLICATION,
    choices=application,
    help="Tell me which python version you are using.",
    nargs="?"
)

parser.add_argument(
    "-l, --language",
    choices=language,
    help="Choose a language.",
    dest=LANGUAGE,
)


parser.add_argument(
    "-v, --version",
    choices=python,
    help="Tell me which python version you are using.",
    dest=PYTHON,
)


parser.add_argument(
    "_",
    nargs="*",
)