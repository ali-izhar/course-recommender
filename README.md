# Course Recommendation System

## Introduction
The Course Recommendation System is a web application designed to provide personalized course recommendations to users based on their interests and preferences. It leverages machine learning algorithms and natural language processing to analyze user queries and recommend the most relevant courses.

## Features
- **Course Recommendations:** Utilizes a custom-built machine learning model trained with course data from Coursera.
- **Intelligent Chat Interface:** Features a chatbot powered by ChatGPT to interact with users and understand their preferences and answer their questions.
- **User Authentication:** Supports account creation and login functionality.
- **Technology Stack:** Built using Flask, Python, and other modern web technologies.

## Installation
Prerequisites
- Python 3.x
- Virtual environment (recommended)

## Steps
1. Clone the repository
```python
git clone [repository url]
```

2. Install dependencies
```python
pip install -r requirements.txt
```

3. Configure environment variables
Create a `.env` file in the root directory and add the following environment variables:
```python
OPENAI_API_KEY=[your openai api key]
```

4. Run the application
```python
python run.py
```

## Usage
1. Open the application in your preferred web browser at `http://localhost:5000/`.
2. Create a new account or log in to an existing one.
3. Interact with the intelligent chatbot to specify your interests and preferences.
4. Explore personalized course recommendations provided by the system.


## Contributing
We welcome contributions to the Course Recommendation System! If you'd like to contribute, please follow these guidelines:
- **Reporting Issues:** If you find a bug or have a feature request, please open a new issue to discuss it.
- **Pull Requests:** If you'd like to contribute code, please fork the repository and create a pull request. Make sure to describe your changes clearly.

## License
This project is licensed under the GPL-3.0 license. See the LICENSE file for details.

> Thank you for your interest in the Course Recommendation System! Feel free to explore, contribute, and share.