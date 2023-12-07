import pandas as pd
import spacy
import re

data = pd.read_csv('output_reddit.csv')

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_locations(text):
    if isinstance(text, str):
        # Process the text using spaCy
        doc = nlp(text)
        
        # location extraction
        extracted_locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']

        # Use regular expression to find additional location patterns 
        location_pattern = re.compile(r'\[([^]]+)\]')
        regex_matches = location_pattern.findall(text)
        regex_locations = [match.strip() for match in regex_matches]

        # Handle cases where locations are enclosed in parentheses after a comma
        comma_parentheses_pattern = re.compile(r',\s*\(([^)]+)\)')
        comma_parentheses_matches = comma_parentheses_pattern.findall(text)
        comma_parentheses_locations = [match.strip() for match in comma_parentheses_matches]

        # Combine all sets of extracted locations
        return list(set(extracted_locations + regex_locations + comma_parentheses_locations))
    else:
        # Handle the case where text is not a valid string
        return []


data = pd.read_csv('output_reddit_data_extracted_location.csv')
data['extracted_locations_treatment'] = data['treatment_tags'].apply(extract_locations)
data['extracted_locations_awards'] = data['total_awards_received'].apply(extract_locations)

# Combine locations from both columns
data['combined_locations'] = data.apply(lambda row: list(set(row['extracted_locations_treatment'] + row['extracted_locations_awards'])), axis=1)

data.to_csv('output_reddit_data_extracted_location_improved-1.csv')

