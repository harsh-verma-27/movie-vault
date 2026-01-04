🎬 Movie Vault
A full-stack web application that allows users to search for movies using the OMDB API, view detailed information, and save their favorite titles into a personal SQLite database (The Vault).

✨ Features
Real-time Movie Search: Connects to the OMDB API to fetch movie data.

Detailed Views: Deep-dive into plot summaries, ratings, and cast information.

Personal Vault: Save and remove movies from a local database using SQLite.

Error Handling: Robust search validation and API timeout protection.

🛠️ Tech Stack
Backend: Python & Flask

Frontend: HTML5 & CSS3

Database: SQLite3

API: OMDB (Open Movie Database)

🚀 Getting Started
1. Prerequisites
Ensure you have Python 3.x installed. You will also need an API key from OMDb API.

2. Installation
Clone the repository and install the required dependencies:

pip install -r requirements.txt

3. Environment Variables
Create a .env file in the root directory and add your keys:

API_KEY=your_omdb_api_key_here
SECRET_KEY=your_flask_secret_key_here

4. Running the App

python app.py

Visit http://127.0.0.1:5000 in your browser.

Created by Harsh Verma
