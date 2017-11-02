from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.controls import BufferControl, FillControl, TokenListControl
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.dimension import LayoutDimension as D

from pygments.token import Token

loop = create_eventloop()
manager = KeyBindingManager()
registry = manager.registry

@registry.add_binding(Keys.ControlE, eager=True)
def exit_(event):
    event.cli.set_return_value(None)

@registry.add_binding(Keys.Enter, eager=True)
def newline_(event):
    event.cli.current_buffer.newline()

@registry.add_binding(Keys.ControlS, eager=True)
def save_(event):
    doc = event.cli.current_buffer.document
    txt = doc.text

    with open("samp.txt", "w") as samp:
        samp.write(txt)

layout = VSplit([
    Window(
        content=BufferControl(buffer_name=DEFAULT_BUFFER), wrap_lines=True),
    Window(
        width=D.exact(1), content=FillControl("|", token=Token.Line)),
    Window(
        content=TokenListControl(
            get_tokens=lambda cli: [(Token, "Hello, world!")])),
])
app = Application(
    key_bindings_registry=registry, layout=layout, use_alternate_screen=True)
cli = CommandLineInterface(application=app, eventloop=loop)

cli.run()
print("Exiting")

