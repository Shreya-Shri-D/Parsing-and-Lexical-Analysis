# Parsing and Lexical Analysis

Theory of Computation coursework: a **chart-based Earley parser** for natural-language-style sentences and a **multi-language lexical analyser** for C, Java, and C++, plus small **palindrome checker** programs used as sample inputs.

---

## Repository layout

```
├── EarleyParser/                    # Earley algorithm (Python)
│   ├── main.py                      # Entry: charts + parse tree
│   ├── grammar.py                  # CFG loading and rule lookup
│   ├── utils.py                    # Normalisation, NLTK tree build/display
│   ├── grammatik.txt               # Grammar + start symbol
│   └── input.txt                   # Sentence(s) to parse
├── Multi-Language-Lexical-Analyser/
│   ├── final_no_errors.py          # Lexers + tabulated token output
│   ├── pal.c / pal.cpp / pal.java  # Palindrome demos (lexer-friendly input)
└── requirements.txt
```

---

## 1. Earley parser (`EarleyParser/`)

### What it does

This implements **Earley’s algorithm** for context-free grammars (CFGs). It maintains a sequence of **charts** (sets of Earley *states*). Each state records:

- A grammar rule, a **dot** position in the rule’s right-hand side, and an **origin** chart index.
- How the state was produced: **Predict** (expand a non-terminal), **Scan** (match a terminal), or **Complete** (finish a rule and advance callers).

Parsing walks the input word by word; after processing, the last chart contains items that show whether the sentence is consistent with the grammar. A **parse tree** is built from completed states (using NLTK’s `Tree`) and can be drawn when a GUI is available.

### Grammar file format (`grammatik.txt`)

- First non-comment line should declare the start symbol, e.g.  
  `% start S`
- Rules use `->` and alternatives with `|`, e.g.  
  `S -> SENTENCE | SENTENCE Con S`  
  `NP -> Det AN`
- **Terminals** are symbols that never appear on the **left** side of any rule. **Non-terminals** have at least one production.
- The bundled grammar models simple English-like **NP / VP** structure, determiners, adjectives, nouns (including multi-word phrases like `female dog`), verbs, and conjunctions.

### Input (`input.txt`)

Plain text; punctuation is stripped in code (`normalize` in `utils.py`). Words are split on whitespace. You can use multiple lines; the normalised string is treated as one token sequence for parsing.

### How to run

From the `EarleyParser` directory (after installing dependencies):

```bash
cd EarleyParser
python main.py
```

Paths to `grammatik.txt` and `input.txt` are resolved **relative to `main.py`**, so the project runs without editing hard-coded machine paths.

### Dependencies

- **Python 3**
- **nltk** — used for `Tree` and optional graphical tree drawing (`Tree.draw()`).

---

## 2. Multi-language lexical analyser (`Multi-Language-Lexical-Analyser/`)

### What it does

`final_no_errors.py` implements three hand-written **finite-state style** lexers:

| Class       | Target language | Notes |
|------------|-----------------|--------|
| `CLexer`   | C               | Preprocessor (`#include`), headers, keywords, identifiers, numbers, strings, operators, symbols. |
| `JavaLexer`| Java            | Keywords, `System.out` / common APIs, class names, etc. |
| `CppLexer` | C++             | Keywords, `std::` patterns, operators including `->` and `::`. |

Each lexer walks the source **character by character**, updates a small state machine, and emits `(token_type, value)` pairs. Tokens are printed as a **grid table** via **tabulate**.

### Sample programs (`pal.*`)

`pal.c`, `pal.cpp`, and `pal.java` are **palindrome sentence checkers**: they read a line of text, strip non-letters, fold case, and report whether the result is a palindrome. They serve as **readable sample inputs** for the lexer (identifiers, strings, I/O calls, etc.).

### How to run the lexer

From `Multi-Language-Lexical-Analyser`:

```bash
# Default: tokenise pal.c in this folder
python final_no_errors.py

# Choose another sample
python final_no_errors.py pal.java
python final_no_errors.py pal.cpp
```

File type is chosen from the **extension** (`.c`, `.java`, `.cpp`).

### How to compile and run the palindrome demos (optional)

```bash
gcc pal.c -o pal_c && ./pal_c
g++ pal.cpp -o pal_cpp && ./pal_cpp
javac pal.java && java PalindromeChecker
```

*(Adjust filenames if your compiler expects a public class name match.)*

### Dependencies

- **Python 3**
- **tabulate** — pretty-printed token tables.

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Academic use

This repository is submitted as part of **M.Sc. TCS — Theory of Computation** coursework. Reuse is limited by your institution’s policies.

---

## Author

**Shreya Shri D** — [`Parsing-and-Lexical-Analysis`](https://github.com/Shreya-Shri-D/Parsing-and-Lexical-Analysis)
