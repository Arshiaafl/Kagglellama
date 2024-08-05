# Multi-Agent Dataset Search Chatbot

This Flask application is designed to help researchers find datasets on Kaggle. The application uses two agents: one for searching datasets based on user queries and another for generating brief descriptions of the datasets.

## Features

- Accepts user queries to search for datasets on Kaggle.
- Returns up to three relevant datasets with brief descriptions.
- Uses Flask for the web interface.
- Integrates with Kaggle API using environment variables for authentication.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Kaggle API credentials (username and key)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/multi-agent-dataset-search-chatbot.git
    cd multi-agent-dataset-search-chatbot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Kaggle API credentials:
    - Go to the [Kaggle website](https://www.kaggle.com/).
    - Log in and go to your account settings.
    - Scroll down to the API section and click "Create New API Token". This will download a `kaggle.json` file.
    - Place the `kaggle.json` file in the `.kaggle` directory in your home folder:
        ```bash
        mkdir ~/.kaggle
        mv /path/to/kaggle.json ~/.kaggle/
        chmod 600 ~/.kaggle/kaggle.json
        ```

### Environment Variables

Set the following environment variables in your deployment platform (e.g., GitHub Actions):

- `KAGGLE_USERNAME`: Your Kaggle username
- `KAGGLE_KEY`: Your Kaggle API key

### Running the Application

To run the application locally:
```bash
python app.py
