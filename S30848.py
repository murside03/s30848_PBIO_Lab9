# Album number: s12345
# Date: 2026-05-05
# Description: Random DNA sequence generator in FASTA format.
#              Supports statistics, name embedding, and extra features.

import random
import csv


def generate_sequence(length: int) -> str:
    """Returns a random DNA sequence of the specified length."""
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choice(nucleotides) for _ in range(length))


def calculate_stats(sequence: str) -> dict:
    """Returns a dictionary of sequence statistics.

    Keys: 'A', 'C', 'G', 'T' (float values, %),
          'GC' (float value, %).
    """
    n = len(sequence)
    stats = {}
    for nuc in ['A', 'C', 'G', 'T']:
        stats[nuc] = round((sequence.count(nuc) / n) * 100, 2)
    stats['gc_ratio_A'] = round(stats['G'] + stats['C'], 2)
    return stats

def validate_positive_int(prompt: str,
                           min_val: int = 1,
                           max_val: int = 100_000) -> int:
    """Gets an integer from the user in a range.
    In case of an error, repeats the question.
    """
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
        except ValueError:
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")


def insert_name(sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence.
    Name written in lowercase letters so it is visually distinguishable.
    """
    position = random.randint(0, len(sequence))
    return sequence[:position] + name.lower() + sequence[position:]


def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    """Returns a formatted FASTA record as a string.
    Header starts with '>', sequence is split into lines of line_width chars.
    """
    header = f">{seq_id}"
    if description:
        header += f" {description}"
    lines = [sequence[i:i + line_width] for i in range(0, len(sequence), line_width)]
    return header + '\n' + '\n'.join(lines) + '\n'


def find_motif(sequence: str, motif: str) -> list:
    """Finds all positions of a motif in the sequence.
    Returns list of positions using 1-based biological indexing.
    """
    positions = []
    start = 0
    motif = motif.upper()
    while True:
        pos = sequence.find(motif, start)
        if pos == -1:
            break
        positions.append(pos + 1)
        start = pos + 1
    return positions

def complement(sequence: str) -> str:
    """Returns the complementary DNA strand.
    A<->T, C<->G pairing rules applied.
    """
    mapping = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(mapping.get(nuc, nuc) for nuc in sequence)


def reverse_complement(sequence: str) -> str:
    """Returns the reverse complementary DNA strand.
    Complement is computed first, then reversed.
    """
    return complement(sequence)[::-1]


def transcribe(sequence: str) -> str:
    """Transcribes DNA to mRNA by replacing T with U."""
    return sequence.replace('T', 'U')


def sliding_window_gc(sequence: str, window_size: int, step: int = 1) -> list:
    """Calculates GC content in a sliding window.
    Returns list of (start_position, gc_content) tuples.
    Start positions use 1-based biological indexing.
    """
    results = []
    for i in range(0, len(sequence) - window_size + 1, step):
        window = sequence[i:i + window_size]
        gc = round((window.count('G') + window.count('C')) / window_size * 100, 2)
        results.append((i + 1, gc))
    return results


def save_sliding_window_csv(data: list, filename: str) -> None:
    """Saves sliding window GC content data to a CSV file.
    Columns: start_position, gc_content.
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['start_position', 'gc_content'])
        writer.writerows(data)

def main():
    """Main program flow. — TODO"""
    pass


if __name__ == "__main__":
    main()