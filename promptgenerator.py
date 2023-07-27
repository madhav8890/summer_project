import tkinter as tk
from tkinter import messagebox
import openai

# Set your GPT-3 API key here
api_key = "your_api_key"
openai.api_key = api_key

def generate_prompt(topic):
    prompt = f"Write a creative writing prompt about {topic}."
    return prompt

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
    )
    return response.choices[0].text.strip()

def generate_prompt_and_response():
    topic = topic_entry.get()
    if topic:
        prompt = generate_prompt(topic)
        response = generate_response(prompt)
        response_text.config(state=tk.NORMAL)
        response_text.delete(1.0, tk.END)
        response_text.insert(tk.END, response)
        response_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Please enter a topic.")

root = tk.Tk()
root.title("GPT-3 Custom Tool")
root.geometry("400x300")

topic_label = tk.Label(root, text="Enter a topic:")
topic_label.pack()

topic_entry = tk.Entry(root)
topic_entry.pack()

generate_button = tk.Button(root, text="Generate Prompt and Response", command=generate_prompt_and_response)
generate_button.pack()

response_label = tk.Label(root, text="Generated Response:")
response_label.pack()

response_text = tk.Text(root, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED)
response_text.pack()

root.mainloop()
