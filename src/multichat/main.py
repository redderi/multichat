import sys
from terminal_app import terminal_app
from window_app import window_app


def main():
    if len(sys.argv) == 2 and sys.argv[1] == '-t':
        terminal_app()
    else:
        window_app()

if __name__ == "__main__":
    main()
