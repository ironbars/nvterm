from abc import ABCMeta, abstractmethod
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.processors import TabsProcessor


__all__ = (
    "TextEditor"
)


class NVComponent(metaclass=ABCMeta):
    """
    Generic class for nvTerm components
    """
    @abstractmethod
    def yield_buffer_content(self):
        """
        Return the contents of this object's buffer to the caller
        """


    @abstractmethod
    def accept_buffer_content(self, content):
        """
        Write given content into own buffer; the format will be different 
        depending on which class uses this
        """


    @abstractmethod
    def clear_buffer(self):
        """
        Empty own buffer
        """


class TextEditor(NVComponent):
    """
    Basic text editor for nvTerm.  Will obey some readline key bindings,
    but not looking for anything fancy here.
    """
    def __init__(self):
        self.processors = [TabsProcessor(get_char1=lambda cli: " ")]
        self.layout = Window(
            content=BufferControl(
                buffer_name=DEFAULT_BUFFER, input_processors=self.processors),
            wrap_lines=True)
        self.buffer = Buffer(is_multiline=True)


    def yield_buffer_content(self):
        return self.buffer.text


    def accept_buffer_content(self, content):
        self.buffer.insert_text(content)


    def clear_buffer(self):
        self.buffer.document = Document()

