# Escape Python Advanced

An interactive Python quiz game with a thrilling escape room theme, designed to test advanced Python programming knowledge through multiple levels of challenging questions.

## 🎮 Game Overview

**Escape Python Advanced** is an educational game where players progress through 3 levels, each containing 3 questions based advanced Python programming Topics. Players must correctly answer questions to collect code segments and unlock access codes to advance to the next level. The Codes are to be arranged in the order of the topics taught

## ✨ Features

- **Multi-Level Gameplay**: 3 progressive levels with increasing difficulty
- **Code Collection System**: Earn 2-character code segments for correct answers
- **Puzzle Solving**: Arrange collected codes in the correct order based on Python topic sequence
- **Multiple Difficulty Modes**: Easy (unlimited time), Medium (10 min), Hard (5 min), Impossible (3 min)
- **Hint System**: Up to 3 hints per level to help with challenging questions
- **Admin Panel**: Complete question management system for educators
- **Beautiful UI**: Dark-themed interface with progress tracking and visual feedback
- **Splash Screen**: Professional game startup experience

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Required Python packages:
  pip install tkinter pillow

### Setup

1. Clone or download the repository
2. Ensure you have the following files in your project directory:
   - `logic.py` (main game file)
   - `questions.txt` (question database)
   - `background_fullscreen.png` (background image)

3. Run the game:
   python logic.py

## 📖 How to Play

1. **Start**: Launch the game and select your preferred difficulty level
2. **Answer Questions**: Each level contains 3 questions about Python advanced topics
3. **Collect Codes**: Correct answers reward you with 2-character code segments
4. **Solve the Puzzle**: Questions are shuffled - use your knowledge to arrange codes in the correct topic order
5. **Enter Access Code**: Combine your code segments to create a 6-character access code
6. **Progress**: Successfully entering the code unlocks the next level

### Difficulty Levels

- **Easy**: Unlimited time to complete all levels
- **Medium**: 10 minutes total time limit
- **Hard**: 5 minutes total time limit  
- **Impossible**: 3 minutes total time limit

## 🛠️ Admin Features

The game includes a comprehensive admin panel for educators and content managers:

### Admin Access
- Create admin accounts with username/password authentication
- Secure login system with credential verification
- Protected administrative functions

### Question Management
- **Modify Questions**: Edit existing question content

### Admin Panel Access
1. Click the hidden button on the main screen
2. Create an admin account (first time) or login with existing credentials
3. Access the question management interface

## 📁 File Structure

escape-python-advanced/
├── logic.py                 # Main game logic and UI
├── questions.txt            # Question database (required)
├── admin_credentials.txt    # Admin login credentials (auto-generated)
├── background_fullscreen.png # Background image (optional)
└── README.md               # This file


## 🔧 Question File Format

Questions are stored in `questions.txt` with the following format:


# Level 1
QUESTION: What is a Python decorator?
ANSWER: A function that modifies another function
HINT: Think about the @ symbol
CODE: AB
ORDER: 1

# Level 2
QUESTION: Explain list comprehensions
ANSWER: Concise way to create lists
HINT: Square brackets with for loops
CODE: CD
ORDER: 2


## 🎯 Educational Goals

This game is designed to reinforce learning in:
- Advanced Python concepts
- Problem-solving under time pressure
- Logical thinking and code organization
- Interactive learning through gamification


## 🚀 Future Enhancements

Potential improvements could include:
- Database integration for question storage
- Multiplayer functionality
- Score tracking and leaderboards  
- Additional question types (multiple choice, code completion)
- Sound effects and animations
- Web-based version

## 🤝 Contributing

To contribute questions or improvements:
1. Follow the established question format
2. Test thoroughly across all difficulty levels
3. Ensure questions align with advanced Python curriculum

## 🆘 Support

If you encounter issues:
1. Ensure all required files are present
2. Check that Python dependencies are installed
3. Verify the `questions.txt` file follows the correct format
4. Make sure you have proper file permissions for creating admin credentials

---

**Ready to test your Python skills? Good luck escaping!** 🐍✨
