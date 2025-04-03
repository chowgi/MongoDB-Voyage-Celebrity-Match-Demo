import face_recognition
from PIL import Image

# Load the image file
image_path = 'Anne.jpg'
image = face_recognition.load_image_file(image_path)

# Detect all face locations in the image
face_locations = face_recognition.face_locations(image)

# Loop through each detected face
for i, (top, right, bottom, left) in enumerate(face_locations):
    face_image = image[top:bottom, left:right]  # Crop the face
    pil_image = Image.fromarray(face_image)
    pil_image.save(f'cropped_face_{i}.jpg')  # Save the cropped face