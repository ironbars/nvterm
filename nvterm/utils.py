from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys


def load_key_bindings(controller):
    manager = KeyBindingManager()
    registry = manager.registry

    @registry.add_binding(Keys.ControlC, eager=True)
    def exit_(event):
        controller.cli.set_return_value(None)

    @registry.add_binding(Keys.Enter, eager=True)
    def newline_(event):
        controller.editor.buffer.newline()

    #@registry.add_binding(Keys.ControlS, eager=True)
    #def save_(event):
        #text = editor.cli.current_buffer.text
        #editor.file_handler.write(text)

    @registry.add_binding(Keys.Tab, eager=True)
    def insert_tab_(event):
        controller.editor.buffer.insert_text("\t")

    return registry
