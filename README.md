# Connect 4 (Player vs AI)

A python implementation of the game Connect 4.

## Features
* **AI**
* **Customisable Board**: You can play with standard 6x7 or you can create custom boards
* **Customisable Gameplay**: Choose your token colour and who moves first

## Prerequisites
You must have **conda** and **Python** installed. 

## How to run
Create environment:
```bash
conda env create -f environment.yaml
```

Activate environment:
```bash
conda activate connect4
```

Run the game:
```bash
python3 main.py
```

## Configuration
You can configure or customise the game by providing command line arguments.
For help:
```bash
python3 main.py --help
```

| Argument | Flag | Description | Available values | Default |
|----------|------|-------------|------------------|---------|
| Difficulty | -d | Max Depth AI searches at each turn | 0 to 10 | 5 |
| Colour | -c | Colour of the tile | r and b | r |
| Turn | -t | Who moves first | 0 - AI first, 1 - Player first | 0 |
| N rows | -r | Number of rows in board | 4 to 30 | 6 |
| N columns | -cols | Number of columns in board | 4 to 30 | 7 |
