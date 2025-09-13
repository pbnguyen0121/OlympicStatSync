# Milestone 2 Analysis

## Application Description
While integrating the Paris Olympics data with the existing dataset, I encountered multiple challenges throughout the project.

## Country data
I merged both datasets by using NOC codes as primary keys for their respective country, iterated through each row and appended non-duplicate data after checking for existing country codes, returning a new merged dataset.  

**Data Structure(s) Used**: 
- **Set:** Python's built-in data structure `set()` which allowed me to store country codes `NOC` for efficient duplicate checking before adding new countries to the main dataset.
    - **Time Complexity:** For adding an element or checking if an item already exists is **O(1)**, however, the worst case can become **O(n)**
- **Lists(2D):** Python's built-in lists allowed me to store country data as rows and columns, which was done through slicing the 2D list in my parameter.
    - **Time Complexity:** Slicing to create a list is **O(n)**, appending a new country is **O(1)**, but sorting my final list is **O(n log n)**

**Inconsistencies Found**: 
- While I was reviewing the existing dataset inside `olympics_country.csv`, I noticed that the dataset had the headers `noc` and `country`, but had used the `country_long` names that were found inside the Paris dataset `country.csv`.

    - **Decision Made**: I ultimately went with the decision of extracting `country` from the Paris dataset and keeping the original dataset as is.

- After I had thought I finished with this section of the project, I kept seeing a '0' in my Paris data intergration tester. I decided to re-review the ```nocs.csv``` file and noticed some countries had a different ```country``` and ```country_long``` value.
    - **Decision Made**: I decided to try and allow my ```new_olympics_country.csv``` to hold both names for the countries that had different values, which finally allowed me to get a higher paris data tester score.

## Medal Tally
I successfully created the medal tally file by using a composite key for each dataset consisting of (edition, edition_id, noc), which allowed me to iterate through the paris and existing medallists, counting the amount of athletes per country, their medals won, finally I merged the two and called the function to write a csv file.

**Data Structure(s) Used**: 
- **Set:** I used Python's built-in data structure `set()` twice here which allowed me to store an athlete  for each country in each event. This allowed me to get an accurate number of athletes that represented a single country, without worrying about duplicates.
    - **Time Complexity:** For adding an element or checking if an item already exists is **O(1)**, however, the worst case can become **O(n)**.
- **Lists(2D):** Using Python's built-in lists twice allowed me to create and store each row of data required to create the medal tally file. 
    - **Time Complexity:** Appending a row of data is **O(1)**, but sorting my final list is **O(n log n)**. When searching through the Olympic games data, the worst case is O(n) where n is the number of olympic games records and has a best case of O(1).
- **Dictionaries:** The ***First dictionary*** I created held each NOC code as a key and their respective country as the value. In doing so, I could figure out which NOC corresponds with what country to properly fill out my file. The ***Second*** and ***Third dictionary*** were used with the composite key described above to hold unique rows of data that belonged to their respective composite key.
    - **Time Complexity:** Now looking up a key on average is O(1), adding an element is also O(1) and finally appending is also O(1).

**Inconsistencies Found**:
-  The `new_medaly_tally.csv` file required both the `NOC` and `country` for each row, and while the `paris/medallists.csv` file had both required columns, the `olympic_athlete_event_result.csv`only carried the `NOC` code.

    - **Decision Made:** I decided to create a helper function named `noc_mapping(country_data)` that used country data to form a dictionary which would allow me to retrieve the country name using any country code.

- The `new_medaly_tally.csv` file required the `edition_id` of each olympic game, but the Paris 2024 summer olympics didn't have one set. The id also had to be unique and match correctly to the other files, which `olympic_games.csv` had already created the id.

    - **Decision Made:** I sent the `olympic_games.csv` data as a 2D list in the function parameters then iterated throughout each row of data till I matched the year '2024' and finally extracted the `edition_id` that was required to complete the medal tally file.

## Adding Age to Event Results
I calculated the athletes age during each Olympic event by retrieving their birthdate from the cleaned athlete bio data and the corresponding Olympic start date from the games dataset. Using these two values, I determined the athletes age on the first day of the competition. If the athletes birthday in that year occurred after the Olympic start date, I subtracted one year from the calculated age to ensure accuracy. Finally, I inserted the calculated age into a new column in the event_results dataset for each athletes record.

**Data Structure(s) Used**: 

- **Dictionaries:**
- - I made two dictionaries to speed things up:

- - - **First**: athlete_id → birthdate. Like a phonebook, if you know the athlete ID, you instantly get their birth date.

- - - **Second**: edition_id → start_date of the Olympic Games. Same idea, but for start dates.
These let me grab info in O(1) time for each lookup. Building them the first time is O(n), but it’s worth it because I don’t have to search the entire dataset every time.

- **Lists (2D):**
- - The CSV data is basically a 2D list — each row is one record, each column is a field. I looped through every row in olympic_athlete_event_results.csv, used my two dictionaries to grab the right dates, calculated the age, and wrote it into the new column. Looping is O(m) where m is the number of event results, and updating one cell is O(1).

**Inconsistencies Found**:
- **Missing athlete data**: 
- - Some athlete_id values in the event results didn’t exist in the athlete bio file, so there was no birth date to use.

- **Decision Made**: 
- - I left the age column blank for those athletes to avoid wrong calculations.

- **Missing start dates**:
- - Some edition_id values in the event results didn’t have a start date in olympics_games.csv (like games canceled due to war or with no recorded competition dates).

- **Decision Made**:
- - If no start date was found, I skipped the age calculation for that row.

