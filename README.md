# Python Chess Game with AI

A complete, fully-functional chess game with a graphical user interface (GUI) built using Python and the Pygame library. This project features a robust engine that enforces all standard and advanced chess rules and includes an AI opponent powered by OpenAI's GPT models.



## Features
* **Complete Chess Logic:** A fully implemented chess engine that handles all aspects of gameplay.
* **AI Opponent:** Play against an AI powered by a large language model (LLM) from OpenAI.
* **Standard and Special Moves:** Includes all standard piece movements as well as the three special moves:
    * Castling (Kingside and Queenside)
    * En Passant
    * Pawn Promotion
* **Full Endgame Detection:** The engine correctly identifies all major endgame conditions:
    * Check and Checkmate
    * Stalemate
    * Draw by Threefold Repetition
    * Draw by the 50-Move Rule
    * Draw by Insufficient Material
* **Interactive GUI:** A clean graphical interface for gameplay, featuring:
    * Move highlighting for selected pieces.
    * A display for captured pieces, player timers, and game status.
    * Buttons for New Game, Undo, Resign, and Offer Draw.
* **AI-Ready:** The engine can generate the current game state in Forsyth-Edwards Notation (FEN), the standard for interfacing with chess AI.

***

## File Structure
The project is organized with a clean separation of concerns:
* `main.py`: The main entry point to launch the game.
* `gui.py`: Manages all Pygame rendering, user input, and visual elements.
* `engine.py`: The core game engine. It handles all game state, rules, and move logic.
* `pieces.py`: Defines the movement patterns for each individual chess piece.
* `ai.py`: Contains the logic for the AI player and communication with the OpenAI API.
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
    * Add your OpenAI API key to this file. **This file should never be shared or uploaded to GitHub.**
        ```
        OPENAI_API_KEY="your_secret_api_key_goes_here"
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