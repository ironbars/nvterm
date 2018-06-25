"""
This module contains thin wrappers around prompt_toolkit UIControls, so that 
the controller object has a consistent interface from which to access their 
content.
"""
import os
import sqlite3
from abc import ABCMeta, abstractmethod

from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.processors import TabsProcessor

from .menu import MenuControl


__all__ = (
    "TextEditor",
    "NoteQuery",
    "NoteList"
)


class NVComponent(metaclass=ABCMeta):
    """
    Generic class for nvTerm components
    """
    @abstractmethod
    def get_content(self):
        """
        Return the contents of this object's buffer to the caller
        """


    @abstractmethod
    def set_content(self, content):
        """
        Write given content into own buffer; the format will be different 
        depending on which class uses this
        """


    @abstractmethod
    def clear_content(self):
        """
        Empty own buffer
        """


class NoteQuery(NVComponent):
    """
    Class to retrieve a list of notes
    """
    def __init__(self, io_backend="file"):
        assert io_backend == "file" or io_backend == "database"
        self.query = None
        self.result = None

        if io_backend == "file":
            self.retriever = _FileRetriever()
        else:
            self.retriever = _DBRetriever()


    def get_content(self):
        self.result = self.retriever.retrieve(self.query)
        
        return self.result

    
    def set_content(self, content):
        self.query = content


    def clear_content(self):
        self.query = None
        self.result = None


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


    def get_content(self):
        return self.buffer.text


    def set_content(self, content):
        self.buffer.insert_text(content)


    def clear_content(self):
        self.buffer.document = Document()


class NoteList(NVComponent):
    """
    The notes menu
    """
    def __init__(self, notes):
        self.layout = Window(content=MenuControl(notes))


    def get_content(self):
        return self.menu.get_selection()


    def set_content(self, notes):
        self.menu.menu_items = notes


    def clear_content(self):
        self.menu.menu_items = []


class _NoteRetriever(metaclass=ABCMeta):
    def retrieve(self, query):
        """
        Query the IO component to get a list of notes
        """


class _FileRetriever(_NoteRetriever):
    def __init__(self):
        self.repository = os.path.expanduser("~/.notes")

    def retrieve(self, query=None):
        if query is None:
            return os.listdir(self.repository)

        notes = os.listdir(self.repository)
        selection = [note for note in notes if query in note]

        return selection


class _DBRetriever(_NoteRetriever):
    def __init__(self):
        self.repository = os.path.expanduser("~/.notes.db")

    def retrieve(self, query):
        conn = sqlite3.connect(self.repository)
        cur = conn.cursor()
        notes = cur.execute(
            "SELECT title FROM notes WHERE title LIKE '%?%'", query)

        conn.close()

        return [note[0] for note in notes]
