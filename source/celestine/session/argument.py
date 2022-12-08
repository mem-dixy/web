""""""

from celestine.text.unicode import NONE

import sys
import dataclasses
import argparse
import types
import typing
import enum


from celestine.session import load

from celestine.text import CELESTINE
from celestine.text import VERSION_NUMBER

from celestine.text.directory import APPLICATION
from celestine.text.directory import INTERFACE
from celestine.text.directory import LANGUAGE

from celestine.text.session import HELP
from celestine.text.session import STORE_TRUE
from celestine.text.session import VERSION


from celestine.text.unicode import HYPHEN_MINUS
from celestine.text.unicode import QUESTION_MARK

from celestine.session.configuration import Configuration

CONFIGURATION = "configuration"

# action
EN = "en"
VIEWER = "viewer"
MAIN = "main"


""""""


""""""


class Hats(enum.Enum):
    Optional = enum.auto()
    YES = enum.auto()


@dataclasses.dataclass
class Cats():
    """"""

    hats: Hats
    default: str
    description: str


@dataclasses.dataclass
class Attribute():
    """"""


class Argument():
    """"""

    @staticmethod
    def flag(
        name: str
    ) -> str:
        """name = -n"""

        iterable = (HYPHEN_MINUS, name[0])
        return str().join(iterable)

    @staticmethod
    def name(
        name: str
    ) -> str:
        """name = --name"""

        iterable = (HYPHEN_MINUS, HYPHEN_MINUS, name)
        return str().join(iterable)

    def __init__(
        self,
        args: list[str],
        exit_on_error: bool
    ) -> None:
        """"""

        parser = argparse.ArgumentParser(
            add_help=False,
            exit_on_error=exit_on_error,
        )

        parser.add_argument(
            APPLICATION,
            nargs=QUESTION_MARK,
        )

        parser.add_argument(
            self.flag(LANGUAGE),
            self.name(LANGUAGE),
        )

        (argument, _) = parser.parse_known_args(args)

        configuration = Configuration.make()

        override = argument.application
        database = configuration.get(CELESTINE, APPLICATION)
        fallback = "__init__"
        application = override or database or fallback

        override = argument.language
        database = configuration.get(CELESTINE, LANGUAGE)
        fallback = "__init__"
        language = override or database or fallback

        language = load.module_fallback(LANGUAGE, argument.language)

        #(application, language) = self.essential(args, exit_on_error)

        self.dictionary: typing.Dict[str, str] = {}
        self.parser = argparse.ArgumentParser(
            add_help=False,
            prog=CELESTINE,
            exit_on_error=exit_on_error,
        )

        # FLAGS WITH NO PARAMETER
        self.information = self.parser.add_argument_group(
            title=language.ARGUMENT_INFORMATION_TITLE,
            description=language.ARGUMENT_INFORMATION_DESCRIPTION,
        )

        self.override = self.parser.add_argument_group(
            title=language.ARGUMENT_OVERRIDE_TITLE,
            description=language.ARGUMENT_OVERRIDE_DESCRIPTION,
        )

        self.positional = self.parser.add_argument_group(
            title=language.ARGUMENT_OVERRIDE_TITLE + "MOO",
            description=language.ARGUMENT_OVERRIDE_DESCRIPTION + "COW",
        )

        self.optional = self.parser.add_argument_group(
            title=language.ARGUMENT_OVERRIDE_TITLE + "MOO",
            description=language.ARGUMENT_OVERRIDE_DESCRIPTION + "COW",
        )

        self.information.add_argument(
            self.flag(CONFIGURATION),
            self.name(CONFIGURATION),
            action=STORE_TRUE,
            help=language.ARGUMENT_HELP_HELP,
        )

        self.information.add_argument(
            self.flag(HELP),
            self.name(HELP),
            action=HELP,
            help=language.ARGUMENT_HELP_HELP,
        )

        self.information.add_argument(
            self.flag(VERSION),
            self.name(VERSION),
            action=VERSION,
            help=language.ARGUMENT_VERSION_HELP,
            version=VERSION_NUMBER,
        )

        self.add_override(
            INTERFACE,
            language.ARGUMENT_INTERFACE_HELP,
            load.argument_default(INTERFACE),
            load.argument(INTERFACE),
        )

        self.add_override(
            LANGUAGE,
            language.ARGUMENT_LANGUAGE_HELP,
            EN,
            load.argument(LANGUAGE),
        )

        self.add_positional(
            APPLICATION,
            "Choose an applicanion. They have more option.",
            load.argument_default(APPLICATION),
            load.argument(APPLICATION),
        )

        self.add_positional(
            MAIN,
            "Choose an applicanion. They have more option.",
            MAIN,
            [MAIN],
            #            load.argument(APPLICATION, application),
        )

        attribute = load.module(APPLICATION, application).attribute
        dictionary: typing.Dict[str, Cats] = {}

        for (name, cats) in attribute.items():
            match cats.hats:
                case Hats.Optional:
                    self.add_optional(
                        name,
                        cats.description,
                        cats.default,
                    )

        self.attribute = Attribute()
        self.new_attribute = self.attribute

        # combine this with argument
        parse_args = self.parser.parse_args(args)

        module = load.module(APPLICATION, application)
        fish_food = module.attribute

        for (name, fallback) in fish_food.items():

            override = getattr(parse_args, name, NONE)
            database = configuration.get(application, name)
            value = override or database or fallback
            setattr(self.attribute, name, value)
            if parse_args.configuration:
                configuration.set(application, name, override)

        configuration.save()

        # combine this with attribute

        attribute: typing.Dict[str, str] = self.dictionary

        configuration = Configuration()
        configuration.load()

        for (name, fallback) in attribute.items():

            override = getattr(parse_args, name, NONE)
            database = configuration.get(application, name)
            value = override or database or fallback
            setattr(self.attribute, name, value)
            if parse_args.configuration:
                configuration.set(application, name, override)

        configuration.save()

    def do_work(self, configuration):
        for (name, fallback) in attribute.items():
            override = getattr(parse_args, name, NONE)
            database = configuration.get(application, name)
            value = override or database or fallback
            setattr(self.attribute, name, value)
            if parse_args.configuration:
                configuration.set(application, name, override)

    def add_positional(
        self,
        name: str,
        description: str,
        default: str,
        choice: list[str],
    ) -> None:
        """"""

        self.dictionary[name] = default

        self.positional.add_argument(
            name,
            choices=choice,
            help=description,
            nargs=QUESTION_MARK,
        )

    def add_optional(
        self,
        name: str,
        description: str,
        default: str,
    ) -> None:
        """"""

        self.dictionary[name] = default

        self.optional.add_argument(
            self.flag(name),
            self.name(name),
            help=description,
        )

    def add_override(
        self,
        name: str,
        description: str,
        default: str,
        choice: list[str],
    ) -> None:
        """"""

        self.dictionary[name] = default

        self.override.add_argument(
            self.flag(name),
            self.name(name),
            choices=choice,
            help=description,
        )
