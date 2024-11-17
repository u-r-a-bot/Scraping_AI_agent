## Project Description
This project demonstrates an AI-powered solution to retrieve specific information from the web based on user-defined queries.
The application processes datasets (CSV or Google Sheets), performs automated searches for each entity in a selected column, and extracts relevant data using an advanced language model (LLM). 
A user-friendly dashboard enables seamless interaction with the system.

## Features
### 1. **File Upload and Google Sheets Integration**
   - Upload CSV files or connect directly to Google Sheets for data input.
   - Preview the dataset and select a primary column for querying.

### 2. **Custom Query with Prompt Templates**
   - Input queries using placeholders (e.g., `{company}`) to retrieve customized information for each entity.

### 3. **Automated Web Search**
   - Utilize APIs like SerpAPI to conduct web searches for each entity in the dataset.

### 4. **LLM Integration for Information Extraction**
   - Parses Extracted information through LLM using a custom input query by user.

### 5. **Results Display and Export**
   - View results in a clean table format within the dashboard.
   - Download the data as a CSV file or update the connected Google Sheet.

## Setup Instructions
```cmd
git clone https://github.com/u-r-a-bot/Scraping_AI_agent.git
pip install -r requirements.txt
streamlit run main.py
```
## Usage Guide
1. **Upload or load Data from google sheets**
2. **Select the column you want to query on**
3. **Enter the query**
4. **Enter the prompt for the llm** 
5. **Download or update on google sheets** 

## API Keys and Environment Variable
In the project working directory add a ```secrets.toml``` to a folder named as
```.streamlit```
So the secrets are in ```/.streamlit/secrets.toml```
In ```secrets.toml``` add groq and serp api key
```secrets.toml
SerpAPI_key = your_serp_api_key
GroqAPI = your_groq_api_key
```

## Optional Features
**Can update data to Google sheets directly**

### Link to the Loom video
https://www.loom.com/share/842bb6616fe04cd5ac35db6d4c441905?sid=96b4970d-1016-47bd-b598-99ba4248cc44