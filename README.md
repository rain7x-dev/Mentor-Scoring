main.py – scoring logic  
mentors.csv – mentors data  
students.csv – students data  
interactions.csv – interaction logs  
feedbacks.csv – feedback ratings  
mentor_scores.csv – output (generated)  
requirements.txt – dependencies  

1. Install dependencies

pip install -r requirements.txt


2. Make sure all four CSV files are in the same directory as main.py

mentors.csv
students.csv
interactions.csv
feedbacks.csv


3. Run the script

python main.py



## Output Format

MentorID — Unique identifier for each mentor
Name — Name of the mentor
M — Final computed mentor score (range: 0–1)
Rank — Ranking based on score (higher is better)
