import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

output_folder ="/departments/"

def process_department(data, department_name):
    # Creating a DataFrame from the sample data
    df = pd.json_normalize(data)

    # Analysis
    num_students = len(df)  # Number of students is the length of the DataFrame
    highest_gpa_row = df.loc[df['GPA'].idxmax()]
    highest_gpa = highest_gpa_row['GPA']
    highest_gpa_seat_number = highest_gpa_row['Seat Number']
    highest_gpa_name = highest_gpa_row['Name']
    highest_gpa_mark = highest_gpa_row['Full Mark']
    average_gpa = round(df['GPA'].mean(), 2)

    rating_counts = df['Rating'].value_counts().to_dict()

    # Preparing the result
    result = {
        f"Number of students in {department_name} department": num_students,
        f"Highest GPA in {department_name} department": highest_gpa,
        f"Highest Seat number in {department_name} department": highest_gpa_seat_number,
        f"Highest GPA Name in {department_name} department": highest_gpa_name,
        f"Highest Mark in {department_name} department": highest_gpa_mark,
        f"Average in {department_name} department": average_gpa,
        f"Number of students with 'Acceptable' rating in {department_name} department": rating_counts.get('Acceptable', 0),
        f"Number of students with 'Weak' rating in {department_name} department": rating_counts.get('Weak', 0),
        f"Number of students with 'Very Good' rating in {department_name} department": rating_counts.get('Very Good', 0),
        f"Number of students with 'Very Weak' rating in {department_name} department": rating_counts.get('Very Weak', 0),
        f"Number of students with 'Good' rating in {department_name} department": rating_counts.get('Good', 0),
        f"Number of students with 'Excellent' rating in {department_name} department": rating_counts.get('Excellent', 0)
    }
    
    # Generate charts
    generate_charts(df, department_name)
    
    return result

def generate_charts(df, department_name):
    # GPA Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['GPA'], kde=True, bins=10)
    plt.title(f'GPA Distribution in {department_name}')
    plt.xlabel('GPA')
    plt.ylabel('Frequency')
    plt.savefig(f"{output_folder}{department_name}_GPA_Distribution.png")
    plt.show()

    # Rating Distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Rating', data=df, order=df['Rating'].value_counts().index)
    plt.title(f'Rating Distribution in {department_name}')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.savefig(f"{output_folder}{department_name}_Rating_Distribution.png")
    plt.show()

    # GPA vs Full Mark
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Full Mark', y='GPA', data=df)
    plt.title(f'GPA vs Full Mark in {department_name}')
    plt.xlabel('Full Mark')
    plt.ylabel('GPA')
    plt.savefig(f"{output_folder}{department_name}_GPA_vs_Full_Mark.png")
    plt.show()

def write_to_file(result):
    with open(output_folder+'departments-info.txt', 'a') as file:
        for key, value in result.items():
            file.write(f"{key}: {value}\n")
        file.write("\n\n")  # Add a newline between department results

def analyze_departments():
    departments = {
        "Data Science": "datascience.json",
        "Robotics": "robotics.json",
        "Multimedia": "multimedia.json",
        "Faculty of CS": "Faculty of CS.json"
    }
    
    for department, file_name in departments.items():
        with open(file_name, 'r') as f:
            data = json.load(f)

        # Write department name as heading
        with open(output_folder+'departments-info.txt', 'a') as file:
            file.write(f"========= {department} Students' data =========\n\n")

        result = process_department(data, department)
        write_to_file(result)
