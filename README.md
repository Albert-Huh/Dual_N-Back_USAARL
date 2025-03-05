# Dual N-Back Test

A Python-based Dual N-Back cognitive training application using **pygame** for graphics/audio. Results and logs are saved in real time for later review and analysis.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Usage](#usage)  
   - [Main Session](#main-session)  
   - [Training Session](#training-session)  
   - [Generating Sound Effects](#generating-sound-effects)  

---

## Overview

The **Dual N-Back** test is a well-known cognitive task used to train and measure working memory. Users are presented with an **alphabet** and **square position** stimulus and must indicate if either stimulus matches the one presented **N** steps earlier. This repository implements **0-Back, 1-Back, 2-Back**, and dynamic difficulty modes in a fullscreen graphical environment.

---

## Features

- **Fullscreen or Resizable Window**: Presents stimuli in a `pygame` window.
- **Multiple Difficulty Levels**:
  - 0-Back (simplest)
  - 1-Back or 2-Back (increasing difficulty)
  - Dynamic training sessions (difficulty can change automatically based on performance).
- **Real-Time Feedback**:
  - Plays “good” or “bad” sound effects for correct/missed/false alarm responses.
- **Session/Training Logs**: Automatically saves text-based reports and user responses in `reports/` and `results/` directories.
- **Subject Metadata**: Prompts for Subject ID, Session ID, Age, Gender, etc.

---

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/dual-n-back-test.git
   cd dual-n-back-test
   '''

2. **Clone this repository**:
   ```bash
   pip install -r requirements.txt
   ```
  - Main dependencies include pygame, gTTS (for sound generation), numpy, and scipy.

3. Generate auditory feedback (optional):
  - By default, `good.mp3` and `bad.mp3` might already be in the repo. If not, run:
  ```bash
    python sound_effect.py
  ```
  This uses `gTTS` to generate the sound files for feedback.

---

## Usage

###Main Session
1. **Run the main session**:
  ```bash
  python main.py
  ```
2. **Enter required subject info** when prompted:
  - Subject Number
  - Session Number
  - Age
  - Gender (M/F)
3. The script will open a fullscreen `pygame` window and sequentially run blocks of 0-back, 1-back, and 2-back tasks (depending on the logic in `n_back_session_fullscreen.py` or `n_back_session.py`).
4. After completion, check the `reports/` and `results/` directories for:
  - `Report.txt` files (summary logs)
  - `Result.txt` files (detailed metrics and response data)

###Training Session
For a shorter, more configurable training experience:
1. **Run the training script**:
  ```bash
  python main_training.py
  ```
2. *Enter difficulty** (0 for Low, 1 for Medium, 2 for High) and subject info.
3. This script primarily references `n_back_training.py` for logic and also outputs logs to `reports/` and `results/`.

###Generating Sound Effects
If you **do not** see `good.mp3` and `bad.mp3` in the repository root, run:
```bash
python sound_effect.py
```
- This creates mp3 files using `gTTS`.
- These sound files provide the audio feedback (correct/incorrect).

