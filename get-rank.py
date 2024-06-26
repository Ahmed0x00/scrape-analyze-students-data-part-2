import json

def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {file} not found.")
        return []

def find_student_rank(seat_number, data):
    # Sort the data based on Full Mark in descending order
    sorted_data = sorted(data, key=lambda x: x['Full Mark'], reverse=True)
    
    # Find the rank of the student with the given seat number
    for rank, student in enumerate(sorted_data, start=1):
        if student['Seat Number'] == seat_number:
            return rank, student, sorted_data[:rank-1]  # Return top-ranked students
    
    return None, None, []

def get_rank(seat_number):
    file = "Faculty of CS.json"  # Replace with your JSON file name

    # Load the data from the JSON file
    data = load_data(file)
    
    if not data:
        return

    # Find the rank of the student
    rank, student, top_students = find_student_rank(seat_number, data)

    if student:
        print(f"Student with Seat Number {seat_number} is ranked {rank}.")
        print(f"Details: {json.dumps(student, indent=2)}")
        
        print(f"\n{rank-1} students above Seat Number {seat_number}:")
        for idx, top_student in enumerate(top_students, start=1):
            print(f"Rank {idx}: {top_student['Name']},id: {top_student['Seat Number']}, Marks: {top_student['Full Mark']}")
    else:
        print(f"Student with Seat Number {seat_number} not found.")
