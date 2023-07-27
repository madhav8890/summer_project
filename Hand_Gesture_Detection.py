import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import keras.utils as image
import numpy as np
from keras.models import load_model9886905
from cvzone.HandTrackingModule import HandDetector
import cv2
import os

class ImageClassifierApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Service Runner")
        self.geometry("400x300")

        # Load Image Classifier Model
        self.image_model = load_model("imageclassifier.h5")

        # Create Hand Detector
        self.hand_detector = HandDetector(maxHands=1)

        # Create GUI elements
        self.service_label = tk.Label(self, text="Select a service to run:", font=("Helvetica", 16))
        self.service_label.pack(pady=20)

        self.image_button = tk.Button(self, text="Image Classifier", command=self.run_image_classifier)
        self.image_button.pack(pady=10)

        self.hand_button = tk.Button(self, text="Hand Gesture Detection", command=self.run_hand_detector)
        self.hand_button.pack(pady=10)

    def run_image_classifier(self):
        self.destroy()  # Close the current GUI window
        ImageClassifierGUI().mainloop()  # Open the Image Classifier GUI

    def run_hand_detector(self):
        self.destroy()  # Close the current GUI window
        HandDetectorGUI().mainloop()  # Open the Hand Gesture Detection GUI


class ImageClassifierGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Classifier")
        self.geometry("400x400")

        self.model = load_model("imageclassifier.h5")

        self.image_label = tk.Label(self, text="Upload an image for classification", font=("Helvetica", 16))
        self.image_label.pack(pady=20)

        self.upload_button = tk.Button(self, text="Upload Image", command=self.open_image)
        self.upload_button.pack()

        self.result_label = tk.Label(self, text="", font=("Helvetica", 20))
        self.result_label.pack(pady=20)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((256, 256))
            image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=image)
            self.image_label.image = image

            self.classify_image(file_path)

    def classify_image(self, file_path):
        test_img = image.load_img(file_path, target_size=(256, 256))
        test_img = image.img_to_array(test_img)
        test_img = np.expand_dims(test_img, axis=0)

        result = self.model.predict(test_img)
        sad_probability = result[0][0]

        if sad_probability > 0.5:
            self.result_label.configure(text="Sad")
        else:
            self.result_label.configure(text="Happy")


class HandDetectorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hand Gesture Detection")
        self.geometry("400x300")

        self.hand_detector = HandDetector(maxHands=1)

        self.hand_label = tk.Label(self, text="Perform hand gestures in front of the camera", font=("Helvetica", 16))
        self.hand_label.pack(pady=20)

        self.result_label = tk.Label(self, text="", font=("Helvetica", 20))
        self.result_label.pack(pady=20)

        self.back_button = tk.Button(self, text="Back", command=self.back_to_main)
        self.back_button.pack(pady=10)

        self.start_hand_detection()

    def start_hand_detection(self):
        cap = cv2.VideoCapture(0)
        while True:
            status, photo = cap.read()
            hand = self.hand_detector.findHands(photo, draw=False)

            if hand:
                total_finger = self.hand_detector.fingersUp(hand[0])

                if total_finger == [1, 0, 0, 0, 0]:
                    self.result_label.configure(text="Thumbs Up")
                elif total_finger == [0, 1, 0, 0, 0]:
                    self.result_label.configure(text="Index Finger")
                elif total_finger == [0, 0, 1, 0, 0]:
                    self.result_label.configure(text="Middle Finger")
                else:
                    self.result_label.configure(text="Nothing")

            cv2.imshow("Hand Detection", photo)
            if cv2.waitKey(1) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def back_to_main(self):
        self.destroy()  # Close the current GUI window
        ImageClassifierApp().mainloop()  # Return to the main Service Runner GUI


if __name__ == "__main__":
    app = ImageClassifierApp()
    app.mainloop()
