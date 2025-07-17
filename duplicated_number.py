import csv
import random
import os
from typing import List, Dict

# SIM Prefixes mapping with network names in descending priority order
SIM_PREFIXES: Dict[str, List[str]] = {
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

def generate_mixed_numbers(unique_numbers: int, duplicates: int) -> List[str]:
    """Generate numbers with ordered duplicates, maintaining network priority and accurate prefix representation"""
    numbers = []
    network_order = ["Globe/TM", "Smart", "TNT", "Smart/TNT", "Sun"]  # Strict priority order
    
    # First, ensure we have at least one number from each prefix in each network
    prefix_samples = []
    for network in network_order:
        for prefix in SIM_PREFIXES[network]:
            prefix_samples.append((network, prefix))
    
    # Add these prefix samples first
    for network, prefix in prefix_samples:
        if len(numbers) >= unique_numbers:
            break
        numbers.append(generate_ph_number(prefix))
    
    # Then fill the rest with random prefixes from any network (maintaining priority)
    for network in network_order:
        if len(numbers) >= unique_numbers:
            break
        prefixes = SIM_PREFIXES[network]
        while len(numbers) < unique_numbers and prefixes:
            prefix = random.choice(prefixes)
            numbers.append(generate_ph_number(prefix))
    
    # Duplicate the first 'duplicates' numbers (highest priority)
    numbers.extend(numbers[:duplicates])
    return numbers

def save_to_csv(filename: str, numbers: List[str]) -> bool:
    """Save numbers to a CSV file (one number per row, no headers)"""
    try:
        dirname = os.path.dirname(filename)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for number in numbers:
                writer.writerow([number])
        
        if not os.path.exists(filename):
            raise RuntimeError("File creation failed silently")
        
        return True
    except Exception as e:
        print(f"\nERROR: Failed to save {filename}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"Attempted path: {os.path.abspath(filename)}")
        return False

def main():
    # Configuration
    CONTACTS_PER_FILE = 1000  # Total numbers (50 unique + 50 duplicates)
    DUPLICATES = 500        # Exact number of duplicates
    UNIQUE_NUMBERS = CONTACTS_PER_FILE - DUPLICATES  # 50 unique
    
    # Save in the same folder as the script
    output_dir = os.path.join(os.path.dirname(__file__), 'Duplicate')
    os.makedirs(output_dir, exist_ok=True)  # Create folder if missing
    
    print(f"Generating 1 file with {CONTACTS_PER_FILE} numbers (50 unique + 50 duplicates)...")
    print(f"Network priority: Globe/TM → Smart → TNT → Smart/TNT → Sun")
    
    numbers = generate_mixed_numbers(UNIQUE_NUMBERS, DUPLICATES)
    filename = os.path.join(output_dir, "Schedule_1.csv") #Change the file name as needed
    
    if save_to_csv(filename, numbers):
        # Verification
        unique_set = set(numbers)
        print(f"\nSuccessfully created: {filename}")
        print(f"File location: {os.path.abspath(filename)}")
        print(f"Total numbers: {len(numbers)} (Expected: {CONTACTS_PER_FILE})")
        print(f"Unique numbers: {len(unique_set)} (Expected: {UNIQUE_NUMBERS})")
        print(f"Duplicates: {len(numbers) - len(unique_set)} (Expected: {DUPLICATES})")
        
        # Print sample numbers (first 3 and last 3)
        print("\nSample numbers:")
        print("First 3 unique:", numbers[:3])
        print("Last 3 (duplicates):", numbers[-3:])
        
        # Print network distribution
        print("\nNetwork distribution in unique numbers:")
        network_counts = {network: 0 for network in SIM_PREFIXES}
        for number in unique_set:
            prefix = number[2:5]  # Extract the prefix (after '63')
            for network, prefixes in SIM_PREFIXES.items():
                if prefix in prefixes:
                    network_counts[network] += 1
                    break
        for network, count in network_counts.items():
            print(f"{network}: {count} numbers")
    else:
        print("\nFailed to create file. Please check error messages above.")

if __name__ == "__main__":
    main()