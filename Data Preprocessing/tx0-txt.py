"""
Created on  August 15  2024
@author: 23829101 Long Qin

@reviewer: Hayeen
"""

import os

# define input and output folders
current_folder = os.getcwd()
input_folder = current_folder
output_folder = os.path.join(current_folder, "output")

# check if output folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


for filename in os.listdir(input_folder):
    if filename.endswith(".tx0"):
        # construct input file path
        input_file_path = os.path.join(input_folder, filename)

        # construct output file
        output_file_name = filename.replace(".tx0", ".txt")

        # construct output file path
        output_file_path = os.path.join(output_folder, output_file_name)

        with open(input_file_path, "r") as input_file:
            lines = input_file.readlines()

        # handle the position of electrode
        electrode_data = []
        electrode_start = False
        for line in lines:
            if "* Electrode positions" in line:
                electrode_start = True
                continue
            if "* Remote electrode positions" in line:
                break
            if electrode_start and "* Electrode [" in line:
                parts = line.split("=")[1].strip().split()
                x = parts[0].strip()
                z = parts[2].strip()
                electrode_data.append(f"{x}     {z}")

        num_electrodes = len(electrode_data)

        # handle the measurement data
        measurement_data = []
        measurement_start = False
        for line in lines:
            if "* Data" in line and "*******************" in line:
                measurement_start = True
                continue
            if measurement_start and line.strip() and not line.startswith("*"):
                parts = line.split()
                if len(parts) < 22:  # set up enough columns
                    continue
                a, b, m, n = parts[1], parts[2], parts[3], parts[4]
                rho = parts[10]
                x = parts[16]
                z = parts[20]
                measurement_data.append(f"{a} {b} {m} {n} {rho} {x} {z}")

        num_measurements = len(measurement_data)

        # write the content to the output file
        with open(output_file_path, "w") as output_file:
            output_file.write(f"{num_electrodes}# Number of electrodes\n")
            output_file.write("# x z\n")
            for line in electrode_data:
                output_file.write(line + "\n")

            output_file.write(f"{num_measurements}# Number of data\n")
            output_file.write("# a b m n rhoa x z\n")
            for i, line in enumerate(measurement_data, 1):
                output_file.write(f"{line}\n")

        print(f"Data extraction and conversion completed for {filename}.")

print("All files processed successfully.")