- **Inconsistent birth date formats**:
- - Originally, the birth dates in the athlete bio file had different formats — some were yyyy-mm-dd, some were dd-Mon-yyyy, and some years had only two digits. This made calculations unreliable.

- **Decision Made**:
- - Before calculating ages, I used the clean_born_dates() function to reformat all dates into dd-Mon-yyyy so everything was consistent.

## Adding 2024/2026 Olympic Dates
I extracted the required headers to find the 2024/2026 Olympic data rows and set each date to their respective index.

**Data Manipulation:**  
I used a for loop on the 2D list provided in my parameter, ignoring the header inside by slicing it ```for row in games_data[1:]:```, which allowed only the data to be iterated. From there, I used an if/elif check on the ```year```column to ensure I'm working on the required rows, then I inserted all 3 date values into their corresponding columns.

**Time Complexity:**
**O(n)**: Where n is the number of rows in the dataset ```games_data```

## Cleaning/Formatting Olympic Dates
I first checked if ```competition_date``` was empty('—') or if the column ```isHeld``` had "Not held due to war". If so, I would ignore those rows to avoid errors.  

For all the valid rows, I called my helper function ```parse_competition_date(comp_date_chk, year)``` to first extract the start and end dates, then sending them to another helper function ```format_date(day, month, year)``` to give us the required format 'dd-Mon-yyyy' and finally using a Python f-string to give us the 'dd-Mon-yyyy to dd-Mon-yyyy' format for the ```competition_date``` column.

**Data Structure(s) Used:**
- **Lists(2D):** I used the 2D list that was given in my parameters ```cleaning_olympic_dates(games_data)```, which was my main dataset where I was extracting/adding data into.
    - **Time Complexity**: Grabbing the index for the required columns in the header was O(1), while looping through the list itself was O(n).

**Inconsistencies Found**:  

**The first inconsistency** I found inside ```olympics_games.csv``` was that the ```competition_date``` column used two different date formats (**Example:** ```6 – 13 April``` and ``` 14 May – 28 October ```).

- **Decision Made:** In my function ```parse_competition_date(competition_date, year)``` I first split the date using en-dash and cleaned the whitespace. 
    ```python
    comp_date = "14 May – 28 October"
    parts = date_str.split('–')   # Now parts = ["14 May ", " 28 October"]
    left_part = parts[0].strip()  # left_part = "14 May"
    right_part = parts[1].strip() # right_part = "28 October"
    left_words = left_part.split()   # left_words = ["14", "May"]
    right_words = right_part.split() # right_words = ["28", "October"]
    ```
    - Then based on how many words were present in each part, I determined the correct format and extracted the required values.

**The Second inconsistency** I found inside ```olympics_games.csv``` was the fact that some ```start_date``` or ```end_date``` values were inconsistent with the actual ```competition_date```. Example:  

```Tokyo 1964: start_date = "10 October", end_date = "24 October" competition_date = "11 – 24 October"```

- **Decision Made:** After googling some of the Olympics data with this inconsistency, I came to the conclusion that the ```competition_date``` was correct. I extracted the ```start_date``` and ```end_date``` from the ```competition_date``` which was already split above with the code snippet above.

    ```python
    # Example "14 May – 28 October" from the snippet above.
    elif len(left_words) == 2:
    start_day = left_words[0]  # start_day = '14'
    end_day = right_words[0]   # end_day = '28'
    start_month = left_words[1] # start_month = "May"
    end_month = right_words[1]  # end_month = "October"
    ```

    - This allowed me to set the correct version of the ```start_date``` and ```end_date```  

**The final inconsistency** I found was when I was checking the required format for the dates (dd-Mon-yyyy) and realized none of the dates had a year already implemented inside them.

- **Decision Made:** I grabbed the index for the ```year_idx``` column that was in the header ```year_idx = games_date[0].index("year")``` inside my main for loop which went through each row of data and used that year when calling the ```parse_competition_date(comp_date_chk, year)```.


## Cleaning 'born' Data
I first created a dictionary that'll hold an athlete's id as a key and the earliest Olympic year they participated in. Then, I called the function ```clean_born_dates(athlete_bio_file, lookup_dict)``` which would attempt to parse the birth date string to a datetime object.  

I also implemented a helper function named ```calc_birth_century(year_two_digits, edition_year)``` which was called when the birth date had a 2 digit year (Ex: "09-Nov-97"). Inside that function, I did some logical checks to determine if an athlete was born in the 1800s, 1900s or 2000s. Finally, I inserted each formatted date back into the ```athlete_bio``` list.

**Data Structure(s) Used:**  
- **Dictionary**: I created the dict ```athlete_edition_lookup = {}``` to hold the ```athlete_id``` as a key and the value as ```edition```. This allowed me to check later on what was the earliest Olympic year the corresponding athlete participated in.

## Adding Paris Athlete Bio Data
I integrated the Paris athlete data by first creating a set which held an athlete's name and their corresponding birthday and used that set to check for existing athletes data. I extracted the required values needed for the merging, formatted the name and the birthdate and finally integrated the data.

**Data Structure(s) Used**: 
- **Set:** Python's built-in data structure `set()` which allowed me to store an Athlete's name and their birthdate to check the existing athlete's data for duplicates. In the same helper function, I did create a set to hold unique athlete_id's as well.
    - **Time Complexity:** For adding an element or checking if an item already exists is **O(1)**, however, the worst case can become **O(n)**
- **Lists(2D):** Using the two 2D list of existing athlete data and Paris athlete data, I was able to compare the both and extract the new athletes into the existing dataset
    - **Time Complexity:** Appending a new row of athlete data is **O(1)**, while slicing the 2D list in my for loops to ignore the header is **O(n)**
