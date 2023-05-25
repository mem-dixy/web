"""Run a bunch of auto formaters."""

import io

from celestine import load
from celestine.file import (
    normalize,
    open_file_stream,
    save_file,
)
from celestine.load import directory
from celestine.package import run


def clean(**star):
    """"""
    print("clean start")
    run("pyupgrade")
    run("pydocstringformatter")
    run("autoflake")
    run("isort")
    run("black")
    print("clean finish")


def licence(**star):
    """"""
    location = load.pathway("licence")
    files = directory.file(location, [], ["cascadia_code_en.txt"])
    for file in files:
        string = io.StringIO()
        lines = open_file_stream(file)
        for line in lines:
            character = normalize.character(line)
            wrap = normalize.wrap_text(character)
            for text in wrap:
                string.write(text)
        save_file(string.getvalue(), file)
