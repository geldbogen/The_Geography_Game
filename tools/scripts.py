import os

filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
output_string= ""

for dir, subdir, file in os.walk(filepath):
    for filename in file:
        if filename.endswith(".csv"):
            output_string += f"{filename}\n"

with open("all_csv_files.txt", "w") as f:
    f.write(output_string)
    f.close()
