# calgary_dogs.py
# Alireza Ghasemi
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd
import os

def load_data(file_path):
    """
    Load the Excel file into a DataFrame.

    Parameters:
    file_path (str): The path to the Excel file.

    Returns:
    pd.DataFrame: DataFrame containing the Excel data.
    """
    return pd.read_excel(file_path)

def normalize_breeds(breeds):
    """
    Normalize the dog breeds to lowercase for case-insensitive comparison.

    Parameters:
    breeds (iterable): An iterable containing dog breed names.

    Returns:
    dict: A dictionary with normalized breed names as keys and original names as values.
    """
    return {breed.lower(): breed for breed in breeds}

def get_dog_breed(valid_dog_breeds_normalized):
    """
    Prompt the user to enter a dog breed until a valid breed is entered.

    Parameters:
    valid_dog_breeds_normalized (dict): A dictionary with normalized breed names as keys and original names as values.

    Returns:
    str: The original dog breed name as entered by the user.
    """
    while True:
        user_input = input("Please enter a dog breed: ").strip().lower()
        if user_input in valid_dog_breeds_normalized:
            return valid_dog_breeds_normalized[user_input]
        else:
            print("Dog breed not found in the data. Please try again and make sure about the spelling the breed name.")

def analyze_data(df, breed):
    """
    Analyze the data for the specified breed and print the results.

    Parameters:
    df (pd.DataFrame): DataFrame containing the dog breeds data.
    breed (str): The dog breed to analyze.
    """
    # Multi-index DataFrame setup
    df.set_index(['Year', 'Month', 'Breed'], inplace=True)

    # Use IndexSlice
    idx = pd.IndexSlice

    # Find and print all years where the selected breed was listed in the top breeds.
    breed_data = df.loc[idx[:, :, breed], :]
    years = breed_data.index.get_level_values('Year').unique()
    print(f"Years where the breed '{breed}' was listed in the top breeds: {', '.join(map(str, years))}")

    # Calculate and print the total number of registrations of the selected breed.
    total_registrations = breed_data['Total'].sum()
    print(f"Total number of registrations for '{breed}': {total_registrations}")

    # Calculate and print the percentage of selected breed registrations out of the total for each year.
    for year in [2021, 2022, 2023]:
        year_data = df.loc[idx[year, :, :], :]
        year_total = year_data['Total'].sum()
        breed_year_total = breed_data.loc[idx[year, :, :], 'Total'].sum()
        if year_total > 0:
            percentage = (breed_year_total / year_total) * 100
            print(f"Percentage of '{breed}' registrations in {year}: {percentage:.2f}%")

    # Calculate and print the percentage of selected breed registrations out of the total three-year percentage.
    total_three_years = df.loc[idx[[2021, 2022, 2023], :, :], 'Total'].sum()
    total_breed_three_years = breed_data.loc[idx[[2021, 2022, 2023], :, :], 'Total'].sum()
    if total_three_years > 0:
        three_year_percentage = (total_breed_three_years / total_three_years) * 100
        print(f"Percentage of '{breed}' registrations over three years: {three_year_percentage:.2f}%")

    # Find and print the months that were most popular for the selected breed registrations.
    popular_months = breed_data[breed_data['Total'] == breed_data['Total'].max()].index.get_level_values('Month')
    print(f"Most popular months for '{breed}' registrations: {', '.join(popular_months)}")

def main():
    """
    Main function to execute the program logic.
    """
    # Import data here
    file_path = 'CalgaryDogBreeds.xlsx'
    df = load_data(file_path)

    print("ENSF 692 Dogs of Calgary")

    # Normalize the breed names
    valid_dog_breeds = df['Breed'].unique()
    valid_dog_breeds_normalized = normalize_breeds(valid_dog_breeds)

    # User input stage
    breed = get_dog_breed(valid_dog_breeds_normalized)

    # Data analysis stage
    analyze_data(df, breed)

if __name__ == '__main__':
    main()