- **Dictionaries:** I used a dictionary to map out the column and values of the 2D list headers I needed. This was done through a ```column_idx->column_value``` pair and allowed me to quickly search for whatever value I needed.
    - **Time Complexity:** Creating the dictionary is an average of **O(n)**, where searching for a specific index is **O(1)**.

**Inconsistencies Found**: 
- While reviewing ```olympic_athlete_bio.csv```, I noticed that some athlete's already existed in this file, but also existed in the Paris athlete bio dataset. However, the ```athlete_id``` wasn't matching each other.

    - **Decision Made**: I decided on keeping the ```athlete_id``` which was already inside the existing dataset, which caused an issue of how to check for duplicates. I ultimately decided on checking with a names/birthdate ```set()```.

- Immediately as I looked at the ```athletes.csv``` file, I noticed the names had a weird format. ```name``` had the format "LASTNAME(s) Firstname", while the ```name_tv``` held the the format "Firstname LASTNAME(s)". I immediately decided on using ```name_tv``` as it would be easier, and then I would just have to use ```.capitalize()```. This also led to realzing that some athletes don't have a ```name_tv```
    - **Decision Made**: In my helper function ```format_athlete_name``` I first checked if ```name_tv``` held a value, and if it did I would clean the names and return them. If there wasn't a value, I would then use the ```name``` string, ```.split()``` the name and re-arrange the parts to movie first name up front.
- The next formatting issue I cam across in ```athletes.csv``` was the fact that their birthdates were in the format "yyyy-dd-mm".
    - **Decision Made**: My helper function ```format_athlete_date(date_str)``` used the method ```datetime.strptime``` to convert a string into a datetime object, then I just returned it using ```date_obj.strftime()``` to convert it back to a string and format it to the required format "dd-Mon-yyyy".
- Inside ```olympic_athlete_bio.csv```, if there was no height or weight present, it was indicated by an empty string. On the other hand, ```athletes.csv``` had them set to 0 if there was no data for them.
    - **Decision Made**: Implemented a check before storing the data, where if the height or weight was set to '0', to instead set the value to an empty string.


# Analysis
# Complexity & Runtime Analysis (n, a, p, e, m): Cleaning, Paris Merge, Medal Tally

# A - Analysis for Cleaning Data

## Cleaning Athlete Birth dates
Let a represent the number of records in the olympic_athlete_bio file  
Let T(a) represent the total number of operations the function ```clean_born_dates``` performs on a

```python
def clean_born_dates(athlete_bio, athlete_lookup_dict):
    date_formats = [                                                                        # 5 - constant, fixed list.
                "%d-%b-%y",    
                "%d-%B-%Y",    
                "%d-%b-%Y",    
                "%d %B %Y",    
                "%Y",          
            ]
    cleaned_data = []                                                                       # 1 - initializing list
    born_idx = athlete_bio[0].index("born")                                                 # 1 - indexing
    athlete_id_idx = athlete_bio[0].index("athlete_id")                                     # 1 - indexing
   
    for row in athlete_bio[1:]:                                                             # (a-1) - as loop runs (a-1) times
        born_value = row[born_idx].strip()                                                  # 3 (a-1) - (assignment, index, strip)
        athlete_id = row[athlete_id_idx]                                                    # 2 (a-1)- (assignment, index) operators
        cleaned_date = ""                                                                   # 1 (a-1) - assignment operator
       
        if born_value:
            parsed = None                                                                   # 1 (a-1) - assignment operator

            for fmt in date_formats:                                                        # 5(a-1) - 5 checks at (a-1) times
                try:
                    parsed = datetime.strptime(born_value, fmt)                             # 2 * 5(a-1) - assignment operator and .striptime() used (a-1) times
                    
                    if fmt == "%d-%b-%y":                                                   # 1 * 5(a-1) - comparsion

                        year_two_digits = int(born_value[-2:])                              # 2 * 5(a-1) - assignment and int() call

                        edition_year = athlete_lookup_dict.get(athlete_id)                  # 2 * 5(a-1) - assignment and slice() call

                        correct_year = calc_birth_century(year_two_digits, edition_year)    # 2 * 5(a-1)
                                                                                            # 2 is the number of operations in calc_birth_century() on a successful search
                                                                                            # 5(a-1) is num of times in the inner loop * the outer loop

                        parsed = parsed.replace(year=correct_year)                          # 3 * 5(a-1)
                                                                                            # 3 is the two assignment operators + replace() call
                    
                    break
                except ValueError: 
                    continue
                   
            if parsed:                                                          
                cleaned_date = parsed.strftime("%d-%b-%Y")                                  # 2(a-1) - assignment operator and strftime() call
               
        row[born_idx] = cleaned_date                                                        # 1(a-1) - assignment operator                                                        
        cleaned_data.append(row)                                                            # 1(a-1) - append() call at (a-1) times
    
    cleaned_data.insert(0, athlete_bio[0])                                                  # 1 - insert() call
    return cleaned_data                                                                     # 1 - return call

# Helper function called
# Assuming the best case, first "if" check goes through
def calc_birth_century(two_digit_year, edition_year):
    if two_digit_year >= 25:                                # 1 - >= operator
        return 1900 + two_digit_year                        # 1 - return
    
    if edition_year >= 2000:                                # 0 - first if was caught
        return 2000 + two_digit_year                        # 0 - first if was caught
    else:
        return 1900 + two_digit_year                        # 0 - first if was caught
```
T(n) = 5 + 1 + 1 + 1 + (a-1) + 3(a-1) + 2(a-1) + 1(a-1) + 1(a-1) + 5(a-1) + 2 * 5(a-1) + 1 * 5(a-1) + 2 * 5(a-1) + 2 * 5(a-1) + 2 * 5(a-1) + 3 * 5(a-1) + 2 * 5(a-1) + 1(a-1) + 1(a-1) + 1 + 1  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 85(a-1) + 10  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 85a - 85 + 10  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 85a - 75  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 85a  
Therefore, T(a) is O(a)

