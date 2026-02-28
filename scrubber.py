import pandas as pd
import re
import sys

# Function to scrub Email addresses using Regex
def scrub_email(text):
    # Regex pattern to identify standard email formats
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # Replaces the email with a hidden tag
    return re.sub(email_pattern, "[EMAIL_HIDDEN]", str(text))

# Function to scrub Indian Phone numbers
def scrub_no(text):
    # Pattern covers +91, 0, 91 prefixes and 10-digit mobile numbers
    phone_pattern = r'(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}'
    return re.sub(phone_pattern, "[PHONE_HIDDEN]", str(text))

# Function to scrub IPv4 and IPv6 addresses
def scrub_ip(text):
    ipv4_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    ipv6_pattern = r'\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'
    
    text = re.sub(ipv4_pattern, "[IPv4_HIDDEN]", str(text))
    return re.sub(ipv6_pattern, "[IPv6_HIDDEN]", text)

# Function to scrub Indian Aadhaar numbers
def scrub_aadhaar(text):
    # Matches 12-digit Aadhaar numbers with optional spaces or hyphens
    aadhaar_pattern = r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
    return re.sub(aadhaar_pattern, "[AADHAAR_HIDDEN]", str(text))

# --- Main Execution Block....
if __name__ == "__main__":
    file_path = r'c:\Users\divya\OneDrive\Desktop\Python p&n\scrubber_P.csv'
    
    try:
        # Load the CSV file into a Pandas DataFrame
        processed_data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        sys.exit()

    # Check if the file contains any data
    if processed_data.empty:
        print("Error: The CSV file is empty. Nothing to process.")
        sys.exit()

    # Dictionary mapping column headers to their respective scrubbing functions
    scrubbing_map = {
        'Email': scrub_email, 
        'Phone': scrub_no, 
        'IP Address': scrub_ip, 
        'Aadhar Num': scrub_aadhaar
    }

    # Loop through the map and apply functions only if the column exists in the file
    for column_name, scrubbing_function in scrubbing_map.items():
        if column_name in processed_data.columns:
            processed_data[column_name] = processed_data[column_name].apply(scrubbing_function)
            print(f"Successfully scrubbed column: {column_name}")

    # Display the final masked data in the console
    print("Final Scrubbed Data")
    print(processed_data.head())

    # Save the cleaned data to a new CSV file
    output_name = 'excel_cleaned.csv'
    processed_data.to_csv(output_name, index=False)
    print(f"Data saved securely to '{output_name}'")