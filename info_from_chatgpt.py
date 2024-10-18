from openai import OpenAI 
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from bs4 import BeautifulSoup  # BeautifulSoup is used to parse HTML content from the website
import requests  # send HTTP requests to the website URL

OPENAI_KEY = ""
client = OpenAI(api_key=OPENAI_KEY)

# Define a function to interact with GPT
def chat_with_gpt(messages):
    # Call the OpenAI API with the provided prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Return the generated response after stripping whitespace
    return response.choices[0].message.content.strip()

# Define a function to extract website content
def web_crawler(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to retrieve website: Status code {response.status_code}"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        text = soup.get_text(separator=' ', strip=True)  # Extract all text content from the webpage, separating by space and stripping excess whitespace

        # Return a dictionary with the webpage title and the extracted text content
        return {
            "title": title,
            "text": text
        }
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request and return an error message
        return f"An error occurred: {e}"

app = Flask(__name__)
CORS(app)  # Enable CORS (Cross-Origin Resource Sharing) for all routes

@app.route("/AI_news", methods=["POST"])
def answer():
    data = request.get_json()

    # Check if 'urls' are provided in the request
    # checks if the key 'urls' is present in the data object
    # checks whether the value associated with the 'urls' key is actually a list
    if 'urls' not in data or not isinstance(data['urls'], list):
        return jsonify({'error': 'A list of URLs is required'}), 400

    # Get the list of URLs
    urls = data['urls']

    # Initialize combined text variable
    combined_text = ""

    # Loop through each URL and fetch its content
    for url in urls:
        website_details = web_crawler(url)

        # If the function returns an error (a string), return the error as a JSON response
        if isinstance(website_details, str):
            return jsonify({'error': website_details}), 400
        
        # Append title and text to the combined text
        combined_text += f"Title: {website_details['title']}\nText: {website_details['text']}\n\n"

    # Prepare GPT message based on the combined content
    messages = [
        {
            "role": "system", 
            "content": "You are an AI assistant specializing in summarizing complex and detailed website content concisely. Focus on capturing key news highlights related to artificial intelligence, summarizing the main points without unnecessary details."
        },
        {
            "role": "user", 
            "content": f"""Summarize the following combined content from AI news websites in 600 to 700 words. Focus on the most important updates in AI research, technological advancements, new projects, and significant initiatives mentioned on the websites: {combined_text}"""
        }
    ]

    # Call OpenAI API and get the response
    response_text = chat_with_gpt(messages)

    # Return the GPT-generated summary
    return jsonify({'News Summary: ': response_text})

if __name__ == "__main__":
    app.run(debug=True)

# curl -X POST http://localhost:5000/AI_news \-H "Content-Type: application/json" \-d '{ "urls": ["https://news.mit.edu/topic/artificial-intelligence2", "https://techcrunch.com/category/artificial-intelligence/", "https://www.artificialintelligence-news.com/"] }'