## Cleaning Olympic dates
Let n represent the size of the array
Let T(n) represent the number of operations performed by ``cleaning_olympic_dates`` when given an array of size n

```python
def cleaning_olympic_dates(games_data):
    # Extract headers
    year_idx = games_data[0].index("year")                  # 1
    start_date_idx = games_data[0].index('start_date')      # 1
    end_date_idx = games_data[0].index("end_date")          # 1
    comp_date_idx = games_data[0].index("competition_date") # 1
    isheld_idx = games_data[0].index("isHeld")              # 1
    
    for row in games_data[1:]:                              # (n-1)
        year = row[year_idx]                                # 2(n-1)

        if year in ["2024", "2026"]:                        # 1(n-1)
            continue                                        # 0(n-1)  # worst case: else-path taken

        comp_date_chk = row[comp_date_idx].strip()          # 3(n-1)  # assign + index + strip
        isheld_chk = row[isheld_idx].strip().lower()        # 4(n-1)  # assign + index + strip + lower
        if comp_date_chk in ['—', '-']:                     # 1(n-1)
            row[start_date_idx] = ""                        # 0(n-1)  # worst case not taken
            row[end_date_idx] = ""                          # 0(n-1)
            row[comp_date_idx] = ""                         # 0(n-1)
        elif isheld_chk == "not held due to war":           # 1(n-1)
            row[start_date_idx] = ""                        # 0(n-1)
            row[end_date_idx] = ""                          # 0(n-1)
        else:
            start_date, end_date, comp_date = \
                parse_competition_date(comp_date_chk, year) # 2(n-1)  # call + assignment
            row[start_date_idx] = start_date                # 1(n-1)
            row[end_date_idx] = end_date                    # 1(n-1)
            row[comp_date_idx] = comp_date                  # 1(n-1)

    return games_data                                       # 1
```

**Helper function called**

```python
def parse_competition_date(competition_date, year):
    date_str = competition_date.strip()                     # 2
    parts = date_str.split('–')                             # 2

    left_part = parts[0].strip()                            # 3
    right_part = parts[1].strip()                           # 3

    left_words = left_part.split()                          # 2
    right_words = right_part.split()                        # 2

    # Example "6 – 13 April"
    if len(left_words) == 1 and len(right_words) >= 2:      # 1
        start_day = left_words[0]                           # 1
        end_day = right_words[0]                            # 1
        month_name = right_words[1]                         # 1

        start_date = format_date(start_day, month_name, year) # 2
        end_date = format_date(end_day, month_name, year)     # 2
        competition_date = f"{start_date} to {end_date}"    # 1

        return start_date, end_date, competition_date       # 1
    
    # Example "1 July – 26 November"
    elif len(left_words) == 2 and len(right_words) >= 2:    # 1
        start_day = left_words[0]                           # 1
        end_day = right_words[0]                            # 1
        start_month = left_words[1]                         # 1
        end_month = right_words[1]                          # 1

        start_date = format_date(start_day, start_month, year) # 2
        end_date = format_date(end_day, end_month, year)       # 2
        competition_date = f"{start_date} to {end_date}"    # 1

        return start_date, end_date, competition_date       # 1

    return "", "", ""                                       # 1

def format_date(day, month, year):
    date_obj = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")  # 2
    formatted_date = date_obj.strftime("%d-%b-%Y")                     # 2
    return formatted_date                                              # 1
```

T(n) = 1 + 1 + 1 + 1 + 1 + (n−1) + 2(n−1) + 1(n−1) + 3(n−1) + 4(n−1) + 1(n−1) + 1(n−1) + 2(n−1) + 1(n−1) + 1(n−1) + 1(n−1) + 1 + 2 + 2 + 1 + 2 + 2 + 3 + 3 + 2 + 2 + 1 + (1+1+1+1) + (2+2+1) + 1
    = 18(n−1) + 32
    = 18n + 14

Therefore T(n) is O(n)

## Create Athlete edition lookup

Let n represent the number of records in the results_data array 
Let T(n) represent the total number of operations the function ``create_athlete_edition_lookup`` performs on n

```python
def create_athlete_edition_lookup(results_data):
    athlete_edition_lookup = {}                                   # 1

    athlete_id_idx = results_data[0].index("athlete_id")          # 1
    edition_idx = results_data[0].index("edition")                # 1

    for row in results_data[1:]:                                  # (n-1)
        athlete_id = row[athlete_id_idx]                          # 2(n-1)  # index + assign
        edition = row[edition_idx]                                # 2(n-1)  # index + assign

        # Extract year from edition
        edition_year = int(edition.split()[0])                    # 4(n-1)  # split + index + int + assign

        # Store the earliest year the athlete participated
        if athlete_id not in athlete_edition_lookup or \
           edition_year < athlete_edition_lookup[athlete_id]:     # 1(n-1)  # condition check
            athlete_edition_lookup[athlete_id] = edition_year     # 1(n-1)  # dict set

    return athlete_edition_lookup                                  # 1
```

T(n) = 1 + 1 + 1 + (n−1) + 2(n−1) + 2(n−1) + 4(n−1) + 1(n−1) + 1(n−1) + 1
    = 11(n−1) + 4
    = 11n − 7
    = 11n

Therefore, T(n) is O(n)

## Athlete birthday lookup

Let a represent the number of records in the athlete_bio array  
Let T(a) represent the total number of operations the function ``athlete_birthdate_lookup`` performs on a

