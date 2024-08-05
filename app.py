import os
from flask import Flask, request, render_template_string
from kaggle.api.kaggle_api_extended import KaggleApi
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

def setup_kaggle_api():
    api = KaggleApi()
    api.authenticate()
    return api

# Initialize Kaggle API
class SearchAgent:
    def __init__(self):
        self.api = KaggleApi()
        self.api.authenticate()

    def search_datasets(self, query):
        datasets = self.api.dataset_list(search=query)
        datasets = datasets[:3]
        return datasets

class DescriptionAgent:
    def __init__(self, model_name="llama3"):
        self.model = OllamaLLM(model=model_name)
        self.template = ChatPromptTemplate.from_template("""
        Provide a brief description of the dataset based on the following link and query:

        Dataset link: {link}
        Query: {query}

        Description:
        """)

    def generate_description(self, link, query):
        prompt = self.template.format(link=link, query=query)
        response = self.model(prompt)
        
        # Debugging: print the response
        print(f"Description Response: {response}")
        
        if isinstance(response, dict):
            description = response.get("choices", [{}])[0].get("text", "").strip()
        else:
            description = response.strip()
        
        return description

# Define the HTML template
from flask import Flask, request, render_template_string


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_query = request.form.get("query")
        response = process_request(user_query)
        return render_template_string(TEMPLATE, response=response, query=user_query)
    return render_template_string(TEMPLATE, response="", query="")

def process_request(user_query):
    search_agent = SearchAgent()
    description_agent = DescriptionAgent()

    # Search for datasets
    datasets = search_agent.search_datasets(user_query)

    if not datasets:
        return "No datasets found."

    # Generate descriptions for each dataset
    descriptions = []
    for dataset in datasets:
        try:
            # Assuming dataset is an object and 'ref' is a property
            dataset_link = f"https://www.kaggle.com/{dataset.ref}"  # Prepend the Kaggle URL
            description = description_agent.generate_description(dataset_link, user_query)
            descriptions.append(f"Link: <a href='{dataset_link}' target='_blank'>{dataset_link}</a><br>Description: {description}")
        except AttributeError as e:
            # Handle cases where 'ref' is not found
            print(f"AttributeError: {e}")
            descriptions.append("Failed to retrieve dataset link or description.")

    return "<br><br>".join(descriptions)

TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Dataset Search</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 40px; }
      h1 { color: #333; }
      form { margin-bottom: 20px; }
      input[type="text"] { width: 300px; padding: 8px; }
      input[type="submit"] { padding: 8px 12px; }
      .response { margin-top: 20px; }
      a { color: #007bff; text-decoration: none; }
      a:hover { text-decoration: underline; }
    </style>
  </head>
  <body>
    <h1>Dataset Search</h1>
    <form method="post">
      <label for="query">Enter your dataset request:</label><br>
      <input type="text" id="query" name="query" value="{{ query }}"><br><br>
      <input type="submit" value="Search">
    </form>
    <hr>
    <div class="response">{{ response|safe }}</div>
  </body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)


