import sys
import cv2


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Accept optional filename from command-line argument
filename_arg = None
if len(sys.argv) > 1:
    filename_arg = sys.argv[1]

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot open camera, please give permission!")
        break

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        # Use passed filename if available, otherwise ask in terminal
        if filename_arg:
            filename = filename_arg
        else:
            filename = input("Please enter the person's name: ")
        cv2.imwrite(f"images/{filename}.png", frame)
        print(f"Saved {filename}.png")

    elif key == ord('q'):
        # Quit the loop
        print("Quitting...")
        break

cap.release()
cv2.destroyAllWindows()