```python
def athlete_birthdate_lookup(athlete_bio):
    birthdate_lookup = {}                                      # 1

    athlete_id_idx = athlete_bio[0].index("athlete_id")        # 1
    born_idx = athlete_bio[0].index("born")                    # 1

    for row in athlete_bio[1:]:                                # (a-1)
        athlete_id = row[athlete_id_idx]                       # 2(a-1)  # index + assign
        birth_date = row[born_idx].strip()                     # 3(a-1)  # index + strip + assign

        birthdate_lookup[athlete_id] = birth_date              # 1(a-1)  # dict set
    
    return birthdate_lookup                                    # 1
```

T(a) = 1 + 1 + 1 + (a−1) + 2(a−1) + 3(a−1) + 1(a−1) + 1
    = 7(a−1) + 4
    = 7a − 3

Therefore, T(a) is O(a)

## Olympic date lookup

Let g represent the number of records in the olympic_games array    
Let T(g) represent the total number of operations the function ``olympic_date_lookup`` performs on g

```python
def olympic_date_lookup(olympic_games):
    # Extract header data
    edition_idx = olympic_games[0].index("edition")         # 1
    start_date_idx = olympic_games[0].index("start_date")   # 1

    dates_lookup = {}                                       # 1

    for row in olympic_games[1:]:                           # (g-1)
        edition = row[edition_idx]                          # 2(g-1)   # index + assign
        start_date_str = row[start_date_idx].strip()        # 3(g-1)   # index + strip + assign

        if start_date_str:                                  # 1(g-1)
            start_date = datetime.strptime(start_date_str, "%d-%b-%Y")  # 2(g-1)  # call + assign
            dates_lookup[edition] = start_date              # 1(g-1)   # dict set

    return dates_lookup                                     # 1
```

T(g) = 1 + 1 + 1 + (g−1) + 2(g−1) + 3(g−1) + 1(g−1) + 2(g−1) + 1(g−1) + 1
    = 10(g−1) + 4
    = 10g − 6

Therefore, T(g) is O(g)

## Add Age to event results

Let g represent the number of records in the olympic_games array    
Let T(g) represent the total number of operations the function ``olympic_date_lookup`` performs on g

```python
def olympic_date_lookup(olympic_games):
    # Extract header data
    edition_idx = olympic_games[0].index("edition")         # 1
    start_date_idx = olympic_games[0].index("start_date")   # 1

    dates_lookup = {}                                       # 1

    for row in olympic_games[1:]:                           # (g-1)
        edition = row[edition_idx]                          # 2(g-1)   # index + assign
        start_date_str = row[start_date_idx].strip()        # 3(g-1)   # index + strip + assign

        if start_date_str:                                  # 1(g-1)
            start_date = datetime.strptime(start_date_str, "%d-%b-%Y")  # 2(g-1)  # call + assign
            dates_lookup[edition] = start_date              # 1(g-1)   # dict set

    return dates_lookup                                     # 1
```

T(n) = 1 + 1 + 1 + (n−1) + 2(n−1) + 2(n−1) + 2(n−1) + 2(n−1) + 1(n−1) + 2(n−1) + 1(n−1) + 1
    = 13(n−1) + 4
    = 13n − 9

Therefore, T(n) is O(n)

**this is helper function**

## Format athlete data

Let n represent the size of the input string date_str   
Let T(n) represent the total number of operations the function ``format_athlete_date`` performs on n

```python
def format_athlete_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # 2  (call + assign)
        return date_obj.strftime("%d-%b-%Y")                # 2  (call + return)
    except ValueError:
        return date_str                                     # 1  (return)
```

T(n) = 2 + 2
= 4

Therefore, T(n) is O(1)

# B - Analysis for add Paris data into records

### Merge countries data

Let c represent the number of rows in existing_data 
Let p represent the number of rows in paris_nocs    
Let T(c, p) represent the total number of operations the function ``merge_countries_data`` performs on c and p

```python
def merge_countries_data(existing_data, paris_nocs):
    merged = [row[:] for row in existing_data]              # 1 + (c)   # assign + copy c rows

    # Extract Paris indices
    code_idx = paris_nocs[0].index("code")                  # 1
    country_idx = paris_nocs[0].index("country")            # 1

    # Create dict for noc -> list of existing country names
    existing_lookup = {}                                    # 1
    for row in existing_data[1:]:                           # (c-1)
        code = row[0].strip().upper()                       # 4(c-1)  # index + strip + upper + assign
        country = row[1].strip()                            # 3(c-1)  # index + strip + assign
        existing_lookup.setdefault(code, set())\
            .add(country.lower())                           # 4(c-1)  # lower + set() + setdefault() + add()

    for row in paris_nocs[1:]:                              # (p-1)
        code = row[code_idx].strip().upper()                # 4(p-1)  # index + strip + upper + assign
        paris_country = row[country_idx].strip()            # 3(p-1)  # index + strip + assign
        paris_country_lower = paris_country.lower()         # 2(p-1)  # lower + assign

        if code in existing_lookup:                         # 1(p-1)
            # Append country if different/not a dupe
            if paris_country_lower not in existing_lookup[code]:  # 1(p-1)
                merged.append([code, paris_country])        # 1(p-1)
                existing_lookup[code].add(paris_country_lower)    # 2(p-1)  # index + add()
        else:
            # Append new paris code
            merged.append([code, paris_country])            # 0(p-1)  # worst-case not taken
            existing_lookup[code] = {paris_country_lower}   # 0(p-1)  # worst-case not taken

    # Sort by country name
    merged[1:] = sorted(merged[1:], key=lambda x: x[1].lower())    # Sort(m) where m = len(merged[1:])

    return merged                                                  # 1
```

