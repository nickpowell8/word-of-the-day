from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
import random
import csv
from datetime import date
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = '5f352379e2ac631c6d834d3a51f845ea'  # Required for session management

# Create a data directory if it doesn't exist
DATA_DIR = Path("user_data")
DATA_DIR.mkdir(exist_ok=True)

try:
    # Load dictionary data
    with open("dictionary_alpha_arrays.json", "r", encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: dictionary_alpha_arrays.json not found!")
    data = []  # Provide empty default to prevent crash
except json.JSONDecodeError:
    print("Error: Invalid JSON in dictionary file!")
    data = []

def safe_filename(name):
    """Convert a username to a safe filename"""
    return "".join(c for c in name if c.isalnum() or c in ('-', '_')).lower()

def arr_index(w):
    if not w:
        return None
    for idx, dictionary in enumerate(data):
        for key in dictionary:
            if w[0].lower() == key[0].lower():
                return idx
    return None

def translate(w, y):
    if y is None or not w:
        return None
    w = w.lower()
    try:
        if w in data[y]:
            return data[y][w]
    except (IndexError, TypeError):
        return None
    return None

def count_syllables(word):
    if not word:
        return 0
    word = word.lower()
    vowels = "aeiouy"
    syllable_count = 0
    
    for i, char in enumerate(word):
        if char in vowels:
            if i == 0 or word[i - 1] not in vowels:
                syllable_count += 1
    
    if word.endswith("e") and len(word) > 1:
        syllable_count -= 1
    
    return max(syllable_count, 1)

def RandoWord():
    if not data:
        return "Error loading dictionary", "error"
    
    try:
        random_dict = random.choice(data)
        random_key = random.choice(list(random_dict.keys()))
        random_word = random_dict[random_key]
        
        if isinstance(random_word, list):
            random_word = random_word[0]
        
        return random_word, random_key
    except (IndexError, KeyError):
        return "Error generating word", "error"

def save_word_to_history(name, word):
    """Safely save a word to user's history"""
    if not name or not word:
        return False
        
    filename = safe_filename(name)
    if not filename:
        return False
        
    filepath = DATA_DIR / f"{filename}.csv"
    
    try:
        with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([word, date.today()])
        return True
    except Exception as e:
        print(f"Error saving word: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    if request.method == 'POST':
        word = request.form.get('word', '').strip()
        if word:
            idx = arr_index(word)
            definition = translate(word, idx)
            return render_template('lookup.html', word=word, definition=definition)
    return render_template('lookup.html')

@app.route('/word-of-day', methods=['GET', 'POST'])
def word_of_day():
    if request.method == 'POST':
        try:
            difficulty = int(request.form.get('difficulty', 0))
            name = request.form.get('name', '').strip()
            
            if not name:
                flash('Please enter your name.')
                return render_template('word_of_day.html')
                
            if difficulty <= 0 or difficulty > 5:
                flash('Please enter a difficulty between 1 and 5.')
                return render_template('word_of_day.html')
            
            # Generate word with matching syllable count
            for _ in range(100):  # Limit attempts to prevent infinite loop
                definition, word = RandoWord()
                if word == "error":
                    flash('Error generating word. Please try again.')
                    return render_template('word_of_day.html')
                    
                if count_syllables(word) == difficulty:
                    # Save to CSV
                    if save_word_to_history(name, word):
                        return render_template('word_of_day.html', 
                                            word=word, 
                                            definition=definition, 
                                            success=True)
                    else:
                        flash('Error saving word to history.')
                        return render_template('word_of_day.html')
                                        
            flash('Could not find a word matching the specified difficulty. Please try again.')
            return render_template('word_of_day.html')
            
        except ValueError:
            flash('Please enter a valid difficulty number.')
            return render_template('word_of_day.html')
            
    return render_template('word_of_day.html')

@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Please enter your name.')
            return render_template('history.html')
            
        filename = safe_filename(name)
        if not filename:
            flash('Invalid name provided.')
            return render_template('history.html')
            
        filepath = DATA_DIR / f"{filename}.csv"
            
        try:
            words = []
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as file:
                    for line in file:
                        try:
                            word, date_str = line.rstrip().split(',')
                            words.append({'word': word, 'date': date_str})
                        except ValueError:
                            continue  # Skip invalid lines
                return render_template('history.html', words=words, name=name)
            else:
                flash('No history found for this name.')
                return render_template('history.html')
        except Exception as e:
            flash('Error reading history file.')
            return render_template('history.html')
            
    return render_template('history.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
