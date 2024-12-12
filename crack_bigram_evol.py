import sys
import json
import random
from string import ascii_uppercase
from typing import List, Dict, Tuple
from unidecode import unidecode
from tqdm import tqdm

def calc_score(text: str, freq_dict: Dict[int, Dict[int, float]]) -> float:
    """
    Calculate the scoring based on bigram frequencies.
    
    Args:
        text (str): Decrypted text
        freq_dict (Dict[int, Dict[int, float]]): Frequency dictionary of bigrams
    
    Returns:
        float: Cumulative score based on bigram frequencies
    """
    max_sz = 3000
    text = text.lower()
    score = 0
    for i in range(min(len(text) - 1, max_sz)):
        score += freq_dict[ord(text[i])][ord(text[i+1])]
    return score

def substitute(alpha: str, text: str) -> str:
    """
    Perform substitution cipher decryption.
    
    Args:
        alpha (str): Substitution alphabet
        text (str): Encrypted text
    
    Returns:
        str: Decrypted text
    """
    alpha_orig = ascii_uppercase
    dct = [chr(i) for i in range(128)]
    for i in range(len(alpha)):
        dct[ord(alpha[i])] = alpha_orig[i]
    return ''.join(dct[ord(c)] for c in text)

class CipherBreaker:
    def __init__(self, encrypted_text: str, freq_dict: Dict[int, Dict[int, float]], 
                 population_size: int = 100, mutation_rate: float = 0.1, 
                 elite_size: int = 10):
        """
        Initialize the evolutionary cipher breaker.
        
        Args:
            encrypted_text (str): Text to be decrypted
            freq_dict (Dict[int, Dict[int, float]]): Frequency dictionary
            population_size (int): Number of candidate solutions
            mutation_rate (float): Probability of mutation
            elite_size (int): Number of top solutions to preserve
        """
        self.encrypted_text = encrypted_text
        self.freq_dict = freq_dict
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        
        # Initialize population
        self.population = self._generate_initial_population()
        
    def _generate_initial_population(self) -> List[str]:
        """
        Generate initial population of random substitution alphabets.
        
        Returns:
            List[str]: List of substitution alphabets
        """
        population = []
        for _ in range(self.population_size):
            alphabet = list(ascii_uppercase)
            random.shuffle(alphabet)
            population.append(''.join(alphabet))
        return population
    
    def _fitness(self, alphabet: str) -> float:
        """
        Calculate fitness (score) for a given alphabet.
        
        Args:
            alphabet (str): Substitution alphabet
        
        Returns:
            float: Fitness score
        """
        decrypted_text = substitute(alphabet, self.encrypted_text)
        return calc_score(decrypted_text, self.freq_dict)
    
    def _crossover(self, parent1: str, parent2: str) -> str:
        """
        Perform crossover between two parent alphabets.
        
        Args:
            parent1 (str): First parent alphabet
            parent2 (str): Second parent alphabet
        
        Returns:
            str: Child alphabet
        """
        # Partially mapped crossover (PMX)
        start, end = sorted(random.sample(range(26), 2))
        child = [''] * 26
        
        # Copy segment from first parent
        child[start:end+1] = list(parent1[start:end+1])
        
        # Fill remaining positions
        for i in range(26):
            if child[i] == '':
                candidate = parent2[i]
                while candidate in child:
                    candidate = parent2[child.index(candidate)]
                child[i] = candidate
        
        return ''.join(child)
    
    def _mutate(self, alphabet: str) -> str:
        """
        Mutate an alphabet by swapping two random characters.
        
        Args:
            alphabet (str): Input alphabet
        
        Returns:
            str: Mutated alphabet
        """
        alphabet_list = list(alphabet)
        i, j = random.sample(range(26), 2)
        alphabet_list[i], alphabet_list[j] = alphabet_list[j], alphabet_list[i]
        return ''.join(alphabet_list)
    
    def evolve(self, generations: int = 1000) -> Tuple[str, float]:
        """
        Run the evolutionary algorithm to break the cipher.
        
        Args:
            generations (int): Number of generations to evolve
        
        Returns:
            Tuple[str, float]: Best alphabet and its fitness score
        """
        best_solution = None
        best_fitness = float('-inf')
        
        progress_bar = tqdm(range(generations))
        for gen in progress_bar:
            # Evaluate fitness of current population
            fitness_scores = [self._fitness(alpha) for alpha in self.population]
            
            # Find best solution in this generation
            current_best_idx = max(range(len(fitness_scores)), 
                                   key=lambda i: fitness_scores[i])
            current_best_fitness = fitness_scores[current_best_idx]
            current_best_solution = self.population[current_best_idx]
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_solution = current_best_solution
            
            # Update progress bar
            progress_bar.set_description(f"Best Score: {best_fitness:.2f}")
            
            # Selection: sort population by fitness
            sorted_population = [x for _, x in sorted(zip(fitness_scores, self.population), 
                                                      reverse=True)]
            
            # Create new population
            new_population = sorted_population[:self.elite_size]  # Elitism
            
            # Crossover and mutation
            while len(new_population) < self.population_size:
                # Tournament selection
                p1 = max(random.sample(sorted_population[:50], 3), 
                         key=lambda x: self._fitness(x))
                p2 = max(random.sample(sorted_population[:50], 3), 
                         key=lambda x: self._fitness(x))
                
                # Crossover
                child = self._crossover(p1, p2)
                
                # Mutation
                if random.random() < self.mutation_rate:
                    child = self._mutate(child)
                
                new_population.append(child)
            
            self.population = new_population
        
        return best_solution, best_fitness

def main():
    # Input handling
    if len(sys.argv) < 2:
        print("Usage: python script.py <encrypted_file>")
        sys.exit(1)
    
    # Load frequency dictionary
    with open('bigrams.json') as f:
        freq_orig = json.load(f)
    
    # Prepare frequency matrix
    freq = [[0] * 128 for _ in range(128)]
    for par, f in freq_orig.items():
        freq[ord(par[0])][ord(par[1])] = f
    
    # Read and preprocess encrypted text
    with open(sys.argv[1]) as f:
        orig_data = unidecode(f.read()).upper()
    
    # Filter to only uppercase letters
    data = ''.join(filter(lambda c: c in ascii_uppercase, orig_data))
    
    # Run evolutionary cipher breaker
    breaker = CipherBreaker(data, freq, 
                            population_size=100, 
                            mutation_rate=0.9, 
                            elite_size=3)
    best_alphabet, best_score = breaker.evolve(generations=100)
    
    # Output results
    print("\nBest Substitution Alphabet:")
    print(best_alphabet)
    print(f"\nBest Score: {best_score}")
    
    # Decrypt and print the original text
    decrypted_text = substitute(best_alphabet, orig_data)
    print("\nDecrypted Text:")
    print(decrypted_text)

if __name__ == "__main__":
    main()