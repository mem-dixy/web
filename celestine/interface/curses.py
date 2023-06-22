""""""

import io
import math

from celestine.typed import (
    N,
    R,
)
from celestine.unicode import LINE_FEED
from celestine.unicode.notational_systems import BRAILLE_PATTERNS
from celestine.window.collection import Rectangle
from celestine.window.element import Abstract as Abstract_
from celestine.window.element import Button as Button_
from celestine.window.element import Image as Image_
from celestine.window.element import Label as Label_
from celestine.window.window import Window as window
from celestine.window.container import View, Zone

color_index = 8  # skip the 8 reserved colors
color_table = {}

COLORS = 15


def get_colors(curses, image):
    """Fails after being called 16 times."""

    global color_index
    global color_table

    colors = image.getcolors()
    for color in colors:
        (count, pixel) = color
        (red, green, blue) = pixel

        red *= 1000
        green *= 1000
        blue *= 1000

        red //= 255
        green //= 255
        blue //= 255

        if red >= 920 or green >= 920 or blue >= 920:
            pass
            # print(red, green, blue)
        curses.init_color(color_index, red, green, blue)
        curses.init_pair(color_index, color_index, 0)

        color_table[pixel] = color_index
        color_index += 1


class Abstract(Abstract_):
    """"""

    def add_string(self, frame, x_dot, y_dot, text, *extra):
        """
        Curses swaps x and y.

        Also minus the window border to get local location.

        Text length need be size-1 long.
        """
        frame.addstr(y_dot - 1, x_dot - 1, text, *extra)

    def render(self, view, item, **star):
        """"""
        text = item
        (x_dot, y_dot) = self.area.origin
        self.add_string(view, x_dot, y_dot, text)


class Button(Abstract, Button_):
    """"""

    def draw(self, ring: R, view, **star):
        """"""
        item = f"button:{self.data}"
        self.render(view, item, **star)


class Image(Abstract, Image_):
    """"""

    def output(self):
        width, height = self.cache.size

        pixels = list(self.cache.getdata())
        string = io.StringIO()

        def shift(offset_x, offset_y):
            nonlocal braille
            nonlocal range_x
            nonlocal range_y

            index_x = range_x + offset_x
            index_y = range_y + offset_y

            index = index_y * width + index_x
            pixel = pixels[index] // 255

            braille <<= 1
            braille |= pixel

        for range_y in range(0, height, 4):
            for range_x in range(0, width, 2):
                braille = 0

                shift(0, 0)
                shift(1, 0)
                shift(0, 1)
                shift(1, 1)
                shift(0, 2)
                shift(1, 2)
                shift(0, 3)
                shift(1, 3)

                text = BRAILLE_PATTERNS[braille]
                string.write(text)

            string.write(LINE_FEED)

        value = string.getvalue()
        value = value[0:-1]
        return value.split(LINE_FEED)

    def render(self, ring, /, collection, item, **star):
        """"""
        curses = ring.package.curses

        (x_dot, y_dot) = self.area.origin

        if not ring.package.pillow:
            self.add_string(
                collection,
                x_dot,
                y_dot,
                item,
            )
            return

        color = list(self.color.getdata())

        index_y = 0
        for row_text in item:
            index_x = 0
            for col_text in row_text:
                width, height = self.color.size
                index = index_y * width + index_x

                (red, green, blue) = color[index]
                table = color_table[(red, green, blue)]
                extra = curses.color_pair(table)

                self.add_string(
                    collection,
                    x_dot + index_x,
                    y_dot + index_y,
                    col_text,
                    extra,
                )

                index_x += 1

            index_y += 1

    def draw(self, ring: R, view, **star):
        """"""
        curses = ring.package.curses
        pillow = ring.package.pillow

        if not pillow:
            self.render(ring, view, self.path.name, **star)
            return

        self.cache = pillow.image_load(self.path)
        self.color = pillow.image_clone(self.cache)

        # Crop box.
        source_length_x = self.cache.image.width
        source_length_y = self.cache.image.height

        length_x, length_y = self.area.size

        target_length_x = length_x * 2
        target_length_y = length_y * 4

        source_length = (source_length_x, source_length_y)
        target_length = (target_length_x, target_length_y)

        box = self.crop(source_length, target_length)
        # Done.

        self.color.brightwing()

        target_length = (target_length_x, target_length_y)
        self.cache.resize(target_length, box)
        self.color.resize(self.area.size, box)

        self.color.quantize()

        self.cache.convert_to_mono()
        self.color.convert_to_color()

        get_colors(curses, self.color.image)

        item = self.output()
        self.render(ring, view, item, **star)


