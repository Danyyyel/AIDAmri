import os
import pandas as pd
import datetime
import glob
import argparse

# Function to check if a file exists in a directory
def file_exists(directory, filename):
    try:
        return os.path.exists(glob.glob(os.path.join(directory, filename))[0])
    except IndexError:
        return False
    
# Function to count files in a directory
def count_files(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

# Function to count specific files in a directory
def count_specific_files(directory, pattern):
    return len([name for name in os.listdir(directory) if name.endswith(pattern) and os.path.isfile(os.path.join(directory, name))])

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="AIDAmri Output Checker")
    parser.add_argument("-i", "--input", required=True, help="Initial directory path")
    args = parser.parse_args()

    init_dir = args.input

    # Initialize lists to store data
    all_data = []

    # Check if the initial directory exists
    if not os.path.exists(init_dir):
        print("Error: Initial directory does not exist.")
        exit(1)

    # Check if batchproc_log.txt exists in init_dir
    batchproc_log_path = os.path.join(init_dir, "batchproc_log.txt")
    if os.path.exists(batchproc_log_path):
        was_processed_with_aidamri = "Yes"
        is_bids = "Yes"
    else:
        was_processed_with_aidamri = "No"

    # Iterate through subject folders
    for subject_folder in os.listdir(init_dir):
        subject_path = os.path.join(init_dir, subject_folder)
        
        if os.path.isdir(subject_path):
            subject_name = subject_folder
            
            # Iterate through time point folders
            for time_point_folder in os.listdir(subject_path):
                time_point_path = os.path.join(subject_path, time_point_folder)
                if os.path.isdir(time_point_path):
                    # Iterate through modality folders
                    for modality_folder in os.listdir(time_point_path):
                        modality_path = os.path.join(time_point_path, modality_folder)
                        if os.path.isdir(modality_path):
                            # Check files within modality_folder
                            files_count = len(glob.glob(os.path.join(modality_path, "**"), recursive=True))
                            
                            # Check if it's a stroke subject
                            is_stroke_subject = "No"

                            stroke_availability = file_exists(modality_path, "*Stroke_mask*")
                            if stroke_availability:
                                is_stroke_subject = "Yes"
                            
                            # Append data to all_data list
                            all_data.append([subject_name, time_point_folder, modality_folder, files_count, is_stroke_subject])

    # Create DataFrame
    columns = ["Subject", "Time_Point", "Modality", "Files_Count", "Stroke_Subject"]
    df = pd.DataFrame(all_data, columns=columns)

    # Directory to save the CSV file
    save_dir = os.path.join(init_dir, "AIDAmri_output_checker")
    os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

    # File path to save the CSV file
    df_save_path = os.path.join(save_dir, "summary_aidamri_report.csv")

    # Write DataFrame to CSV
    df.to_csv(df_save_path, index=False)

    # Print messages
    print("Results_Checker_Output:", datetime.datetime.now())
    print("Was_raw_data_processed_with_AIDAmri?:", was_processed_with_aidamri)
    print("Is_data_BIDS?:", is_bids)
    print("Summary report saved to:", df_save_path)
