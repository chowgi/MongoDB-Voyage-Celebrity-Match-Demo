
# MongoDB and Voyage Celebrity Look-Alike Finder

Demo application that highlights MongoDB Atlas Vector Search and Voyage AI's multimodal embeddings. Designed as a technical showcase, this demo leverages advanced AI technologies to match user inputs with celebrity profiles. Please note that this is solely a demonstration, and the results may vary.

## Try it Live!

You can "remix"try the app directly on Replit here:
[https://replit.com/@BenKarciauskas/MongoDB-Avoyage-Celebrity-Match-Demo?v=1#main.py]

## Features

- Upload photos or take pictures with your webcam
- Advanced facial recognition and vector embedding
- Real-time similarity matching with a database of celebrity images
- Shows top 3 celebrity matches with similarity percentages

## Tech Stack

- Replit (hosting and dependancies)
- Flask (Python web framework)
- MongoDB Atlas (Vector database)
- VoyageAI (Vector embeddings)
- Face Recognition library
- HTML/CSS/JavaScript (Frontend)

## Setup Instructions

1. Create a MongoDB Atlas account and get your connection string
2. Set up environment variables in Replit:
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `VOYAGE_API_KEY`: Your Voyage AI API key for creating image embeddings

3. Install dependencies (automatically handled by Replit)

4. Load the celebrity database:
```bash
python load_data.py
```

5. Run the application:
```bash
python main.py
```

The app will be available at `http://0.0.0.0:5000`

## How it Works

1. When you upload an image or take a photo, the app processes it using facial recognition
2. The image is converted into a vector embedding using VoyageAI
3. MongoDB Atlas Vector Search finds the most similar celebrity faces
4. The top 3 matches are displayed with similarity percentages