from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.processors import TabsProcessor

from .key_bindings import create_key_bindings
from .file_handler import FileHandler


class TextEditor(object):
    """
    Main class
    """
    def __init__(self, initial_file=None):
        self.file_handler = FileHandler(initial_file)
        self.keybind_registry = create_key_bindings(self)
        self.loop = create_eventloop()
        self.app = self._create_application()
        self.cli = CommandLineInterface(
            application=self.app, eventloop=self.loop)

    
    def _create_application(self):
        procs = [TabsProcessor(get_char1=lambda cli: " ")]
        layout = Window(
            content=BufferControl(
                buffer_name=DEFAULT_BUFFER, input_processors=procs),
                wrap_lines=True)
        registry = create_key_bindings(self)
        application = Application(
            key_bindings_registry=registry, 
            layout=layout, 
            use_alternate_screen=True)

        return application

    
    def load_initial_file(self):
        text = self.file_handler.read()
        
        if text is not None:
            self.cli.current_buffer.insert_text(text)


    def run(self):
        self.load_initial_file()
        self.cli.run()
        
