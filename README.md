├── main.py               # Main scoring script
├── mentors.csv           # Mentor data
├── students.csv          # Student/mentee data
├── interactions.csv      # Mentor-student interaction data
├── feedbacks.csv         # Student feedback ratings
├── mentor_scores.csv     # Output: ranked mentor scores (generated on run)
├── requirements.txt      # Python dependencies

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


|  Column  |           Description             |
|          |                                   |
| MentorID | Unique mentor identifier          |
| Name     | Mentor name                       |
| M        | Final Mentor Score (0–1)          |
| Rank     | Rank in descending order of score |