class Label(Abstract, Label_):
    """"""

    def draw(self, ring: R, view, **star):
        """"""
        item = f"label:{self.data}"
        self.render(view, item, **star)


class Window(window):
    """"""

    def setup(self, container):
        """"""
        curses = self.ring.package.curses
        container.canvas = curses.window(*self.area.value)

    def draw(self, **star):
        """"""
        curses = self.ring.package.curses

        # Do normal draw stuff.
        # self.setup(self.page)

        value = self.container.area.value
        self.page.canvas = curses.window(*value)

        super().draw(**star)

        self.stdscr.noutrefresh()
        self.background.noutrefresh()
        self.page.canvas.noutrefresh()
        curses.doupdate()

        # Reset the global color counter.
        global color_index
        global color_table
        color_index = 8
        color_table = {}

    def extension(self):
        """"""
        if self.ring.package.pillow:
            return self.ring.package.pillow.extension()

        return []

    def view(self, name, function):
        """"""
        container = self.container.zone(name, mode=Zone.DROP)
        self.setup(container)
        function(self.ring, container)

        area = Rectangle(*self.container.area.value)
        container.spot(area)
        self._view.set(name, container)

    def __enter__(self):
        super().__enter__()

        curses = self.ring.package.curses

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.start_color()

        (size_y, size_x) = self.stdscr.getmaxyx()
        self.area = Rectangle(0, 0, size_x, size_y)

        self.background = curses.window(0, 0, size_x, size_y)
        self.background.box()

        header_box = (0, 0, size_x, 1)
        header = curses.subwindow(self.background, *header_box)
        header.addstr(0, 1, self.ring.language.APPLICATION_TITLE)

        footer_box = (0, size_y - 1, size_x, 1)
        footer = curses.subwindow(self.background, *footer_box)
        footer.addstr(0, 1, self.ring.language.CURSES_EXIT)

        #
        area = Rectangle(1, 1, size_x - 2, size_y - 2)
        self.container = View(
            self.ring,
            "window",
            self,
            self.element,
            area,
            offset_x=0,
            offset_y=0,
        )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

        curses = self.ring.package.curses

        while True:
            event = self.stdscr.getch()
            match event:
                case 258 | 259 | 260 | 261 as key:
                    match key:
                        case curses.KEY_UP:
                            self.cord_y -= 1
                        case curses.KEY_DOWN:
                            self.cord_y += 1
                        case curses.KEY_LEFT:
                            self.cord_x -= 1
                        case curses.KEY_RIGHT:
                            self.cord_x += 1

                    size_x, size_y = self.area.size
                    self.cord_x %= size_x
                    self.cord_y %= size_y
                    self.stdscr.move(
                        math.floor(self.cord_y),
                        math.floor(self.cord_x),
                    )
                case curses.KEY_EXIT:
                    break
                case curses.KEY_CLICK:
                    self.page.poke(self.cord_x, self.cord_y)

        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        return False

    def __init__(self, ring: R, **star) -> N:
        element = {
            "button": Button,
            "image": Image,
            "label": Label,
        }
        area = Rectangle(0, 0, 0, 0)
        super().__init__(ring, element, area, **star)
        self.background = None
        self.cord_x = 0.5
        self.cord_y = 0.5
        self.frame = None
        self.stdscr = None

        self.container = None
