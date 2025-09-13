# Feel free to add additional python files to this project and import
# them in this file. However, do not change the name of this file
# Avoid the names ms1check.py and ms2check.py as those file names
# are reserved for the autograder

# To run your project use:
#     python runproject.py

# This will ensure that your project runs the way it will run in the
# the test environment

import csv
import os
from datetime import datetime
import random

# This function reads a csv file and return a list of lists
# each element of the returned list is a row in the csv file
# The first row is the header row
# Special case: if file is olympic_athlete_event_results.csv, add 'age' column
def read_csv_file(file_name):
    data_set = []
    with open(file_name, mode='r', encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        for i, row in enumerate(csv_reader):
            if file_name == "olympic_athlete_event_results.csv":
                if i == 0:
                    row.append("age")   # Header row
                else:
                    row.append("0") # Data row
            data_set.append(row)
    return data_set

# This function writes out a list of lists to a csv file
# each element of the list is a row in the csv file
# The first row is the header row
def write_csv_file(file_name, data_set):
    with open(file_name, mode='w', newline='', encoding="utf-8-sig") as file:
        csv_writer = csv.writer(file)
        for row in data_set:
            csv_writer.writerow(row)

# This function accepts two 2D lists of country data,
# adds new data that doesn't exist already in existing_data,
# returns a sorted, merged 2D list of countries & their codes.
def merge_countries_data(existing_data, paris_nocs):
    merged = [row[:] for row in existing_data]  # Copy existing country data

    # Extract Paris indices
    code_idx = paris_nocs[0].index("code")
    country_idx = paris_nocs[0].index("country")

    # Create dict for noc -> list of existing country names
    existing_lookup = {}
    for row in existing_data[1:]:
        code = row[0].strip().upper()
        country = row[1].strip()
        existing_lookup.setdefault(code, set()).add(country.lower())

    for row in paris_nocs[1:]:
        code = row[code_idx].strip().upper()
        paris_country = row[country_idx].strip()
        paris_country_lower = paris_country.lower()

        if code in existing_lookup:
            # Append country if different/not a dupe
            if paris_country_lower not in existing_lookup[code]:
                merged.append([code, paris_country])
                existing_lookup[code].add(paris_country_lower)
        else:
            # Append new paris code
            merged.append([code, paris_country])
            existing_lookup[code] = {paris_country_lower}

    # Sort by country name
    merged[1:] = sorted(merged[1:], key=lambda x: x[1].lower())

    return merged

# This function accepts 2D lists that hold medallists data and country data,
# calls helper functions to process the different data and then merges/creates
# the medal tally csv.
def create_medal_tally_file(event_data, paris_medallists, country_data, games_data):
    noc_lookup = noc_mapping(country_data) # Create NOC lookup dictionary
    
    # Process both data sets
    existing_medallists = process_existing_medallists(event_data, noc_lookup)
    paris_medallists = process_paris_medallists(paris_medallists, games_data)

    merged_medallists = existing_medallists + paris_medallists

    # Headers for new_medal_tally
    header = [
        "edition", "edition_id", "Country", "NOC",
        "number_of_athletes", "gold_medal_count",
        "silver_medal_count", "bronze_medal_count", "total_medals"
    ]

    merged_medallists.insert(0, header)

    write_csv_file("new_medal_tally.csv", merged_medallists)

# This function accepts a 2D list of country data,
# maps each NOC code to their respective country
# and returns a dictionary of NOC->Country
def noc_mapping(country_data):
    noc_lookup = {} # dict for mapping noc codes to countries

    for row in country_data[1:]:
        noc = row[0].upper().strip()
        country = row[1].strip()
        noc_lookup[noc] = country
    return noc_lookup

# This function accepts 2D list of medallist data and a dictionary of countries/codes,
# processes countries data, including medals and athletes
# and returns a 2D list of merged country data and their event results
def process_existing_medallists(event_data, noc_lookup):

    # Extract Existing headers
    edition_idx = event_data[0].index("edition")
    edition_id_idx = event_data[0].index("edition_id")
    medal_idx = event_data[0].index("medal")
    country_noc_idx = event_data[0].index("country_noc")
    athlete_idx = event_data[0].index("athlete_id")

    country_performance = {} # Group by country

    csv_data = [] 

    # Finding/setting unique editions to
    # group athlete data
    for row in event_data[1:]:
        edition = row[edition_idx]
        edition_id = row[edition_id_idx]
        noc = row[country_noc_idx]
        
        key = (edition, edition_id, noc)
        if key not in country_performance:
            country_performance[key] = []     # Key is new, create empty row
        country_performance[key].append(row)


    for key, rows in country_performance.items():
        edition, edition_id, noc = key
        country_name = noc_lookup.get(noc, "Unknown") # Get country name

        unique_athletes = set()
        gold = silver = bronze = 0

        for row in rows:
            athlete_id = row[athlete_idx].strip().lower()
            unique_athletes.add(athlete_id) # Get country athletes count

            medal = row[medal_idx].lower().strip()
            if "gold" in medal:
                gold += 1
            elif "silver" in medal:
                silver += 1
            elif "bronze" in medal:
                bronze += 1
            
        num_athletes = len(unique_athletes)
        total_medals = gold + silver + bronze

        csv_row = [edition, edition_id, country_name, noc, num_athletes, gold, silver, bronze, total_medals] # Create each row of data
        csv_data.append(csv_row) # 

    return csv_data

# This function accepts 2D lists of medallist data
# and extracts/processes each countries data from the paris csv file
def process_paris_medallists(paris_medallists, games_data):
    # Extract Paris Headers
    medal_idx = paris_medallists[0].index("medal_type")
    country_code_idx = paris_medallists[0].index("country_code")
    country_name_idx = paris_medallists[0].index("country_long")
    name_idx = paris_medallists[0].index("name")

    # Extract games headers
    year_idx = games_data[0].index("year")
    edition_id_idx = games_data[0].index("edition_id")

    paris_edition = "2024 Summer Olympics" # Edition name

    paris_edition_id = None
    for row in games_data[1:]:
        if "2024" in row[year_idx]:
            paris_edition_id = row[edition_id_idx]
            break  # When found, exit
    
    if paris_edition_id is None:
        raise ValueError("2024 Olympics is not found in the games data")

    country_performance = {} # Group by country

    csv_data = []

    # Setting unique country codes
    for row in paris_medallists[1:]:
        noc = row[country_code_idx]
        if noc not in country_performance:
            country_performance[noc] = [] 
        country_performance[noc].append(row)

    # Set corresponding country name
    for noc, rows in country_performance.items():
        country_name = rows[0][country_name_idx] if len(rows) > 0 else "Unknown"

        gold = silver = bronze = 0
        unique_athletes = set()
    
        # Set medals and athletes
        for row in rows:
            medal = row[medal_idx].lower().strip()
            if "gold" in medal:
                gold += 1
            elif "silver" in medal:
                silver += 1
            elif "bronze" in medal:
                bronze += 1

            athlete_name = row[name_idx].strip().lower()
            unique_athletes.add(athlete_name)

        total_medals = gold + silver + bronze
        num_athletes = len(unique_athletes)

        csv_row = [paris_edition, paris_edition_id, country_name, noc, num_athletes, gold, silver, bronze, total_medals] # Create each row of data
        csv_data.append(csv_row) # Loop each

    return csv_data

# This function accepts a 2D list of olympic games data
# and adds the proper dates to 2 new olympic games
def add_olympic_games(games_data):
    # Extract headers
    year_idx = games_data[0].index("year")
    start_date_idx = games_data[0].index('start_date')
    end_date_idx = games_data[0].index("end_date")
    comp_date_idx = games_data[0].index("competition_date")

    # Set years for both olympics
    paris_year = "2024"
    milano_cortina_year = "2026"

    for row in games_data[1:]:
        # Handle 2024 Olympics data
        if row[year_idx] == paris_year:
            row[start_date_idx] = "26-Jul-2024"
            row[end_date_idx] = "11-Aug-2024"
            row[comp_date_idx] = "26-Jul-2024 to 11-Aug-2024"
        # Handle 2026 Olympics data
        elif row[year_idx] == milano_cortina_year:
            row[start_date_idx] = "06-Feb-2026"
            row[end_date_idx] = "22-Feb-2026"
            row[comp_date_idx] = "06-Feb-2026 to 22-Feb-2026"

# This function receives a 2D list of olympic games data,
# sets empty values to "" and calls helper function
# to return properly formatted dates in the 2D list
def cleaning_olympic_dates(games_data):
    # Extract headers
    year_idx = games_data[0].index("year")
    start_date_idx = games_data[0].index('start_date')
    end_date_idx = games_data[0].index("end_date")
    comp_date_idx = games_data[0].index("competition_date")
    isheld_idx = games_data[0].index("isHeld")
    
    for row in games_data[1:]:
        year = row[year_idx] # Set the year for the olympics game

        if year in ["2024", "2026"]: # Ignore the new data
            continue

        # If there are no dates
        comp_date_chk = row[comp_date_idx].strip()
        isheld_chk = row[isheld_idx].strip().lower()
        if comp_date_chk in ['—', '-']:
            # Set all dates to empty
            row[start_date_idx] = ""
            row[end_date_idx] = ""
            row[comp_date_idx] = ""
        elif isheld_chk == "not held due to war":
            row[start_date_idx] = ""
            row[end_date_idx] = ""
        else:
            start_date, end_date, comp_date = parse_competition_date(comp_date_chk, year) # Extract required dates
            # Set new dates
            row[start_date_idx] = start_date
            row[end_date_idx] = end_date
            row[comp_date_idx] = comp_date

    return games_data

# This function accepts a date range as a string and a year,
# splits and cleans the data to extract needed values,
# calls a helper function to format the dates
# and returns 3 different formatted dates
def parse_competition_date(competition_date, year):
    date_str = competition_date.strip()
    parts = date_str.split('–') # Begin date extraction

    # Cleaning data in case of spaces
    left_part = parts[0].strip()
    right_part = parts[1].strip()

    left_words = left_part.split()
    right_words = right_part.split()

    # Example "6 – 13 April"
    if len(left_words) == 1 and len(right_words) >= 2:
        start_day = left_words[0]
        end_day = right_words[0]
        month_name = right_words[1]

        # Format each required date
        start_date = format_date(start_day, month_name, year) 
        end_date = format_date(end_day, month_name, year)
        competition_date = f"{start_date} to {end_date}"

        return start_date, end_date, competition_date
    
    # Example "1 July – 26 November"
    elif len(left_words) == 2 and len(right_words) >= 2:
        start_day = left_words[0]
        end_day = right_words[0]
        start_month = left_words[1]
        end_month = right_words[1]

        # Format each required date
        start_date = format_date(start_day, start_month, year)
        end_date = format_date(end_day, end_month, year)
        competition_date = f"{start_date} to {end_date}"

        return start_date, end_date, competition_date

    # If empty data is provided    
    return "", "", ""

# This funnction accepts 3 string values that make up a date,
# formats them to the required format "dd-Mon-yyy"
# and returns the formatted date
def format_date(day, month, year):
    # Convert to datetime object
    date_obj = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")

    # Formatting it to dd-Mon-yyyy
    formatted_date = date_obj.strftime("%d-%b-%Y")

    return formatted_date

# This function accepts a 2D list of olympic results date,
# creates a dictionary to map an athletes identifier to their 
# earliest olympic year they participated in and
# returns a dictionary holding that data
def create_athlete_edition_lookup(results_data):
    athlete_edition_lookup = {}
    
    athlete_id_idx = results_data[0].index("athlete_id")
    edition_idx = results_data[0].index("edition")
    
    for row in results_data[1:]:
        athlete_id = row[athlete_id_idx]
        edition = row[edition_idx]
        
        # Extract year from edition
        edition_year = int(edition.split()[0])
        
        # Store the earliest year the athlete participated
        if athlete_id not in athlete_edition_lookup or edition_year < athlete_edition_lookup[athlete_id]:
            athlete_edition_lookup[athlete_id] = edition_year
    
    return athlete_edition_lookup

# This function accepts a 2 digit integer that represents a year "i.e. 06"
# and the earliest year the athlete competed,
# returns year with the correct century
def calc_birth_century(two_digit_year, edition_year):
    if two_digit_year >= 25:
        return 1900 + two_digit_year
    
    if edition_year >= 2000:
        return 2000 + two_digit_year
    else:
        return 1900 + two_digit_year
        
# This function accepts a 2D list of athlete's bios and a dictionary
# which holds athlete_id and their earliest participating year,
# changes the different born date formats to "dd-Mon-yyyy" and
# returns a clean, formatted athlete bio 2D list
def clean_born_dates(athlete_bio, athlete_lookup_dict):
    # Used to find athlete's born date format
    date_formats = [
                "%d-%b-%y",    # dd-Mon-yy
                "%d-%B-%Y",    # dd-Month-yyyy
                "%d-%b-%Y",    # dd-Mon-yyyy
                "%d %B %Y",    # dd Month yyyy
                "%Y",          # yyyy
            ]
    cleaned_data = []

    # Extract header indicies
    born_idx = athlete_bio[0].index("born")
    athlete_id_idx = athlete_bio[0].index("athlete_id")
   
    for row in athlete_bio[1:]:
        born_value = row[born_idx].strip() # Extract birth date
        athlete_id = row[athlete_id_idx]   # Extract athlete_id
        cleaned_date = ""
       
        # If birthdate isn't an empty string
        if born_value:
            # Loop through each format to find the date
            parsed = None
            for fmt in date_formats:
                try:
                    parsed = datetime.strptime(born_value, fmt) # Convery string to datetime object
                    
                    # Handle 2-digit years
                    if fmt == "%d-%b-%y":
                        year_two_digits = int(born_value[-2:]) # Extract the two digit year
                        edition_year = athlete_lookup_dict.get(athlete_id) # Extract year this athlete competed
                        correct_year = calc_birth_century(year_two_digits, edition_year)
                        parsed = parsed.replace(year=correct_year) # Update datetime object
                    
                    break
                # If parsing failed
                except ValueError: 
                    continue
                   
            if parsed:
                # Convert datetime object back to string in the 'dd-Mon-yyyy' format
                cleaned_date = parsed.strftime("%d-%b-%Y")
               
        row[born_idx] = cleaned_date
        cleaned_data.append(row)
    
    cleaned_data.insert(0, athlete_bio[0]) # Insert header
    return cleaned_data

# This function accepts a 2D list of athlete's bio,
# creates a dictionary which holds an athletes id and their birth date
# and returns the dictionary
def athlete_birthdate_lookup(athlete_bio):
    birthdate_lookup = {}

    athlete_id_idx = athlete_bio[0].index("athlete_id")
    born_idx = athlete_bio[0].index("born")

    for row in athlete_bio[1:]:
        athlete_id = row[athlete_id_idx]
        birth_date = row[born_idx].strip()

        birthdate_lookup[athlete_id] = birth_date
    
    return birthdate_lookup

# This function accepts a 2D list of olympic games data,
# creates a dictionary which holds the edition as a key with the corresponding start date
# and returns the dictionary
def olympic_date_lookup(olympic_games):
    # Extract header data
    edition_idx = olympic_games[0].index("edition")
    start_date_idx = olympic_games[0].index("start_date")

    dates_lookup = {} # Empty dictionary

    for row in olympic_games[1:]:
        edition = row[edition_idx]
        start_date_str = row[start_date_idx].strip()

        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%d-%b-%Y")
            dates_lookup[edition] = start_date

    return dates_lookup

# This function accepts a birthdate as a string and the start date of a specific olympic,
# calculates the athletes age at the attended olympic and returns the age
def calculate_athlete_age(birth_date_str, olympic_start_date):

    birth_date = datetime.strptime(birth_date_str, "%d-%b-%Y") # Convert to datetime object
        
    age = olympic_start_date.year - birth_date.year # Calculate age at Olympic start
        
    # Check if birthday hasn't happened yet in the Olympic year
    if (olympic_start_date.month, olympic_start_date.day) < (birth_date.month, birth_date.day):
         age -= 1
            
    return str(age)

# This function accepts a 2D list of olympic event data, a dictionary that holds athletes birth date,
# and another dictionary which holds the start date of each olympic.
# It calculates and adds the age of each athlete during their olympic participation
# and returns event_data with a populated age column.
def add_age_to_event_results(event_data, birthdate_lookup, dates_lookup):
    # Extract headers
    edition_idx = event_data[0].index("edition")
    athlete_id_idx = event_data[0].index("athlete_id")
    age_idx = event_data[0].index("age")
    
    for row in event_data[1:]:
        edition = row[edition_idx] # Extract edition
        athlete_id = row[athlete_id_idx] # Extract athlete_id
        
        # Using both dictionaries, extract birth date and start date
        birth_date = birthdate_lookup.get(athlete_id)
        olympic_dates = dates_lookup.get(edition, None)
        
        if birth_date and olympic_dates:
            age = calculate_athlete_age(birth_date, olympic_dates) # Helper function to handle calculation
            row[age_idx] = age
        else:
            row[age_idx] = ""  # If data is missing
    
    return event_data

# This function accepts an athlete's birthdate as 'yyyy-dd-mm',
# converts and returns the date as the format 'dd-Mon-yyyy'
def format_athlete_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d-%b-%Y")
    except ValueError:
        return date_str  # Return unmodified date if theres an error

# This function accepts a 2D list of athlete data,
# creates a set which holds name/birthdates and returns the set
def get_existing_athlete_data(athlete_bio_data):
    # Extract header indices
    name_idx = athlete_bio_data[0].index("name")
    born_idx = athlete_bio_data[0].index("born")
    athlete_id_idx = athlete_bio_data[0].index("athlete_id")
    
    existing_name_birthdate = set()  # Set of (name, birthdate)
    existing_ids = set() # Set used to hold unique ids
    
    for row in athlete_bio_data[1:]:
        name = row[name_idx].strip().lower()
        birthdate = row[born_idx].strip()
        existing_name_birthdate.add((name, birthdate))
        
        try:
            existing_ids.add(int(row[athlete_id_idx]))
        except (ValueError, IndexError):
            continue
    
    return existing_name_birthdate

# This function accepts two strings that hold names,
# checks if name_tv is empty, if so, uses the regular name,
# and returns a formatted name as a string
def format_athlete_name(name_tv, name):
    if name_tv:
        return ' '.join(word.capitalize() for word in name_tv.split()) # Clean up name

    if name:
        words = name.strip().split() # Break full name into parts
        if len(words) >= 2:
            first_name = words[-1].capitalize() # Ensure first letter is uppercase
            # Capitalize and split multiple last names
            last_name_parts = [word.capitalize() for word in words[:-1]]
            return f"{first_name} {' '.join(last_name_parts)}"
        else:
            return name.strip().capitalize() # Check if there's one name

# This function accepts two 2D lists of athlete data,
# checks for dupes and merges the two
# and returns a formatted, merged 2D list of athlete data
def merge_paris_athlete_bio(athlete_bio_data, paris_athletes_data):
    # Dict to hold the index/value for the required columns
    paris_indices = {col: paris_athletes_data[0].index(col) for col in 
                    ["code", "name", "name_tv", "gender", "birth_date", "height", "weight", "country", "country_code"]}
    
    # Create a set of data, holds names/birth dates
    existing_name_birthdate = get_existing_athlete_data(athlete_bio_data)
    
    for row in paris_athletes_data[1:]:
        paris_birth_date = row[paris_indices['birth_date']].strip() # Extract paris birth dates

        # Extract the name values and call the format name helper function
        name_tv = row[paris_indices["name_tv"]]
        name = row[paris_indices["name"]]
        formatted_name = format_athlete_name(name_tv, name)
        
        # Convert dates to 'dd-Mon-yyyy'
        converted_birth_date = format_athlete_date(paris_birth_date)
        
        # Check for duplicate name + birthdate combinations
        if (formatted_name.lower(), converted_birth_date) not in existing_name_birthdate:
            # Extract athlete data
            gender = row[paris_indices['gender']].strip()
            height = row[paris_indices['height']].strip()
            weight = row[paris_indices['weight']].strip()
            athlete_id = row[paris_indices['code']].strip()

            # Check if height/weight = 0, if so, set to empty string
            height = "" if height == "0" else height
            weight = "" if weight == "0" else weight
 
            # Create new row of paris athlete data
            new_row = [
                athlete_id,
                formatted_name,
                gender,
                converted_birth_date,
                height,
                weight,
                row[paris_indices['country']].strip(),
                row[paris_indices['country_code']].strip()
            ]
            
            athlete_bio_data.append(new_row)

            # Add name/birthdate to set, used for duplicate checking
            existing_name_birthdate.add((name.lower(), converted_birth_date))
    
    return athlete_bio_data

# This main function is the function that the runner will call
# The function prototype cannot be changed
def main():
    # Load existing data
    athlete_bio_file = read_csv_file("olympic_athlete_bio.csv")
    event_data = read_csv_file("olympic_athlete_event_results.csv")
    country_data = read_csv_file("olympics_country.csv")
    games_data = read_csv_file("olympics_games.csv")
    
    # Load Paris data
    paris_athletes = read_csv_file(os.path.join("paris", "athletes.csv"))
    paris_events = read_csv_file(os.path.join("paris", "events.csv"))
    paris_medallists = read_csv_file(os.path.join("paris", "medallists.csv"))
    paris_nocs = read_csv_file(os.path.join("paris", "nocs.csv"))
    paris_teams = read_csv_file(os.path.join("paris", "teams.csv"))
       
    # Add paris country data into existing data
    merged_countries = merge_countries_data(country_data, paris_nocs)

    add_olympic_games(games_data) # Add 2024/2026 Olympic data
    cleaning_olympic_dates(games_data) # Clean existing Olympic dates

    # Create lookup dictionary for athlete participation year
    lookup_dict = create_athlete_edition_lookup(event_data)

    # Clean athlete's birth dates
    clean_athlete_bio = clean_born_dates(athlete_bio_file, lookup_dict)

    # Create 2 dictionaries to hold birthdate/olympic date
    birthdate_lookup = athlete_birthdate_lookup(clean_athlete_bio)
    dates_lookup = olympic_date_lookup(games_data)

    # Add 'age' values to event results
    event_data_with_ages = add_age_to_event_results(event_data, birthdate_lookup, dates_lookup)

    # Add paris athletes into athlete bio
    merged_athletes_bio = merge_paris_athlete_bio(clean_athlete_bio, paris_athletes)

    # olympics_medal_tally.csv
    create_medal_tally_file(event_data, paris_medallists, merged_countries, games_data)

    # Write all merged data
    write_csv_file("new_olympics_country.csv", merged_countries)
    write_csv_file("new_olympic_athlete_event_results.csv", event_data_with_ages)
    write_csv_file("new_olympics_games.csv", games_data)
    write_csv_file("new_olympic_athlete_bio.csv", merged_athletes_bio)