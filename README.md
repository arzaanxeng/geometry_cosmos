# Geometry Cosmos

A Python toolkit for 2D geometry calculations with interactive plotting.

## Features

| Mode | What it does |
|---|---|
| **Line–line** | Finds the intersection point, or the distance between parallel lines |
| **Point–point** | Calculates the Euclidean distance between two coordinates |
| **Circle–line** | Determines whether a line is a secant, tangent, or misses a circle, and plots the result |

## Project structure

```
geometry_cosmos/
├── geometry.py            # Core classes: Point, Geometry, GeometryAnalyzer
├── main.py                # Interactive CLI entry point
├── tests/
│   ├── __init__.py
│   └── test_geometry.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/geometry-cosmos.git
cd geometry-cosmos
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the CLI

```bash
python main.py
```

## Example session

```
==========================================
        Welcome to Geometry Cosmos
==========================================
  All lines use the form:  ax + by + c = 0

  1 — Line-line  (intersection / parallel distance)
  2 — Point-point  (Euclidean distance)
  3 — Circle-line  (tangent / secant / none)
  0 — Quit

  Your choice: 1

  Line 1  (a1·x + b1·y + c1 = 0)
    a1: 1
    b1: 1
    c1: -1

  Line 2  (a2·x + b2·y + c2 = 0)
    a2: 1
    b2: -1
    c2: 1

  Intersection point: (0.0, 1.0)
```

## Using the API directly

```python
from geometry import Point, Geometry, GeometryAnalyzer

# Euclidean distance
d = Point(0, 0, 3, 4).point_distance()   # -> 5.0

# Line-line intersection
geo = Geometry(1, 1, -1,  1, -1, 1)
print(geo.line_intersection())            # -> (0.0, 1.0)

# Parallel line distance
geo = Geometry(1, 1, 1,  1, 1, 5)
print(geo.parallel_line_distance())       # -> 2.8284

# Circle-line analysis (plots and prints report)
GeometryAnalyzer(
    a1=0, b1=0, r=5,    # circle: centre (0, 0), radius 5
    a2=1, b2=0, c2=0,   # line:   x = 0
).analyze_geometry()
```

## Running tests

```bash
pytest tests/ -v
```

## Requirements

- Python 3.10+
- numpy >= 1.24
- matplotlib >= 3.7
- pytest >= 7.4  *(tests only)*

