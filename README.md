# Python Checkers Game with AI

A complete, fully-functional checkers game with a graphical user interface (GUI) built using Python and the Pygame library. This project features a robust engine that enforces all standard checkers rules and includes an AI opponent powered by Google's Gemini models.

## Features
* **Complete Checkers Logic:** A fully implemented checkers engine that handles all aspects of gameplay.
* **AI Opponent:** Play against an AI powered by a large language model (LLM) from Google.
* **Standard and Special Moves:** Includes all standard piece movements as well as:
    * Capturing (Jumping)
    * Promotion to a King
* **Full Endgame Detection:** The engine correctly identifies all major endgame conditions:
    * Win by capturing all opponent pieces.
    * Win by blocking all opponent's legal moves.
    * Draw by Threefold Repetition.
    * Draw by Agreement.
    * Resignation.
* **Interactive GUI:** A clean graphical interface for gameplay, featuring:
    * Move highlighting for selected pieces.
    * A display for captured pieces, player timers, and game status.
    * Buttons for New Game, Undo, Resign, and Offer Draw.
* **AI-Ready:** The engine can generate the current game state in Portable Draughts Notation (PDN), the standard for interfacing with checkers AI.

***

## File Structure
The project is organized with a clean separation of concerns:
* `main.py`: The main entry point to launch the game.
* `gui.py`: Manages all Pygame rendering, user input, and visual elements.
* `engine.py`: The core game engine. It handles all game state, rules, and move logic.
* `pieces.py`: Defines the movement patterns for each individual checkers piece.
* `ai.py`: Contains the logic for the AI player and communication with the Google Gemini API.
* `config.py`: A central file for all constants, such as colors, window size, and UI layout.
* `requirements.txt`: Lists the necessary Python packages for the project.

***

## How to Run

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Set up your API Key**
    * Create a new file in the root directory of the project named `.env`.
    * Add your Google Gemini API key to this file. **This file should never be shared or uploaded to GitHub.**
        ```
        GEMINI_API_KEY="your_secret_api_key_goes_here"
        ```

3.  **Create and activate a virtual environment**
    ```bash
    # Create the environment
    python3 -m venv venv
    
    # Activate on Linux/macOS
    source venv/bin/activate
    
    # Activate on Windows (PowerShell)
    .\venv\Scripts\Activate.ps1
    ```

4.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the game**
    ```bash
    python main.py
    ```

***

## Controls
* **Mouse Click:** Select a piece and click a valid destination square to move.
* **`U` Key:** Undo the last move.
* **`R` Key:** Reset the game to its starting position.
