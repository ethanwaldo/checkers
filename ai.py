# ai.py
# This file contains the logic for an AI player using the Google Gemini API.

import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()

# The API key is now passed directly to the client
API_KEY = os.getenv("GEMINI_API_KEY")

class AIPlayer:
    """
    An AI player that uses a Google Gemini model to decide on a checkers move.
    """
    def __init__(self):
        """Initializes the Gemini client."""
        try:
            if not API_KEY:
                raise ValueError("GEMINI_API_KEY not found in .env file.")
            genai.configure(api_key=API_KEY)
            self.model = genai.GenerativeModel("gemini-pro")
            print("Gemini AI Player initialized successfully.")
        except Exception as e:
            print(f"ERROR: Could not initialize Gemini client: {e}")
            self.client = None

    def get_best_move(self, pdn_string):
        """
        Given the current board state in PDN, asks the AI for the best move via the Gemini API.
        """
        if not self.model:
            print(f"ERROR: Gemini client not initialized.")
            return None

        prompt = (
            "You are a helpful checkers assistant. Your goal is to identify the best possible move. "
            "You must respond ONLY with the move in the format 'start_square-end_square' (e.g., '11-15' or '22-25'). "
            "Do not add any commentary or explanation.\n\n"
            "The board state is provided in PDN format. For example: [R:K1,2,3:B4,5,6] means it is Red's turn to move, Red has kings on squares 1, 2, and 3, and Black has men on squares 4, 5, and 6." 
            "The squares are numbered 1-32, starting from the top-left of the board.\n\n"
            "Remember the rules of checkers:"
            "1. Men move forward diagonally one square at a time."
            "2. Kings can move forward or backward diagonally."
            "3. If a capture is available, it must be taken."
            "4. A piece is crowned a king when it reaches the opponent's back row.\n\n"
            f"User: Given the PDN string '{pdn_string}', what is the best move for the current player?\n"
            "Model:"
        )

        try:
            response = self.model.generate_content(prompt)

            if not response.candidates:
                finish_reason = response.candidates[0].finish_reason if response.candidates else 'UNKNOWN'
                print(f"ERROR: Gemini response was blocked or empty. Finish Reason: {finish_reason}")
                return None

            response_text = response.text.strip()
            match = re.search(r'\d+-\d+', response_text)

            if match:
                return match.group(0)
            else:
                print(f"ERROR: Could not find a valid move in AI response: '{response_text}'")
                return None

        except Exception as e:
            print(f"ERROR: An API request error occurred: {e}")
            return None