import json
from abc import ABC, abstractmethod
from pathlib import Path

database = "School_data.json"   # Main database
data = {"students": [], "teachers": []}     # Dummy database, changes will occur here first and then sent to mai database

if Path(database).exists():
    with open(database, 'r') as f:
        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(database, 'w') as f:
        json.dump(data, f, indent = 4)

class Persons(ABC):
    @abstractmethod
    def get_roles(self):
        pass
    
    @abstractmethod
    def register(self):
        pass
    
    @abstractmethod
    def show_details(self):
        pass
    
    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email:
            return True
        else:
            return False
    
    

class Student(Persons):
    def get_roles(self):
        return "Student"
    
    def register(self):
        name = input("Tell your name: ")
        age = int(input("Tell your age: "))
        email = input("Tell your mail: ")
        roll_no = input("Enter your roll no: ")
        
        if not Persons.validate_email(email):
            print("Invalid details")
            return
        
        for i in data["students"]:
            if i['roll_no'] == roll_no:
                print("Student already exists")
                return
        
        data["students"].append({
            "name": name,
            "age": age,
            "email": email,
            "roll_no": roll_no,
            "grades": {}
        })
        save()
        print(f"Student {name} registered")
    

    def show_details(self):
        roll_no = input("Enter roll no: ")
        for i in data['students']:
            if i['roll_no'] == roll_no:
                grades = i['grades']
                avg = sum(grades.values() / len(grades)) if grades else 0
                
                print(f"\n Name: {i['name']}")
                print(f"Roll No: {i['roll_no']}")
                print("Grades: ", grades)
                print(f"Average: {avg:.2f}")
                return
        print("Student not found")
    
    def add_grades(self):
        roll_no = input("Enter roll no: ")
        subject = input("Enter the subject: ")
        marks = float(input("Enter the marks: "))
        
        for i in data['students']:
            if i['roll_no'] == roll_no:
                i['grades'][subject] = marks
                save()
                print("Grades added successfully")
                return
        print("Student not found")
    
class Teacher(Persons):
    def get_roles(self):
        return "Teacher"
    
    def register(self):
        name = input("Tell your name: ")
        age = int(input("Tell your age: "))
        email = input("Tell your mail: ")
        emp_id = input("Enter your employee id: ")
        subject = input("Subject: ")
        
        if not Persons.validate_email(email):
            print("Invalid details")
            return
        
        for i in data["teachers"]:
            if i['emp_id'] == emp_id:
                print("Teacher already exists")
                return
        
        data["teachers"].append({
            "name": name,
            "age": age,
            "email": email,
            "emp_id": emp_id,
            "subjects": subject
        })
        save()
        print(f"Teacher {name} registered")
    
    def show_details(self):
        emp_id = input("Enter employee id: ")
        for i in data['teachers']:
            if i['emp_id'] == emp_id:
                print(f"\n Name: {i['name']}")
                print(f"Emp ID: {i['emp_id']}")
                print(f"Subject: {i['subjects']}")
                return
        print("Teacher not found")

        

stud = Student()
teach = Teacher()


print("Press 1 to register a student")
print("Press 2 to register a teacher")
print("Press 3 to add grades")
print("Press 4 to show a student details")
print("Press 5 to show teacher details")

choice = int(input("Enter your choice: "))
if choice == 1:
    stud.register()
elif choice == 2:
    teach.register()
elif choice == 3:
    stud.add_grades()
elif choice == 4:
    stud.show_details()
elif choice == 5:
    teach.show_details()
else:
    print("Invalid choice")