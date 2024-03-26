import pathlib
import textwrap
import os
import google.generativeai as genai
#from flask import Flask, request, render_template 

from IPython.display import display
from IPython.display import Markdown

from pymongo import MongoClient
from flask import Flask, request, render_template

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mocktest']
# Used to securely store your API keycd
#from google.colab import userdata


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Generate a mock paper for JEE exam with 90 questions to be displayed under div section of html page, I don't want any explanation or instruction in it just the whole question paper, it should be of only question no answer should be involved")



document = {'Questions': response.text}
collection.insert_one(document)

# Example: Query documents
for doc in collection.find():
    print("From mongodb",doc)




from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Define some values to display

    # Pass these values to the template
    return render_template('mockPage.html', Questions=response.text)

if __name__ == '__main__':
    app.run(debug=True)
