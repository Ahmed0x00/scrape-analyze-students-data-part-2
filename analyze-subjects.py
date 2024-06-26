import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

output_folder ="/subjects/"

# Read data from Faculty of CS.json
with open('Faculty of CS.json', 'r') as f:
    faculty_data = json.load(f)

# Create a pandas DataFrame from the data
df = pd.DataFrame(faculty_data)

# Extract the marks into a separate DataFrame
marks_df = pd.DataFrame(df['Marks'].tolist())

# Define the mark ranges and labels
mark_ranges = {
    '45-50': (45, 50),
    '50-55': (50, 55),
    '60-65': (60, 65),
    '65-70': (65, 70),
    '70-75': (70, 75),
    '75-80': (75, 80),
    '80-85': (80, 85),
    '85-95': (85, 95),
}

# Analyze the marks for each subject and create bar charts
def analyze_marks():
    with open(output_folder + 'subject-analysis.txt', 'w') as f:
        for subject in marks_df.columns:
            mark_counts = []
            f.write(f"Analyzing {subject} marks:\n")
            
            for mark_label, (low, high) in mark_ranges.items():
                count = ((marks_df[subject] >= low) & (marks_df[subject] < high)).sum()
                mark_counts.append((mark_label, count))
                f.write(f"  Number of students with mark {mark_label}: {count}\n")
            
            failed_count = (marks_df[subject] < 50).sum()
            higher_than_95_count = (marks_df[subject] > 95).sum()
            average_mark = round(marks_df[subject].mean())
            
            mark_counts.append(("Failed", failed_count))
            mark_counts.append(("Higher than 95", higher_than_95_count))
            
            f.write(f"  Number of students who Failed: {failed_count}\n")
            f.write(f"  Number of students with mark Higher than 95: {higher_than_95_count}\n")
            f.write(f"  Average mark in {subject}: {average_mark}\n\n")
            
            # Convert to DataFrame for plotting
            mark_counts_df = pd.DataFrame(mark_counts, columns=["Mark Range", "Count"])

            # Plotting
            plt.figure(figsize=(10, 6))
            sns.barplot(x="Mark Range", y="Count", data=mark_counts_df)
            plt.title(f"Mark Distribution in {subject}")
            plt.xlabel("Mark Range")
            plt.ylabel("Number of Students")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the plot as a PNG file
            plt.savefig(output_folder + f"{subject}_mark_distribution.png")
            plt.close()

# Analyze the number of students who failed in each subject
def analyze_failed_students(marks_df):
    num_failed_students = (marks_df < 45).sum()
    return num_failed_students

# Analyze the number of students who failed in a certain number of subjects
def analyze_num_subjects_failed(marks_df):
    num_subjects_failed = marks_df.lt(45).sum(axis=1)
    num_students_failed = num_subjects_failed.value_counts()
    return num_students_failed