T(c, p) = (1 + c) + 1 + 1 + 1 + (c−1) + 4(c−1) + 3(c−1) + 4(c−1) + (p−1) + 4(p−1) + 3(p−1) + 2(p−1) + 1(p−1) + 1(p−1) + 1(p−1) + 2(p−1) + Sort(m) + 1
    = (13c − 12) + (15p − 15) + 4 + Sort(m) + 1
    = 13c + 15p − 22 + Sort(m)

Let m = len(merged[1:]) ≤ c + p. Sorting cost Sort(m) = O(m log m) = O((c + p) log(c + p))

Therefore, T(c, p) is O((c + p) log(c + p))

### Add Olympic games

Let g represent the number of records in the games_data array   
Let T(g) represent the total number of operations the function ``add_olympic_games`` performs on g

```python
def add_olympic_games(games_data):
    # Extract headers
    year_idx = games_data[0].index("year")                 # 1
    start_date_idx = games_data[0].index('start_date')     # 1
    end_date_idx = games_data[0].index("end_date")         # 1
    comp_date_idx = games_data[0].index("competition_date")# 1

    # Set years for both olympics
    paris_year = "2024"                                    # 1
    milano_cortina_year = "2026"                           # 1

    for row in games_data[1:]:                             # (g-1)
        # Handle 2024 Olympics data
        if row[year_idx] == paris_year:                    # 1(g-1)
            row[start_date_idx] = "26-Jul-2024"            # 3(g-1)  # worst-case: this branch taken
            row[end_date_idx] = "11-Aug-2024"              #        (three assignments)
            row[comp_date_idx] = "26-Jul-2024 to 11-Aug-2024"
        # Handle 2026 Olympics data
        elif row[year_idx] == milano_cortina_year:         # 1(g-1)
            row[start_date_idx] = "06-Feb-2026"            # 0(g-1)  # worst-case not taken
            row[end_date_idx] = "22-Feb-2026"              # 0(g-1)
            row[comp_date_idx] = "06-Feb-2026 to 22-Feb-2026"  # 0(g-1)

```

T(g) = 1 + 1 + 1 + 1 + 1 + 1 + (g−1) + 1(g−1) + 3(g−1) + 1(g−1)
    = 6 + 6(g−1)
    = 6g

Therefore, T(g) is O(g)

### Merge paris athlete bio

Let a represent the number of records in the athlete_bio_data array 
Let p represent the number of records in the paris_athletes_data array

```python
def merge_paris_athlete_bio(athlete_bio_data, paris_athletes_data):
    # Dict to hold the index/value for the required columns
    paris_indices = {col: paris_athletes_data[0].index(col) for col in   # 9  - constant, fixed list of 9 indices
                    ["code", "name", "name_tv", "gender", "birth_date", "height", "weight", "country", "country_code"]}
    
    # Create a set of data, holds names/birth dates
    existing_name_birthdate = get_existing_athlete_data(athlete_bio_data) # 2  - call + assign  (plus T_get(a) below)
    
    for row in paris_athletes_data[1:]:                                   # (p-1)
        paris_birth_date = row[paris_indices['birth_date']].strip()       # 3(p-1)  - index + strip + assign

        # Extract the name values and call the format name helper function
        name_tv = row[paris_indices["name_tv"]]                           # 2(p-1)  - index + assign
        name = row[paris_indices["name"]]                                 # 2(p-1)  - index + assign
        formatted_name = format_athlete_name(name_tv, name)               # 2(p-1)  - call + assign
                                                                          #          (helper cost counted separately)
        # Convert dates to 'dd-Mon-yyyy'
        converted_birth_date = format_athlete_date(paris_birth_date)      # 2(p-1)  - call + assign
                                                                          #          (helper cost counted separately)
        # Check for duplicate name + birthdate combinations
        if (formatted_name.lower(), converted_birth_date) not in existing_name_birthdate:  # 1(p-1)
            # Extract athlete data
            gender = row[paris_indices['gender']].strip()                 # 3(p-1)  - index + strip + assign
            height = row[paris_indices['height']].strip()                 # 3(p-1)
            weight = row[paris_indices['weight']].strip()                 # 3(p-1)
            athlete_id = row[paris_indices['code']].strip()               # 3(p-1)

            # Check if height/weight = 0, if so, set to empty string
            height = "" if height == "0" else height                      # 2(p-1)  - compare + assign
            weight = "" if weight == "0" else weight                      # 2(p-1)  - compare + assign
 
            # Create new row of paris athlete data
            new_row = [                                                   # 1(p-1)  - list build + assign
                athlete_id,
                formatted_name,
                gender,
                converted_birth_date,
                height,
                weight,
                row[paris_indices['country']].strip(),                    # (counted above in list build line)
                row[paris_indices['country_code']].strip()                # (counted above in list build line)
            ]
            
            athlete_bio_data.append(new_row)                              # 1(p-1)  - append

            # Add name/birthdate to set, used for duplicate checking
            existing_name_birthdate.add((name.lower(), converted_birth_date))  # 2(p-1)  - lower + add
    
    return athlete_bio_data                                               # 1
```

**Helper function called**

## Helper: format_athlete_date
Let n represent the size of the input string date_str   
Let T(n) represent the total number of operations the function ``format_athlete_date performs`` on n

```python
def format_athlete_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # 2  (call + assign)
        return date_obj.strftime("%d-%b-%Y")                # 2  (call + return)
    except ValueError:
        return date_str                                     # 1  (return)
```

T(n) = 2 + 2
    = 4

Therefore, T(n) is O(1)

## Helper: format_athlete_name

