from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.application import Application
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.shortcuts import create_eventloop

from .components import TextEditor
from .utils import load_key_bindings

__all__ = (
    "NVController"
)


class NVController(object):
    """
    Class for orchestration; allows all NVComponents to interact
    """
    def __init__(self):
        self.editor = TextEditor()
        #self.file_manager = FileManager()
        #self.search_control = SearchControl()
        self.layout = self.editor.layout
        self.buffers = {
            DEFAULT_BUFFER:  self.editor.buffer
            #"FILES": self.file_manager.buffer
            #"CONTROL": self.search_control.buffer
        }
        self.loop = create_eventloop()
        self.application = self._create_application()
        self.cli = CommandLineInterface(
            application=self.application, eventloop=self.loop)


    def _create_application(self):
        registry = load_key_bindings(self)
        app = Application(
            key_bindings_registry=registry,
            buffers=self.buffers,
            layout=self.layout,
            use_alternate_screen=True)

        return app


    def run(self):
        self.cli.run()
