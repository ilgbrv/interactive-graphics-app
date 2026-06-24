# SuperRace — 2D Interactive Racing Simulator

An interactive 2D desktop racing game built with Python and the Tkinter Canvas graphics environment. The project features automated environment scrolling, dynamic object physics, user betting interaction, and procedurally generated assets. 

Developed as a capstone project during the **Stanford University "Code in Place"** program (2026).

## Tech Stack & Architecture
* **Language:** Python 
* **GUI Engine:** Tkinter Canvas API
* **Concepts Applied:** Event-driven programming, Game loop architecture, State tracking, Procedural grid rendering, Physics simulation (deceleration/braking models).

## Key Features & Implementation Details

* **Interactive Betting Dashboard:** Implements a game-state freeze at startup. Monitors real-time user input (`canvas.get_new_mouse_clicks()`) and filters coordinate matrices (Y-axis bounds mapping) to process users' bets on either the Red or Blue team.
* **Infinite Pseudo-3D Scrolling Algorithm:** Simulates high-speed movement through a continuous rendering loop. Uses coordinate boundary-check resets (`TEXT_OFFSCREEN_LIMIT` and `LINE_OFFSCREEN_LIMIT`) to recycle and wrap background road markers and fence typography seamlessly.
* **Procedural Track & Asset Generation:** 
  * Generates checkered curb patterns dynamically using alternating pixel grids based on arithmetic modulos (`stripe_number % 2 == 0`).
  * Procedurally renders pixel-art finish flags using nested loops to evaluate cell placement formulas (`(i + j) % 2 == 0`) for colors.
* **Dynamic Physics & Vector Constraints:** Car telemetry relies on randomized speed steps (`random.randint(-8, 9)`), bound inside vector limit values (`MIN_TRACK_LIMIT` / `MAX_TRACK_LIMIT`) to ensure safe horizontal constraints.
* **Linear Deceleration Braking Model:** Features a progressive braking state machine. When cars cross the finish threshold, the engine reduces speeds step-by-step using declining acceleration formulas (`brake_timer // BRAKE_DECELERATION_RATE`) until objects hit a full stop.

## How to Run

1. Clone the repository:
```bash
git clone https://github.com
```

2. Place the required `dashboard.png` image asset inside the project root folder.

3. Run the script:
```bash
python main.py
```
