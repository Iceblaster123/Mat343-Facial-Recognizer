import face_recognition
import numpy as np
import cv2
import os

# Dynamically build known images list from files in the images/ directory
image_dir = "images"
valid_exts = (".jpg", ".jpeg", ".png", ".bmp")

known_face_encodings = []
known_face_names = []

if not os.path.isdir(image_dir):
    print(f"Warning: '{image_dir}' directory not found. No known faces loaded.")
else:
    for fname in sorted(os.listdir(image_dir)):
        if not fname.lower().endswith(valid_exts):
            continue
        filepath = os.path.join(image_dir, fname)
        name = os.path.splitext(fname)[0]
        try:
            image = face_recognition.load_image_file(filepath)
            encodings = face_recognition.face_encodings(image)
            if not encodings:
                print(f"Warning: no face found in '{filepath}', skipping.")
                continue
            encoding = encodings[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)
            print(f"Loaded known face: {name} ({filepath})")
        except Exception as e:
            print(f"Error loading '{filepath}': {e}")


video = cv2.VideoCapture(0) # opens camera so we can see the video

if not video.isOpened(): # edge case catching
    print("Cannot open camera")
    exit()

while True:
    ret, frame = video.read()
    if not ret: # edge case catching
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 20, bottom - 6), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 1)

    # Show the output
    cv2.imshow('Video', frame)



    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'): # Press 'q' to quit
        print("Quiting...")
        break


video.release
cv2.destroyAllWindows