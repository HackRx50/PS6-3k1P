import json
import asyncio  # Import asyncio
from sqlalchemy.orm import Session
from database import get_db, QuizDataDB  # Adjust the import based on your structure
from functions import *

sample_json = {"quiz": [
  {
    "question": "What is the entry age for adults at Bajaj Allianz?",
    "options": [
      "17 to 60 years",
      "18 to 65 years",
      "20 to 70 years",
      "21 to 75 years"
    ],
    "correctAnswer": "18 to 65 years"
  }]}

async def main():  # Define an async main function
    await upload_quiz_data(sample_json, 'abc')

if __name__ == '__main__':
    asyncio.run(main())  # Run the async main function
