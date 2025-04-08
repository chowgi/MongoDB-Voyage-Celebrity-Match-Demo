import face_recognition
from PIL import Image

# Load the image file
image_path = 'syd.webp'
image = face_recognition.load_image_file(image_path)

# Detect all face locations in the image
face_locations = face_recognition.face_locations(image)

# Define padding (in pixels)
padding = 50  # Adjust this value to increase/decrease padding

# Loop through each detected face
for i, (top, right, bottom, left) in enumerate(face_locations):
    # Add padding to all sides, making sure we don't exceed image boundaries
    height, width = image.shape[:2]
    top = max(0, top - padding)
    right = min(width, right + padding)
    bottom = min(height, bottom + padding)
    left = max(0, left - padding)

    face_image = image[top:bottom, left:right]  # Crop the face
    pil_image = Image.fromarray(face_image)
    pil_image.save(f'cropped_face.jpg')  # Save the cropped face
