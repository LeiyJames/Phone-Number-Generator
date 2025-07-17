import csv
import random
import os
from typing import List, Dict

# SIM Prefixes mapping with network names (for reference only)
SIM_PREFIXES: Dict[str, List[str]] = {
    "Globe/TM": ["905", "906", "915", "916", "917", "926", "927", "935", "936", "945"],
    "Smart": ["908", "918", "919", "920", "921", "928", "929", "939", "946", "947", "949"],
    "TNT": ["907", "909", "910", "912", "930", "938", "946", "948", "950"],
    "Smart/TNT": ["907", "908", "909", "910", "912", "913", "914"],
    "Sun": ["922", "923", "924", "925", "931", "932", "932", "934", "940", "941", "942"]
}

def generate_invalid_number() -> str:
    """Generate an invalid Philippine mobile number with various patterns"""
    patterns = [
        # Wrong country code (not 63)
        lambda: f"6{random.randint(0, 5)}{''.join([str(random.randint(0, 9)) for _ in range(9)])}",
        # Wrong length (not 11 digits)
        lambda: f"63{random.randint(1, 9)}{''.join([str(random.randint(0, 9)) for _ in range(8)])}",
        # Invalid prefix (000, 111, 222)
        lambda: f"63{random.choice(['000', '111', '222'])}{''.join([str(random.randint(0, 9)) for _ in range(7)])}",
        # Completely random digits
        lambda: ''.join([str(random.randint(0, 9)) for _ in range(random.randint(8, 15))]),
        # Valid format but invalid carrier prefix
        lambda: f"63{random.choice(['000', '123', '555'])}{''.join([str(random.randint(0, 9)) for _ in range(7)])}",
        # Numbers with letters/special characters
        lambda: f"63{random.choice(['81', '90', '91'])}" + \
                ''.join(random.choice('abcdefghijABCDEFGHIJ!@#$%^&*()') for _ in range(7)),
        # Valid prefix but wrong structure
        lambda: f"63{random.choice(random.choice(list(SIM_PREFIXES.values())))}{''.join(random.choice('ABCD!@#$') for _ in range(7))}"
    ]
    return random.choice(patterns)()

def generate_unique_invalid_numbers(count: int) -> List[str]:
    """Generate unique invalid numbers"""
    numbers = set()
    while len(numbers) < count:
        numbers.add(generate_invalid_number())
    return list(numbers)

def save_to_csv(filename: str, numbers: List[str]) -> bool:
    """Save numbers to CSV (one per row, no headers)"""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows([[num] for num in numbers])
        return True
    except Exception as e:
        print(f"ERROR: Failed to save {filename}\n{type(e).__name__}: {e}")
        return False

def main():
    # ===== USER CONFIGURATION =====
    # 1. Set total number of invalid numbers to generate
    TOTAL_NUMBERS = 25
    
    # 2. Custom CSV filename (optional)
    CUSTOM_FILENAME = "Invalid_25.csv" 
    # =============================
    
    # Generate unique invalid numbers
    print(f"\nGenerating {TOTAL_NUMBERS} unique invalid numbers...")
    numbers = generate_unique_invalid_numbers(TOTAL_NUMBERS)
    
    # Set filename
    if not CUSTOM_FILENAME:
        CUSTOM_FILENAME = f"Invalid_Numbers_{TOTAL_NUMBERS}.csv"
    
    # Save to CSV
    output_dir = os.path.join(os.path.dirname(__file__), "Invalid_Numbers")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, CUSTOM_FILENAME)
    
    if save_to_csv(filepath, numbers):
        # Verification
        print(f"\n✅ Successfully created: {CUSTOM_FILENAME}")
        print(f"📁 Location: {os.path.abspath(filepath)}")
        print(f"🔢 Total invalid numbers: {len(numbers)}")
        print(f"🌟 All numbers are unique: {len(numbers) == len(set(numbers))}")
        
        # Sample output
        print("\n🔍 Sample invalid numbers:")
        print("First 5:", numbers[:5])
    else:
        print("\n❌ Failed to create file. Check errors above.")

if __name__ == "__main__":
    main()