import csv
import random
import os
from typing import List, Dict
from faker import Faker

# Initialize Faker
fake = Faker()

# SIM Prefixes mapping with network names
SIM_PREFIXES: Dict[str, List[str]] = {
    "Globe/TM": ["905", "906", "915", "916", "917", "926", "927", "935", "936", "945"],
    "Smart": ["908", "918", "919", "920", "921", "928", "929", "939", "946", "947", "949"],
    "TNT": ["907", "909", "910", "912", "930", "938", "946", "948", "950"],
    "Smart/TNT": ["907", "908", "909", "910", "912", "914"],
    "Sun": ["922", "923", "924", "925", "931", "932", "932", "934", "941", "942"]
}

def generate_ph_number(prefix: str) -> str:
    """Generate a PH number (0 + prefix + 7 random digits)"""
    return f"0{prefix}{''.join([str(random.randint(0, 9)) for _ in range(7)])}"

def generate_contact_row(prefix: str) -> str:
    """Generate a contact row matching Book1.csv format"""
    first_name = fake.first_name()
    middle_name = fake.random_letter().upper()  # Single initial like in your example
    last_name = fake.last_name()
    mobile_number = generate_ph_number(prefix)
    company = fake.company().replace(",", "")  # Remove commas to match your format
    position = fake.job().replace(",", "")
    department = random.choice(["Sales", "Marketing", "IT", "HR", "Finance", "Operations", 
                              "R&D", "Logistics", "Admin", "Support", "Legal", "Strategy",
                              "Management", "Production", "Creative", "Research", "Development"])
    email = f"{first_name.lower()}.{last_name.lower()}@{company.replace(' ', '').lower()}.com"
    city = fake.city()
    address = f"{random.randint(1, 999)} {fake.street_name()}, {city}"
    
    # Format exactly like Book1.csv
    return f"{first_name}|{middle_name}|{last_name}|{mobile_number}|{company}|{position}|{department}|{email}|{address}"

def generate_contacts_with_distribution(
    network_counts: Dict[str, int],
    duplicates: int
) -> List[str]:
    """Generate contacts with exact distribution per network + duplicates"""
    contacts = []
    
    # Generate unique contacts per network
    for network, count in network_counts.items():
        if network not in SIM_PREFIXES:
            raise ValueError(f"Unknown network: {network}")
        for _ in range(count):
            prefix = random.choice(SIM_PREFIXES[network])
            contacts.append(generate_contact_row(prefix))
    
    # Add duplicates (from the start to maintain priority)
    contacts.extend(contacts[:duplicates])
    return contacts

def save_to_csv(filename: str, contacts: List[str]) -> bool:
    """Save contacts to CSV (one per row, no headers)"""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            f.write("\n".join(contacts))
        return True
    except Exception as e:
        print(f"ERROR: Failed to save {filename}\n{type(e).__name__}: {e}")
        return False

def main():
    # ===== USER CONFIGURATION =====
    # 1. Set counts per network (adjusted to match your sample size)
    NETWORK_COUNTS = {
        "Globe/TM": 2,
        "Smart": 2,
        "TNT": 2,
        "Smart/TNT": 2,
        "Sun": 2
    }
    
    # 2. Set number of duplicates
    DUPLICATES = 5
    
    # 3. Custom CSV filename
    CUSTOM_FILENAME = "Duplicate_5i.csv" 
    # =============================
    
    # Generate contacts
    contacts = generate_contacts_with_distribution(NETWORK_COUNTS, DUPLICATES)
    
    # Save to CSV
    output_dir = os.path.join(os.path.dirname(__file__), "Output")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, CUSTOM_FILENAME)
    
    if save_to_csv(filepath, contacts):
        print(f"\n✅ Successfully created: {CUSTOM_FILENAME}")
        print(f"📁 Location: {os.path.abspath(filepath)}")
        print(f"👥 Total contacts: {len(contacts)}")
        
        # Sample output
        print("\n🔍 Sample contacts (first 5):")
        for contact in contacts[:5]:
            print(contact)
    else:
        print("\n❌ Failed to create file.")

if __name__ == "__main__":
    main()