import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import keras.utils as image
import numpy as np
from keras.models import load_model

class ImageClassifierApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Classifier")
        self.geometry("400x300")

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

if __name__ == "__main__":
    app = ImageClassifierApp()
    app.mainloop()
