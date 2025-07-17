import csv
import random
import os
from typing import List, Dict, Optional

# SIM Prefixes mapping with network names
SIM_PREFIXES: Dict[str, List[str]] = {
    "Globe/TM": ["905", "906", "915", "916", "917", "926", "927", "935", "936", "945"],
    "Smart": ["908", "918", "919", "920", "921", "928", "929", "939", "946", "947", "949"],
    "TNT": ["907", "909", "910", "912", "930", "938", "946", "948", "950"],
    "Smart/TNT": ["907", "908", "909", "910", "912", "913", "914"],
    "Sun": ["922", "923", "924", "925", "931", "932", "932", "934", "940", "941", "942"]
}

def generate_ph_number(prefix: str) -> str:
    """Generate a PH number (63 + prefix + 7 random digits)"""
    return f"63{prefix}{''.join(str(random.randint(0, 9)) for _ in range(7))}" 

def generate_numbers_with_distribution(
    network_counts: Dict[str, int],
    duplicates: int
) -> List[str]:
    """Generate numbers with exact distribution per network + duplicates"""
    numbers = []
    
    # Generate unique numbers per network
    for network, count in network_counts.items():
        if network not in SIM_PREFIXES:
            raise ValueError(f"Unknown network: {network}")
        for _ in range(count):
            prefix = random.choice(SIM_PREFIXES[network])
            numbers.append(generate_ph_number(prefix))
    
    # Add duplicates (from the start to maintain priority)
    numbers.extend(numbers[:duplicates])
    return numbers

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
    # 1. Set EXACT counts per network (adjust these numbers)
    NETWORK_COUNTS = {
        "Globe/TM": 200,   #  Globe/TM numbers
        "Smart": 200,      #  Smart numbers
        "TNT": 200,        #  TNT numbers
        "Smart/TNT": 200,   #  Smart/TNT numbers
        "Sun": 200        #  Sun numbers
    }
    
    # 2. Set number of duplicates (e.g., 50 duplicates of the first 50 numbers)
    DUPLICATES = 500
    
    # 3. Custom CSV filename (optional, auto-generates if None)
    CUSTOM_FILENAME = "Duplicate_500.csv" 
    # =============================
    
    # Generate numbers
    unique_numbers = sum(NETWORK_COUNTS.values())
    total_numbers = unique_numbers + DUPLICATES
    numbers = generate_numbers_with_distribution(NETWORK_COUNTS, DUPLICATES)
    
    # Auto-generate filename if not provided
    if not CUSTOM_FILENAME:
        CUSTOM_FILENAME = "_".join(
            f"{network}_{count}" 
            for network, count in NETWORK_COUNTS.items()
        ) + f"_dup_{DUPLICATES}.csv"
    
    # Save to CSV
    output_dir = os.path.join(os.path.dirname(__file__), "Duplicate")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, CUSTOM_FILENAME)
    
    if save_to_csv(filepath, numbers):
        # Verification
        unique_set = set(numbers)
        print(f"\n✅ Successfully created: {CUSTOM_FILENAME}")
        print(f"📁 Location: {os.path.abspath(filepath)}")
        print(f"🔢 Total numbers: {len(numbers)} (Expected: {total_numbers})")
        print(f"🌟 Unique numbers: {len(unique_set)} (Expected: {unique_numbers})")
        print(f"♻️ Duplicates: {len(numbers) - len(unique_set)} (Expected: {DUPLICATES})")
        
        # Network distribution
        print("\n📶 Network distribution (unique numbers):")
        for network, count in NETWORK_COUNTS.items():
            print(f"  - {network}: {count} numbers")
        
        # Sample output
        print("\n🔍 Sample numbers:")
        print("First 3:", numbers[:3])
        print("Last 3 (duplicates):", numbers[-3:])
    else:
        print("\n❌ Failed to create file. Check errors above.")

if __name__ == "__main__":
    main()