from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.enums import DEFAULT_BUFFER, SEARCH_BUFFER
from prompt_toolkit.layout.controls import BufferControl, FillControl
from prompt_toolkit.layout.containers import Window, HSplit
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.token import Token

editor_layout = Window(
    content=BufferControl(buffer_name=DEFAULT_BUFFER), wrap_lines=True)
fm_layout = Window(
    height=D.exact(10), content=BufferControl(buffer_name='FILES'))
search_layout = Window(
    height=D.exact(1), content=BufferControl(buffer_name=SEARCH_BUFFER))
app_layout = HSplit([
    search_layout,
    Window(height=D.exact(1),
        content=FillControl('-', token=Token.Line)),
    fm_layout,
    Window(height=D.exact(1),
        content=FillControl('-', token=Token.Line)),
    editor_layout
])
buffers = {
    DEFAULT_BUFFER: Buffer(is_multiline=True),
    "FILES": Buffer(),
    SEARCH_BUFFER: Buffer()
}
registry = KeyBindingManager().registry

@registry.add_binding(Keys.ControlC, eager=True)
def exit_(event):
    event.cli.set_return_value(None)

loop = create_eventloop()
app = Application(
    key_bindings_registry=registry,
    buffers=buffers,
    layout=app_layout, 
    use_alternate_screen=True)
cli = CommandLineInterface(application=app, eventloop=loop)

cli.run()
print("Exiting")