Let w represent the number of words in the provided name (name_tv or name)  
Let T(w) represent the total number of operations the function ``format_athlete_name`` performs on w

```python
def format_athlete_name(name_tv, name):
    if name_tv:                                                # 1
        return ' '.join(word.capitalize() for word in name_tv.split())  # 2 + 2w
        # 2 = split + join call, 2w ≈ per-word capitalize + join aggregation

    if name:                                                   # 1
        words = name.strip().split()                           # 3   - strip + split + assign
        if len(words) >= 2:                                    # 1
            first_name = words[-1].capitalize()                # 3   - index + capitalize + assign
            last_name_parts = [word.capitalize()               # 2(w-1) - per-word capitalize + append
                               for word in words[:-1]]
            return f"{first_name} {' '.join(last_name_parts)}" # 1   - join/format
        else:
            return name.strip().capitalize()                   # 3   - strip + capitalize + return
```

T(w) = 1 + 3 + 1 + 3 + 2(w−1) + 1 = 2w + 7 ⇒ O(w)
herefore, T(w) is O(w)

## Helper: get_existing_athlete_data

Let a represent the number of records in the athlete_bio_data array 
Let T(a) represent the total number of operations the function ``get_existing_athlete_data`` performs on a

```python
def get_existing_athlete_data(athlete_bio_data):
    # Extract header indices
    name_idx = athlete_bio_data[0].index("name")               # 1
    born_idx = athlete_bio_data[0].index("born")               # 1
    athlete_id_idx = athlete_bio_data[0].index("athlete_id")   # 1
    
    existing_name_birthdate = set()                            # 1
    existing_ids = set()                                       # 1
    
    for row in athlete_bio_data[1:]:                           # (a-1)
        name = row[name_idx].strip().lower()                   # 4(a-1)  - index + strip + lower + assign
        birthdate = row[born_idx].strip()                      # 3(a-1)  - index + strip + assign
        existing_name_birthdate.add((name, birthdate))         # 1(a-1)  - add
        
        try:
            existing_ids.add(int(row[athlete_id_idx]))         # 3(a-1)  - index + int + add
        except (ValueError, IndexError):
            continue                                           # 0(a-1)
    
    return existing_name_birthdate                              # 1
```

T(a) = 1 + 1 + 1 + 1 + 1 + (a−1) + 4(a−1) + 3(a−1) + 1(a−1) + 3(a−1) + 1
    = 11(a−1) + 6
    = 11a − 5

Therefore, T(a) is O(a)

Let T(a, p, w) be the total operations of ``merge_paris_athlete_bio`` including helpers

T(a, p, w) = [33(p−1) + 12] + [11a − 5] + [(2w + 7)(p−1)] + [4(p−1)]
= (44 + 2w)(p−1) + 11a + 7
= (44 + 2w)p + 11a − (37 + 2w)

Therefore, T(a, p, w) is O(a + p·w)
If w is treated as a small constant, T(a, p) is O(a + p)

# C - Analysis for generate the medal results for all games

### Create medal tally file

Let n represent the number of records in event_data 
Let m represent the number of records in paris_medallists   
Let c represent the number of records in country_data   
Let g represent the number of records in games_data

```python
def create_medal_tally_file(event_data, paris_medallists, country_data, games_data):
    noc_lookup = noc_mapping(country_data)                     # 2   (call + assign)

    # Process both data sets
    existing_medallists = process_existing_medallists(         # 2   (call + assign)
        event_data, noc_lookup)
    paris_medallists = process_paris_medallists(               # 2   (call + assign)
        paris_medallists, games_data)

    merged_medallists = existing_medallists + paris_medallists # 1   (concat assign)

    # Headers for new_medal_tally
    header = [                                                 # 1   (literal assign)
        "edition", "edition_id", "Country", "NOC",
        "number_of_athletes", "gold_medal_count",
        "silver_medal_count", "bronze_medal_count", "total_medals"
    ]

    merged_medallists.insert(0, header)                        # 1   (insert)

    write_csv_file("new_medal_tally.csv", merged_medallists)   # 1   (call)
```
**Helper function called**

## Helper: noc_mapping

Let c represent the number of records in country_data   
Let T(c) represent the total number of operations the function ``noc_mapping`` performs on c

```python
def noc_mapping(country_data):
    noc_lookup = {}                                           # 1

    for row in country_data[1:]:                              # (c-1)
        noc = row[0].upper().strip()                          # 4(c-1)  (index + upper + strip + assign)
        country = row[1].strip()                              # 3(c-1)  (index + strip + assign)
        noc_lookup[noc] = country                             # 1(c-1)  (dict set)
    return noc_lookup                                         # 1
```
T(c) = 1 + 4 + 3 + 1 + 1 = 8(c−1) + 2 = 8c − 6
Therefore, T(c) is O(c)

## Helper: process_existing_medallists

Let n represent the number of records in event_data 
Let k represent the number of grouped keys (edition, edition_id, noc)   
Let T(n, k) represent the total number of operations the function ``process_existing_medallists`` performs on n and k

