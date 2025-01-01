import pandas as pd

og_file_path = "Timetable_27_Dec_2024_removed_removed.xlsx"

try:
    df = pd.read_excel(og_file_path)
except PermissionError:
    print(f"Permission denied: Unable to access '{og_file_path}'. Please check if the file is open or if you have the necessary permissions.")
    exit(1)
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    exit(1)


curr_row = 27

row_indices_to_remove = []

while curr_row < df.shape[0]:
    row_indices_to_remove.append(curr_row)
    row_indices_to_remove.append(curr_row + 1)
    row_indices_to_remove.append(curr_row + 2)

    curr_row += 28


df = df.drop(row_indices_to_remove)

new_file_path = og_file_path.replace(".xlsx", "_rows_removed.xlsx")

# (need to set it to a mode such that itwill overwrite any existing file with the same name.) -> not done yet.
df.to_excel(new_file_path, index = False) 
