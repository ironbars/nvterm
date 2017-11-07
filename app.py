import sys
from nvterm import text_editor

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = None

    editor = text_editor.TextEditor(filename)
    
    editor.run()


if __name__ == "__main__":
    main()