```python
def process_existing_medallists(event_data, noc_lookup):
    # Extract Existing headers
    edition_idx = event_data[0].index("edition")              # 1
    edition_id_idx = event_data[0].index("edition_id")        # 1
    medal_idx = event_data[0].index("medal")                  # 1
    country_noc_idx = event_data[0].index("country_noc")      # 1
    athlete_idx = event_data[0].index("athlete_id")           # 1

    country_performance = {}                                  # 1
    csv_data = []                                             # 1

    # Group by (edition, edition_id, noc)
    for row in event_data[1:]:                                # (n-1)
        edition = row[edition_idx]                            # 2(n-1)
        edition_id = row[edition_id_idx]                      # 2(n-1)
        noc = row[country_noc_idx]                            # 2(n-1)
        key = (edition, edition_id, noc)                      # 1(n-1)
        if key not in country_performance:                    # 1(n-1)
            country_performance[key] = []                     # 1(n-1)
        country_performance[key].append(row)                  # 2(n-1)  (index + append)

    for key, rows in country_performance.items():             # k
        edition, edition_id, noc = key                        # 1(k)
        country_name = noc_lookup.get(noc, "Unknown")         # 2(k)

        unique_athletes = set()                               # 1(k)
        gold = silver = bronze = 0                            # 1(k)

        for row in rows:                                      # sums to (n-1)
            athlete_id = row[athlete_idx].strip().lower()     # 4(n-1)
            unique_athletes.add(athlete_id)                   # 1(n-1)

            medal = row[medal_idx].lower().strip()            # 4(n-1)
            if "gold" in medal:                               # 2(n-1)  (check + inc in taken branch)
                gold += 1
            elif "silver" in medal:
                silver += 1
            elif "bronze" in medal:
                bronze += 1
            
        num_athletes = len(unique_athletes)                   # 2(k)
        total_medals = gold + silver + bronze                 # 1(k)

        csv_row = [edition, edition_id, country_name, noc,    # 1(k)
                   num_athletes, gold, silver, bronze, total_medals]
        csv_data.append(csv_row)                              # 1(k)

    return csv_data                                           # 1
```

T(n, k) = (5 + 1 + 1) + 2+2+2+1+1+1+2 + 1+2+1+1+2+1+1 + 4+1+4+2 + 1
    = 7 + 11(n−1) + 10k + 11(n−1) + 1
    = 22(n−1) + 10k + 8 = 22n + 10k − 14
Therefore, T(n, k) is O(n) (since k ≤ n)

## Helper: process_paris_medallists

Let m represent the number of records in paris_medallists   
Let g represent the number of records in games_data 
Let h represent the number of NOC groups in paris_medallists    
Let T(m, g, h) represent the total number of operations the function ``process_paris_medallists`` performs on m, g, and h

```python
def process_paris_medallists(paris_medallists, games_data):
    # Extract Paris Headers
    medal_idx = paris_medallists[0].index("medal_type")       # 1
    country_code_idx = paris_medallists[0].index("country_code") # 1
    country_name_idx = paris_medallists[0].index("country_long") # 1
    name_idx = paris_medallists[0].index("name")              # 1

    # Extract games headers
    year_idx = games_data[0].index("year")                    # 1
    edition_id_idx = games_data[0].index("edition_id")        # 1

    paris_edition = "2024 Summer Olympics"                    # 1

    paris_edition_id = None                                   # 1
    for row in games_data[1:]:                                # (g-1)
        if "2024" in row[year_idx]:                           # 1(g-1)
            paris_edition_id = row[edition_id_idx]            # 0(g-1)   (taken once; worst-case not each iter)
            break                                             # 0(g-1)
    
    if paris_edition_id is None:                              # 1
        raise ValueError("2024 Olympics is not found in...")  # 0 (assume not raised)

    country_performance = {}                                  # 1
    csv_data = []                                             # 1

    # Group by NOC
    for row in paris_medallists[1:]:                          # (m-1)
        noc = row[country_code_idx]                           # 2(m-1)
        if noc not in country_performance:                    # 1(m-1)
            country_performance[noc] = []                     # 1(m-1)
        country_performance[noc].append(row)                  # 2(m-1)

    # Aggregate per NOC
    for noc, rows in country_performance.items():             # h
        country_name = rows[0][country_name_idx] if len(rows) > 0 else "Unknown"  # 3(h)
        gold = silver = bronze = 0                            # 1(h)
        unique_athletes = set()                               # 1(h)
    
        for row in rows:                                      # sums to (m-1)
            medal = row[medal_idx].lower().strip()            # 4(m-1)
            if "gold" in medal:                               # 2(m-1)   (check + inc)
                gold += 1
            elif "silver" in medal:
                silver += 1
            elif "bronze" in medal:
                bronze += 1

            athlete_name = row[name_idx].strip().lower()      # 4(m-1)
            unique_athletes.add(athlete_name)                 # 1(m-1)

        total_medals = gold + silver + bronze                 # 1(h)
        num_athletes = len(unique_athletes)                   # 2(h)

        csv_row = ["2024 Summer Olympics", paris_edition_id,  # 1(h)
                   country_name, noc, num_athletes,
                   gold, silver, bronze, total_medals]
        csv_data.append(csv_row)                              # 1(h)

    return csv_data                                           # 1
```
T(m, g, h) = (6 + 1 + 1) + 1(g−1) + (1 + 1) + 2+1+1+2 + 3+1+1+1+2+1+1 + 4+2+4+1 + 1
    = 8 + (g−1) + 2 + 6(m−1) + 10h + 11(m−1) + 1
    = 17(m−1) + (g−1) + 10h + 9
Therefore, T(m, g, h) is O(m + g) (since h ≤ m)

Let k represent the number of (edition, edition_id, noc) groups in event_data (1 ≤ k ≤ n)   
Let h represent the number of NOC groups in paris_medallists (1 ≤ h ≤ m)    
Let T(n, m, c, g, k, h) represent the total number of operations the function ``create_medal_tally_file`` performs (including helpers)

T(n, m, c, g, k, h) = 10 + (8c − 6) + (22n + 10k − 14) + [17(m−1) + (g−1) + 10h + 9]
    = 8c + 22n + 17m + g + 10k + 10h − 19

Therefore, with k ≤ n and h ≤ m, T(n, m, c, g) is O(n + m + c + g)