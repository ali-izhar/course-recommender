# Course Recommendation System

## Introduction
The Course Recommendation System is a web application that recommends courses to users based on their interests. The application uses the free udemy public API available on [RapidAPI](https://rapidapi.com/) and a custom-built machine learning model to recommend courses to users. The application also uses the [ChatGPT](https://openai.com/blog/chatgpt/) model to generate responses to user queries. The application is built using [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [Python](https://www.python.org/).

## Installation
1. Clone the repository
```bash
git clone [repo-url]
```

2. Install the dependencies
```bash
pip install -r requirements.txt
```

3. Set up your API keys
```bash
Create a .env file in the root directory of the project
Add the following lines to the .env file
RAPID_API_KEY=[your-rapid-api-key]
RAPID_API_HOST=[your-rapid-api-host]
OPENAI_API_KEY=[your-openai-api-key]
# any other API keys you may need
```

4. Delete existing database instance (optional)
```bash
Delete the database.db file in the root directory of the project
```

5. Run the application
```bash
python run.py
```

## Usage
1. Open the application in your browser
2. Create an account
3. Login to your account
4. Interact with the chatbot to get course recommendations

## References
1. [ChatGPT](https://openai.com/blog/chatgpt/)
2. [Flask](https://flask.palletsprojects.com/en/2.0.x/)
3. [Python](https://www.python.org/)
4. [RapidAPI](https://rapidapi.com/)