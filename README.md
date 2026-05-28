# Wordle Solver

**An entropy-based Wordle solver that finds the optimal guess using information theory.**

Uses a precomputed feedback matrix and Shannon entropy to rank every possible guess by how much information it reveals — consistently solving Wordles in 3-4 guesses.

## How It Works

1. **Feedback Matrix** — Precomputes the color pattern (green/yellow/gray) for every possible guess-answer pair and stores it as a NumPy array
2. **Entropy Calculation** — For each candidate guess, calculates how evenly it partitions the remaining answer space using Shannon entropy: `H = -sum(p * log2(p))`
3. **Greedy Selection** — Picks the guess with the highest entropy (most information gain), filters the remaining words by the observed pattern, and repeats

The solver starts from ~12,000 valid guesses and ~2,300 possible answers, narrowing down exponentially with each guess.

## Key Files

| File | Purpose |
|------|---------|
| `wordle.py` | Core solver — entropy ranking + feedback matrix |
| `WordleSolver.ipynb` | Interactive notebook walkthrough |
| `wordletester.py` | Batch testing across all possible answers |
| `answer_words.txt` | Official Wordle answer list |
| `words.txt` | Full valid guess list |

## Usage

```bash
pip install numpy tqdm

# Run the solver interactively
python wordle.py

# Batch test performance
python wordletester.py
```

## Performance

The entropy-based approach significantly outperforms naive strategies — most puzzles solve in 3-4 guesses by maximizing information gain at each step.

## License

MIT
