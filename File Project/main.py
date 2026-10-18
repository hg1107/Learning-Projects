from pathlib import Path
import os


def createfile():
    try:
        name = input("Tell your file name: ")
        path = Path(name)
        if not path.exists():
            with open(path,"w") as fs:
                data = input("Enter the data you want to write")
                fs.write(data)
            print("File created successfully")
        else:
            print("File name already exists")
    except Exception as er:
        print("Error occured: ", er)




def readfile():
    try:
        name = input("Enter your file name: ")
        path = Path(name)
        if path.exists():
            with open(path, 'r') as fs:
                content = fs.read()
                print("Your file content is:\n", content)
        else:
            print("No such file exists")
    except Exception as er:
        print("Error occured: ", er)




def updatefile():
    try:
        name = input("Tell your file name: ")
        path = Path(name)
        
        if path.exists():
            print("Operations")
            print("1. Renaming the file")
            print("2. Appending the content")
            print("3. Overwriting the file")
            
            choice = int(input("Enter your option: "))
            if choice == 1:
                newname = input("Tell the new file name: ")
                new_path = Path(newname)
                if not new_path.exists():
                    path.remane(new_path)
                    print("Renamed successfully")
                else:
                    print("File already exists")
            elif choice == 2:
                with open(path, 'a') as fs:
                    data = input("What do you want to append: ")
                    fs.write("\n" + data)
                print("Appended successfully")
            elif choice == 3:
                with open(path, 'w') as fs:
                    data = input("What do you want to overwrite: ")
                    fs.write("\n" + data)
                print("Owerwritten successfully")
    
    except Exception as er:
        print("Error occured: ", er)




def deletefile():
    try:
        name = input("Enter file name: ")
        path = Path(name)
        if path.exists():
            path.unlink()
            print("File deleted successfully")
        else:
            print("No file exists")
    except Exception as er:
        print("Error occured: ", er)




print("Press 1 for creating a file")
print("Press 2 for reading the file")
print("Press 3 for updating the file")
print("Press 4 for deleting the file")

a = int(input("\nTell your response: "))

if a == 1:
    createfile()
if a == 2:
    readfile()
if a == 3:
    updatefile()
if a == 4:
    deletefile()
    
