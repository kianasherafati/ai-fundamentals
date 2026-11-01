# Constraints and Adversarial Search

Two complementary search projects:

- **Crossword:** a constraint-satisfaction solver using domain filtering, AC-3, and backtracking with variable/value ordering.
- **Isolation:** game-playing agents using minimax, iterative-deepening alpha-beta search, and expectimax with heuristic evaluation functions.

## Crossword

From this project directory:

```sh
cd crossword
python -X utf8 main.py puzzles/p1.txt
```

Run from `crossword/` so the relative `words/words.txt` path resolves correctly.

## Isolation

From this project directory:

```sh
cd isolation
python visualize.py
```

The visualizer writes `isoviz/match.json` and opens the bundled browser visualization. Preserve the `isoviz/` and inner `isolation/` package directories. Python sources use the standard library; the browser visualization includes its own JavaScript assets.

[Crossword implementation](crossword/creator.py) · [Game agents](isolation/game_agent.py) · [Course report](report.pdf)

The bundled engine and visualizer include their original license notices.
