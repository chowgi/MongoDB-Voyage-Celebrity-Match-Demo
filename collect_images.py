
from bing_image_downloader import downloader
import boto3
import os
import time
import requests
from io import BytesIO

def upload_to_s3(image_data, bucket_name, key_name, s3_client):
    try:
        s3_client.put_object(Bucket=bucket_name, Key=key_name, Body=image_data)
        return True
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        return False

def download_celebrity_images(celebrity_names, num_images=3):
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ['aws_access_key'],
        aws_secret_access_key=os.environ['aws_secret_key'],
        region_name="ap-south-1"
    )
    bucket_name = 'celeb-images-demo'

    def celebrity_exists(celebrity):
        try:
            # List objects with celebrity name prefix
            response = s3_client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=f"{celebrity}/",
                MaxKeys=1
            )
            # If any objects exist with this prefix, the celebrity folder exists
            return 'Contents' in response
        except Exception:
            return False

    for celebrity in celebrity_names:
        if celebrity_exists(celebrity):
            print(f"Skipping {celebrity} - Images already exist in S3")
            continue

        print(f"Downloading {celebrity}...")
        try:
            # Use Bing downloader to get image URLs
            downloaded_images = downloader.download(
                celebrity,
                limit=num_images,
                output_dir="temp_images",
                adult_filter_off=False,
                force_replace=False,
                timeout=60,
                verbose=True
            )

            # Upload each image to S3
            for i, image_path in enumerate(os.listdir(f"temp_images/{celebrity}")):
                full_path = f"temp_images/{celebrity}/{image_path}"
                with open(full_path, 'rb') as img_file:
                    s3_key = f"{celebrity}/image_{i+1}.jpg"
                    if upload_to_s3(img_file.read(), bucket_name, s3_key, s3_client):
                        print(f"Successfully uploaded {s3_key} to S3")
                os.remove(full_path)  # Clean up local file

            # Clean up temp directory
            os.rmdir(f"temp_images/{celebrity}")
            print(f"Successfully processed images for {celebrity}")
            time.sleep(1)  # Small delay between celebrities

        except Exception as e:
            print(f"Error processing images for {celebrity}: {str(e)}")

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

    # Create temp directory if it doesn't exist
    if not os.path.exists("temp_images"):
        os.makedirs("temp_images")

    # Download and upload images for each celebrity
    download_celebrity_images(celebrities)

    # Clean up temp directory
    if os.path.exists("temp_images"):
        os.rmdir("temp_images")

if __name__ == "__main__":
    main()
