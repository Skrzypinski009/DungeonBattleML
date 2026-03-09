# DungeonBattleML
A program for testing AI algorithms in a turn-based battle game.

## Technologies Used
- **Python 3.13**
- **Main libraries:**
  - **NumPy** (Math)
  - **Pandas** (Data processing)
  - **Scikit-learn** (Supervised learning)
  - **Gymnasium** (Reinforcement learning)
  - **Peewee** (ORM)
  - **Kivy** (GUI)
- **Database:** SQLite

## Game Overview
### Stats
- Health Points (HP)
- Energy Points
- Attack Damage
- Health Potions

### Actions
- Attack
- Heavy Attack
- Block
- Regeneration
- End Turn

### Battle Process
1. **Select game options:** Set the number of potions and types of enemies to fight.
2. **Turn-based gameplay:** Perform actions as long as your energy points allow.
3. **Victory condition:** The battle ends when a participant reaches 0 HP.

## Data Collection
The program can collect gameplay data during battles for analysis and training purposes.

## AI Training
### Supervised Learning
1. After collecting data, you can create a **Dataset** from selected battles.
2. The program allows you to select one of three models: **Decision Tree, Random Forest, or MLP Neural Network**.
3. Once the training process is complete, you can test the model's performance in-game.

### Reinforcement Learning
1. Choose the **Q-table** model (currently the only available RL method).
2. Select game options and start the training process.
3. After training, you can test the model in-game and observe its behavior.
