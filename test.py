import os 
def truncate_file(file_path, line_number):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        if line_number < 1 or line_number > len(lines):
            print("Invalid line number.")
            return

        file.seek(0)
        file.truncate()
        file.writelines(lines[:line_number - 1])
    
truncate_file('./styles.csv', 44446)