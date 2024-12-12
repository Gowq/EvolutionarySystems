# Cipher Breaking: Markov Chain Evolutionary Decryption

## Overview

This project implements a sophisticated cipher decryption technique that combines Markov chain analysis with an evolutionary algorithm. The system breaks substitution ciphers by using:
- Markov chain bigram frequency analysis as a fitness heuristic
- Evolutionary algorithm as a meta-heuristic search strategy

## Key Concepts

### Markov Chain Heuristic
- Uses bigram frequency probabilities to evaluate decryption quality
- Calculates a score based on the likelihood of character sequences
- Derives probabilities from a reference text corpus

### Evolutionary Meta-Heuristic
- Generates and evolves potential decryption keys
- Applies genetic algorithm principles to explore solution space
- Employs strategies like:
  - Population-based search
  - Crossover of candidate solutions
  - Mutation to introduce variation

## Technical Approach

1. **Frequency Analysis**
   - Preprocesses reference text to create bigram probability matrix
   - Calculates log-probabilities for character sequences
   - Generates a comprehensive frequency dictionary

2. **Evolutionary Decryption**
   - Initializes population of random substitution alphabets
   - Evaluates fitness using Markov chain bigram probabilities
   - Iteratively improves solutions through:
     * Tournament selection
     * Partially mapped crossover (PMX)
     * Controlled mutation

## Prerequisites

- Python 3.7+
- Dependencies:
  ```
  unidecode
  tqdm
  ```

## Installation

```bash
git clone <repository-url>
pip install unidecode tqdm
```

## Usage

### Preprocess Reference Text

Generate bigram frequency dictionary:
```bash
python process_data.py <reference_text_corpus>
```

### Decrypt Cipher

Break substitution cipher:
```bash
python crack_bigram_evol.py <encrypted_text_file>
```

## Configurable Parameters

- `population_size`: Number of candidate decryption keys
- `mutation_rate`: Probability of introducing random changes
- `elite_size`: Top solutions preserved between generations
- `generations`: Number of evolutionary iterations

## Configuration Example

```python
breaker = CipherBreaker(
    encrypted_text, 
    freq_dict, 
    population_size=100,  # Larger population increases search depth
    mutation_rate=0.9,    # High mutation explores more solutions
    elite_size=3          # Preserves top-performing candidates
)
```

## Algorithmic Workflow

1. Generate initial random substitution alphabets
2. Evaluate each alphabet's decryption quality using Markov chain probabilities
3. Select top-performing solutions
4. Create new generation through:
   - Crossover of promising candidates
   - Controlled random mutations
5. Repeat for specified number of generations
6. Return best-performing decryption key

## Performance Characteristics

- **Strengths**
  - Handles complex substitution ciphers
  - Adaptable to different text domains
  - Explores large solution spaces efficiently

- **Limitations**
  - Computational intensity increases with complexity
  - Solution quality depends on reference text
  - Not guaranteed to find perfect decryption

## Mathematical Foundations

- **Fitness Scoring**: Log-probability of bigram sequences
- **Search Strategy**: Genetic algorithm with tournament selection
- **Exploration vs Exploitation**: Balanced through mutation and crossover

## Potential Improvements

- Implement adaptive mutation rates
- Integrate trigram or higher-order Markov analysis
- Parallel processing of candidate solutions

