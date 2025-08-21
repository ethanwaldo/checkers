# main.py
# Main entry point of the application

from gui import CheckersGUI


def main():
    """Main entry point of the application."""
    game = CheckersGUI()
    game.run()


if __name__ == "__main__":
    main()
