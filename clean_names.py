
import json

def clean_names():
    # Read the names from the file
    with open('names.txt', 'r') as file:
        names = json.loads(file.read())

    # Create a set to track unique names (case-insensitive)
    unique_names = set()
    cleaned_names = []
    removed_names = []

    for name in names:
        # Convert to lower case for comparison
        name_lower = name.lower()
        
        # Check if it's a single name
        if len(name.split()) < 2:
            removed_names.append(f"{name} (single name)")
            continue
            
        # Check for duplicates
        if name_lower in unique_names:
            removed_names.append(f"{name} (duplicate)")
            continue
            
        unique_names.add(name_lower)
        cleaned_names.append(name)

    # Save the cleaned names back to names.txt
    with open('names.txt', 'w') as file:
        json.dump(cleaned_names, file, indent=2)

    # Print summary
    print(f"Original count: {len(names)}")
    print(f"Cleaned count: {len(cleaned_names)}")
    print("\nRemoved names:")
    for name in removed_names:
        print(f"- {name}")

if __name__ == "__main__":
    clean_names()
