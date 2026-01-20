WhatsApp Chat Analyzer 📊
An end-to-end Data Science project that transforms raw WhatsApp chat exports into an interactive dashboard. This tool provides deep insights into communication patterns, user activity, and media sharing habits for both Group and Individual chats.

🚀 Key Features
Comprehensive Statistics: Tracks total messages, words, media files, and shared links.
Activity Maps: Visualizes the most active users, monthly trends, and weekly heatmaps.
Dynamic WordClouds: Generates visualizations of the most frequent words, excluding common stop words.
Emoji Analysis: Analyzes emoji usage frequency with interactive pie charts.
Format Flexibility: Robust regex logic to handle both 12-hour (AM/PM) and 24-hour time formats automatically.
Cross-Platform Emoji Support: Pre-configured to handle Windows-specific emoji fonts (Segoe UI Emoji) to avoid Matplotlib errors.

🛠️ Tech Stack
Framework: Streamlit
Data Manipulation: Pandas
Visualization: Matplotlib, Seaborn, WordCloud
Text Processing: Regex (re), URLExtract

📂 Project Structure
app.py: The main entry point for the Streamlit dashboard.
preprocessor.py: Handles data cleaning, regex-based parsing, and date-time formatting.
helper.py: Contains logic for statistics generation, emoji counting, and visualization helpers.
requirements.txt: List of all necessary Python libraries.
.gitignore: Configured to exclude .venv/, __pycache__/, and local environment files.
