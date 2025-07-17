import csv
import random
import string
from typing import List, Dict

# SIM Prefixes mapping with network names in descending priority order
SIM_PREFIXES: Dict[str, List[str]] = {
    "Globe/TM": ["905", "906", "915", "916", "917", "926", "927", "935", "936", "945"],
    "Smart": ["908", "918", "919", "920", "921", "928", "929", "939", "946", "947", "949"],
    "TNT": ["907", "909", "910", "912", "930", "938", "946", "948", "950"],
    "Smart/TNT": ["907", "908", "909", "910", "912", "913", "914"],
    "Sun": ["922", "923", "924", "925", "931", "932", "932", "934", "940", "941", "942"]
}

def generate_valid_number(prefix: str) -> str:
    """Generate a valid Philippine mobile number (63 + prefix + 7 digits)"""
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"63{prefix}{suffix}"

def generate_invalid_number() -> str:
    """Generate an invalid Philippine mobile number with various patterns"""
    patterns = [
        # Wrong length (not 11 digits)
        lambda: f"63{random.randint(1, 9)}{''.join([str(random.randint(0, 9)) for _ in range(8)])}",
        # Wrong country code (not 63)
        lambda: f"6{random.randint(0, 5)}{''.join([str(random.randint(0, 9)) for _ in range(9)])}",
        # Invalid prefix (000, 111, 222)
        lambda: f"63{random.choice(['000', '111', '222'])}{''.join([str(random.randint(0, 9)) for _ in range(7)])}",
        # Completely random digits
        lambda: ''.join([str(random.randint(0, 9)) for _ in range(12)]),
        # Numbers with letters mixed in
        lambda: f"63{random.choice(['81', '90', '91'])}" + \
               ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))
    ]
    return random.choice(patterns)()

def generate_mixed_numbers(valid_count: int, invalid_count: int) -> List[List[str]]:
    """Generate numbers with valid first, then invalid"""
    numbers = []
    all_prefixes = [p for network in SIM_PREFIXES.values() for p in network]
    
    # Generate VALID numbers (first segment)
    valid_numbers = [
        [generate_valid_number(random.choice(all_prefixes))] 
        for _ in range(valid_count)
    ]
    
    # Generate INVALID numbers (second segment)
    invalid_numbers = [
        [generate_invalid_number()] 
        for _ in range(invalid_count)
    ]
    
    # Combine (valid first, then invalid)
    numbers = valid_numbers + invalid_numbers
    return numbers

def save_to_csv(filename: str, numbers: List[List[str]]):
    """Save numbers to CSV (no headers)"""
    with open(filename, 'w', newline='') as f:
        csv.writer(f).writerows(numbers)

def main():
    # CONFIGURATION
    CONTACTS_PER_FILE = 100   # Total numbers per file
    INVALID_COUNT = 50        # Invalid numbers per file
    NUMBER_OF_FILES = 1      # Files to generate
    
    print(f"Creating {NUMBER_OF_FILES} files with:")
    print(f"- First {CONTACTS_PER_FILE - INVALID_COUNT} valid numbers")
    print(f"- Last {INVALID_COUNT} invalid numbers (some with letters)\n")
    
    for i in range(1, NUMBER_OF_FILES + 1):
        nums = generate_mixed_numbers(
            valid_count=CONTACTS_PER_FILE - INVALID_COUNT,
            invalid_count=INVALID_COUNT
        )
        save_to_csv(f"ValidFirst_InvalidLast_{i}.csv", nums)
        
        # Print sample output
        print(f"\nGenerated ValidFirst_InvalidLast_{i}.csv")
        print("First 5 (valid):", [n[0] for n in nums[:5]])
        print("Last 5 (invalid):", [n[0] for n in nums[-5:]])
    
    print("\nDone! Files have valid numbers first, followed by invalid numbers.")

if __name__ == "__main__":
    main()