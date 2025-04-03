
import json

def clean_names():
    try:
        # Read the names from the file
        with open('names.txt', 'r') as file:
            content = file.read().strip()
            # Remove any trailing commas before closing bracket
            if content.endswith(',]'):
                content = content[:-2] + ']'
            names = json.loads(content)

        # Create a set to track unique names (case-insensitive)
        unique_names = set()
        cleaned_names = []
        removed_names = []

        for name in names:
            if not isinstance(name, str):
                continue
                
            # Strip whitespace and normalize
            name = name.strip()
            
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

    except Exception as e:
        print(f"Error processing names: {str(e)}")
        print("Please check the names.txt file for any formatting issues")

if __name__ == "__main__":
    clean_names()
