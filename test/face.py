import PIL.Image
import PIL.ImageDraw
import face_recognition
import os

# Modify your path here
image_path = os.getcwd()+"/image/image01.jpg"

# Load the file into a numpy array
given_image = face_recognition.load_image_file(image_path)

# Find all the faces in the image
face_locations = face_recognition.face_locations(given_image)

number_of_faces = len(face_locations)
print("We found {} face(s) in this image.".format(number_of_faces))

# Load the image into a Python Image Library object
pil_image = PIL.Image.fromarray(given_image)

for face_location in face_locations:
    # Print the location of each face in this image
    top, left, bottom, right = face_location
    print("A face is detected at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    # Draw a box around the face
    draw = PIL.ImageDraw.Draw(pil_image)
    draw.rectangle([left, top, right, bottom], outline="red", width=3)

# Display the image on screen with detected faces
pil_image.show()