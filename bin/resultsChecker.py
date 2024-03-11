import os
import pandas as pd

# Function to check if a file exists in a directory
def file_exists(directory, filename):
    return os.path.exists(os.path.join(directory, filename))

# Function to count files in a directory
def count_files(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

# Function to count specific files in a directory
def count_specific_files(directory, pattern):
    return len([name for name in os.listdir(directory) if name.endswith(pattern) and os.path.isfile(os.path.join(directory, name))])

# Initialize lists to store data
processed_data = []
not_processed_data = []

# Iterate through subject folders
for subject_folder in os.listdir("proc_dash_data"):
    subject_path = os.path.join("proc_dash_data", subject_folder)
    if os.path.isdir(subject_path):
        subject_info = subject_folder.split("_")
        subject_name = subject_info[-2]
        time_point = subject_info[-3]
        
        # Initialize flags
        processed = True
        not_processed_reasons = []

        # Iterate through modality folders
        for modality_folder in os.listdir(subject_path):
            modality_path = os.path.join(subject_path, modality_folder)
            if os.path.isdir(modality_path):
                modality = modality_folder.split("_")[-1]
                stroke_availability = False
                group = "Sham"
                bias = file_exists(modality_path, "*bias.nii.gz")
                bias_bent = file_exists(modality_path, "*biasBet.nii.gz")
                non_splitted_parental = file_exists(modality_path, "non_splitted_parental.nii.gz")
                splitted_parental = file_exists(modality_path, "splitted_parental.nii.gz")
                non_splitted_non_parental = file_exists(modality_path, "non_splitted_non_parental.nii.gz")

                # Check for stroke availability for 'anat' modality
                if modality == "anat":
                    stroke_availability = file_exists(modality_path, "*stroke_mask.nii.gz")
                    if stroke_availability:
                        group = "Stroke"

                # Additional checks
                if modality in ["DTI", "diff"]:
                    dsi_studio_folder = os.path.join(modality_path, "DSI_studio")
                    fa_files = count_specific_files(dsi_studio_folder, "fa.nii.gz")
                    if not os.path.exists(dsi_studio_folder) or fa_files != 15:
                        # Reject subject
                        processed = False
                        not_processed_reasons.append(f"DSI Studio folder missing or incorrect number of FA files ({fa_files})")
                
                if modality == "func":
                    functional_path = os.path.join(modality_path, "funk")
                    if not os.path.exists(functional_path):
                        # Reject subject
                        processed = False
                        not_processed_reasons.append("Functional folder missing")
                
        # Append data to appropriate list
        if processed:
            processed_data.append([subject_name, time_point])
        else:
            not_processed_data.append([subject_name, time_point, ", ".join(not_processed_reasons)])

# Create DataFrame for processed data
processed_df = pd.DataFrame(processed_data, columns=["Subject", "Time Point"])

# Create DataFrame for not processed data
not_processed_df = pd.DataFrame(not_processed_data, columns=["Subject", "Time Point", "Reason"])

# Write DataFrames to CSVs
processed_df.to_csv("summary_report.csv", index=False)
not_processed_df.to_csv("not_processed_report.csv", index=False)



OTHER idea

import os
import pandas as pd

# Function to check if a file exists in a directory
def file_exists(directory, filename):
    return os.path.exists(os.path.join(directory, filename))

# Initialize dictionary to store subject data
subject_data = {}

# Iterate through subject folders
for subject_folder in os.listdir("proc_dash_data"):
    subject_path = os.path.join("proc_dash_data", subject_folder)
    if os.path.isdir(subject_path):
        subject_info = subject_folder.split("_")
        subject_name = subject_info[-2]
        time_point = subject_info[-3]

        # Initialize dictionary for the subject
        if subject_name not in subject_data:
            subject_data[subject_name] = {"Time Point": time_point, "DTI": False, "anat": False, "diff": False, "func": False, "Group": "Not Stroke"}

        # Iterate through modality folders
        for modality_folder in os.listdir(subject_path):
            modality_path = os.path.join(subject_path, modality_folder)
            if os.path.isdir(modality_path):
                modality = modality_folder.split("_")[-1]

                # Check for stroke mask availability
                if modality == "anat":
                    stroke_availability = file_exists(modality_path, "*stroke_mask.nii.gz")
                    if stroke_availability:
                        subject_data[subject_name]["Group"] = "Stroke"

                # Update modality status
                if modality in ["DTI", "diff", "func"]:
                    subject_data[subject_name][modality] = True

# Create DataFrame for summary report
summary_df = pd.DataFrame(subject_data).T.reset_index()
summary_df.columns = ["Subject", "Time Point", "DTI", "anat", "diff", "func", "Group"]

# Write DataFrame to CSV
summary_df.to_csv("summary_report.csv", index=False)

