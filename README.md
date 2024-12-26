# Dictionary Learning Application

A Python/flask-based interactive dictionary application utilizing bootstrap,html and css that offers multiple features for word learning and tracking. The application uses a JSON-based dictionary database and provides functionality for word lookups, daily word learning, and progress tracking.

Program has option to check standard dictionary and see all definitions or to index into specific definitions.
With word of the day you choose a difficulty level between 1 and 5, complexity is choosen through number of syllables in words.
Once you have recieved your word you are then asked to enter your name which is then made into a name.csv file in the format of (word, date)
the last option is to see previous words of the day you have viewed just by entering your name.

## Features

### 1. Standard Dictionary Lookup
- Look up definitions for specific words
- Case-insensitive word searching
- Error handling for words not found in the dictionary

### 2. Word of the Day Generator
- Generate random words based on syllable difficulty (1-5 syllables)
- Save learned words with dates to a personal progress file
- Customized difficulty selection for learning

### 3. Progress Tracking
- View previously learned words with their corresponding dates
- Personal progress tracking through CSV files
- Individual progress files for each user

## Prerequisites

- Python 3.x
- Required files:
  - `dictionary_alpha_arrays.json` (dictionary database) 
  url:https://github.com/matthewreagan/WebstersEnglishDictionary/blob/master/dictionary_alpha_arrays.json

## Usage

Run the program and choose from three main options:

1. **Standard Dictionary (Option 1)**

2. **Word of the Day (Option 2)**

3. **Previous Words History (Option 3)**

## File Structure

- `dictionary_alpha_arrays.json`: Contains the dictionary database
- `{name}.csv`: Personal progress tracking files (created for each user)

## Functions

- `arr_index(w)`: Finds the correct dictionary index for a given word
- `translate(w, y)`: Retrieves word definitions from the dictionary
- `count_syllables(word)`: Calculates the number of syllables in a word
- `RandoWord()`: Generates a random word-definition pair

## Error Handling

The application includes error handling for:
- Invalid word lookups
- Invalid difficulty levels
- Missing progress files
- Invalid menu selections

## Note

The dictionary data is organized alphabetically in the JSON file, with words stored in separate arrays based on their first letter.

## Future Plans

I am currently implementing a GUI through Tkinter and plan to use it in my cs50x project.

I am also in the stages of learning how to create the .exe to run the program independent of an IDE.


Thank You, for looking at word of the day,

                                    Nicholas A Powell