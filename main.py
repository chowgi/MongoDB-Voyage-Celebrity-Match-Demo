
from simple_image_download import simple_image_download as simp
import os

def download_celebrity_images(celebrity_names, num_images=3):
    response = simp.simple_image_download()
    response.thumbnails = False
    
    for celebrity in celebrity_names:
        print(f"Downloading {celebrity}...")
        try:
            # Download images
            images = response.download(celebrity, num_images)
            
            # Move images to celebrity-specific folder
            celebrity_dir = os.path.join("celebrity_images", celebrity)
            if not os.path.exists(celebrity_dir):
                os.makedirs(celebrity_dir)
            
            # Get the downloaded images and move them
            for img in images:
                if os.path.exists(img):
                    filename = os.path.basename(img)
                    new_path = os.path.join(celebrity_dir, filename)
                    os.rename(img, new_path)
            
            print(f"Successfully downloaded images for {celebrity}")
            
        except Exception as e:
            print(f"Error downloading images for {celebrity}: {str(e)}")

def main():
    # List of 100 celebrities
    celebrities = [
        "Tom Hanks", "Jennifer Lawrence", "Leonardo DiCaprio", "Meryl Streep",
        "Brad Pitt", "Angelina Jolie", "Morgan Freeman", "Julia Roberts",
        "Robert Downey Jr", "Scarlett Johansson", "Will Smith", "Emma Stone",
        "Johnny Depp", "Anne Hathaway", "Denzel Washington", "Sandra Bullock",
        "Chris Hemsworth", "Natalie Portman", "Tom Cruise", "Nicole Kidman",
        "Matt Damon", "Emma Watson", "George Clooney", "Charlize Theron",
        "Ryan Reynolds", "Jennifer Aniston", "Hugh Jackman", "Kate Winslet",
        "Chris Evans", "Margot Robbie", "Samuel L Jackson", "Cate Blanchett",
        "Christian Bale", "Amy Adams", "Mark Wahlberg", "Jennifer Lopez",
        "Benedict Cumberbatch", "Emily Blunt", "Dwayne Johnson", "Viola Davis",
        "Jake Gyllenhaal", "Rachel McAdams", "Michael B Jordan", "Jessica Chastain",
        "Chris Pratt", "Emma Thompson", "Idris Elba", "Zoe Saldana",
        "Ryan Gosling", "Penelope Cruz", "Matthew McConaughey", "Kate Hudson",
        "Daniel Craig", "Halle Berry", "Ben Affleck", "Michelle Williams",
        "Russell Crowe", "Reese Witherspoon", "Colin Firth", "Marion Cotillard",
        "Joaquin Phoenix", "Julianne Moore", "Michael Fassbender", "Naomi Watts",
        "Eddie Redmayne", "Alicia Vikander", "Tom Hardy", "Saoirse Ronan",
        "Jude Law", "Rachel Weisz", "Paul Rudd", "Eva Green",
        "Liam Neeson", "Helena Bonham Carter", "Gary Oldman", "Rose Byrne",
        "Oscar Isaac", "Kate Beckinsale", "Ralph Fiennes", "Emily VanCamp",
        "Joseph Gordon-Levitt", "Diane Kruger", "Ethan Hawke", "Elizabeth Banks",
        "Jeremy Renner", "Olivia Wilde", "Viggo Mortensen", "Gemma Arterton",
        "Josh Brolin", "Rebecca Ferguson", "Joel Edgerton", "Rosamund Pike",
        "Chiwetel Ejiofor", "Carey Mulligan", "Mahershala Ali", "Brie Larson",
        "Sam Rockwell", "Tilda Swinton", "Daniel Kaluuya", "Lupita Nyong'o",
        "Willem Dafoe", "Sally Hawkins", "Richard Madden", "Florence Pugh"
    ]
    
    # Create main output directory if it doesn't exist
    if not os.path.exists("celebrity_images"):
        os.makedirs("celebrity_images")
    
    # Download images for each celebrity
    download_celebrity_images(celebrities)

if __name__ == "__main__":
    main()
