#!/usr/bin/python3

print("Content-type: text/html")
print()

import cgi
import openai
import subprocess

myKey = "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"

openai.api_key = myKey

def generate_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=15
    )
    return response.choices[0].text.strip()

# Retrieve user input from HTML form
form = cgi.FieldStorage()
user_input = form.getvalue("in")
#print("ChatGPT: Hello, how can I assist you today?")

#a = subprocess.getoutput("sudo\t"  +  response)
response = generate_response(user_input)
print("ChatGPT:", response)
