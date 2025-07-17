import csv
import random
from typing import List

# SIM Prefixes mapping with network names in descending priority order
SIM_PREFIXES: dict[str, List[str]] = {
    "Globe/TM": ["905", "906", "915", "916", "917", "926", "927", "935", "936", "945"],
    "Smart": ["908", "918", "919", "920", "921", "928", "929", "939", "946", "947", "949"],
    "TNT": ["907", "909", "910", "912", "930", "938", "946", "948", "950"],
    "Smart/TNT": ["907", "908", "909", "910", "912", "913", "914"],
    "Sun": ["922", "923", "924", "925", "931", "932", "932", "934", "940", "941", "942"]
}

def generate_ph_number(prefix: str) -> str:
    """Generate a random Philippine mobile number (63 + prefix + 7 random digits)"""
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"63{prefix}{suffix}"

def generate_mixed_numbers(total_numbers: int) -> List[List[str]]:
    """Generate numbers from ALL networks (randomly mixed)"""
    numbers = []
    all_prefixes = []
    
    # Combine all prefixes into one list
    for network in SIM_PREFIXES:
        all_prefixes.extend(SIM_PREFIXES[network])
    
    # Generate random numbers
    for _ in range(total_numbers):
        prefix = random.choice(all_prefixes)  # Randomly pick any prefix
        number = generate_ph_number(prefix)
        numbers.append([number])  # CSV format: 1 number per row
    
    return numbers

def save_to_csv(filename: str, numbers: List[List[str]]):
    """Save numbers to a CSV file"""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(numbers)

def main():
    # CONFIGURATION (Change as needed)
    CONTACTS_PER_FILE = 20 # Numbers per file
    NUMBER_OF_FILES = 1       # How many CSV files to generate
    
    print(f"Generating {NUMBER_OF_FILES} files with {CONTACTS_PER_FILE} mixed numbers each...")
    
    for file_num in range(1, NUMBER_OF_FILES + 1):
        numbers = generate_mixed_numbers(CONTACTS_PER_FILE)
        filename = f"Valid_{file_num}.csv"
        save_to_csv(filename, numbers)
        print(f"Created {filename}")

    print("Done!")

if __name__ == "__main__":
    main()