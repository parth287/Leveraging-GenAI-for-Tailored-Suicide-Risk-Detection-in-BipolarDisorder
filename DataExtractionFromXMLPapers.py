#Helps extracting data from XML based PubMed papers and search for attributes and marks then as found or not.

import xml.etree.ElementTree as ET
import pandas as pd

# Load the XML file from the uploaded path
file_path = '/Users/parth.doshi/Desktop/Parth/Masters/DAEN690/Data_Extraction/ResearchPapers.xml'

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Let's print the tag of the root and the first child to see the structure
root_tag = root.tag
first_child_tag = root[0].tag if len(root) > 0 else "No children"

root_tag, first_child_tag


# List of specified attributes for binary checking
attributes = [
    "Age", "Psychoeducation", "Bipolar Disorder I (BD I)", "Bipolar Disorder II (BD II)", "Hypomania",
    "Communication Skills Training", "Problem Solving Skills Training", "Pharmacotherapy", "Family Focused Therapy",
    "Symptom", "Psychosocial Treatment", "Therapist Competence", "Adherence Scales", "Psychiatric Status", "Mania",
    "Depression", "Comorbid Diagnosis", "Female", "Protocol Therapy Sessions", "Antidepressant", "Anxiolytic",
    "Psychostimulant", "Second Generation Antipsychotic", "Lithium", "Any Antidepressant (AD)", "Benzodiazepine",
    "Stimulant", "AntiAnxiety Medication", "Race", "Gender", "Pediatric Bipolar Disorder (PBD)",
    "Bipolar Disorder Type 2", "Psychiatric Comorbidity", "Treatment", "Medications", "Family History",
    "Mortality Status", "Index Episode (Mixed)", "Primary Diagnosis", "Psychosocial Precipitants", "Suicidal Ideation",
    "Diagnostic Assessment", "Comorbid Psychiatric Conditions", "Substance Use Disorders (SUD)",
    "Alcohol Use Disorders (AUD)", "Psychotherapy", "Manic Episodes", "Depressive Episodes", "Hypomanic Symptoms",
    "Antidepressant Medication", "Social Rhythm Therapy", "Cognitive-Behavioral Therapy", "DSM-IV Criteria",
    "Depression Severity", "Mania Severity", "Marital Status", "Anticonvulsants", "Valproate", "Atypical Antipsychotics",
    "Other Mood Stabilizers", "Drug Use Disorder", "Mood Disorder", "First Generation Antipsychotic",
    "Any Mood Stabilizer (MS)", "Divalproex/Carbamazepine", "Lamotrigine", "Selective Serotonin Reuptake Inhibitors (SSRI)",
    "Selective Norepinephrine Reuptake Inhibitors (SNRI)", "Tricyclic Antidepressants (TCA)", "Other Antidepressants",
    "Prazosin", "Sleep Medication", "Post-Traumatic Stress Disorder", "Posttraumatic Stress Disorder (PTSD)",
    "Irritable Mood", "Manic Symptoms", "Prior Mania / Hypomania", "Mood Episode",
    "Systematic Treatment Enhancement Program for Bipolar Disorder (STEP-BD)", "Male", "Population",
    "Generalized Anxiety Disorders", "Obsessions", "Anxiety Disorders", "Psychoactive Substance Use Disorders",
    "Phobic Disorders", "Kleptomania", "Trichotillomania", "Pyromania", "ICD NOS (Self-injurious behavior)",
    "Mental Retardation", "Duration Cycling", "Olanzapine", "Acute Mania", "Prevention of Relapse",
    "Safety and Tolerability", "Rapid Cycling and Treatment-Resistant Patients", "Clinical Efficacy",
    "Pharmacodynamics and Pharmacokinetics", "Schizophrenia", "Valproate Monotherapy", "Fluoxetine",
    "Constructive Family Communication", "Communication Training for CHR Psychosis", "Stress", "Genetic Risk",
    "Neurobiological Vulnerability", "Mood Stabilizers", "Patient History", "Antidepressants",
    "Dehydroepiandrosterone-sulfate (DHEAS)", "Polycystic Ovarian Syndrome", "Mood Stabilizer",
    "Valproate-Treated Females", "Diagnosis", "Sexual Dysfunction", "Alcohol Use Disorder", "Cannabis Use Disorder",
    "Substance Use", "Mood Symptoms", "Impulsivity (Barratt Impulsiveness Scale)", "Subjective Response to Alcohol",
    "bipolar disorder I/II", "predominant polarity", "manic/hypomanic episodes", "mood episodes", "dipressive episodes",
    "psychiatric disorders", "neuro imaging", "biomarkers", "psycho therapy", "psychosocial treatments",
    "maintainance therapy"
]

# Initialize a DataFrame to hold the binary data for each article
df = pd.DataFrame(columns=attributes)

# Function to check presence of attributes in article text
def check_presence(article, attributes):
    # Convert article text to lower case for case insensitive search
    article_text = ''.join(article.itertext()).lower()
    return [1 if attribute.lower() in article_text else 0 for attribute in attributes]

# Populate the DataFrame by processing each article
for article in root.findall('.//PubmedArticle'):
    # Check the presence of each attribute in the current article
    presence = check_presence(article, attributes)
    # Append the result to the DataFrame
    df.loc[len(df)] = presence

# Adding a paper identifier to each row. The identifier can be the PMID if available, or an incremental index.

# Initialize a new DataFrame to hold the binary data for each article with an identifier
df_with_id = pd.DataFrame(columns=['Paper_ID'] + attributes)

# Function to extract PMID or use an incremental index as identifier
def extract_identifier(article):
    pmid_element = article.find('.//PMID')
    return pmid_element.text if pmid_element is not None else f"Article_{df_with_id.index[-1] + 1 if len(df_with_id.index) > 0 else 1}"

# Populate the DataFrame by processing each article with identifiers
for i, article in enumerate(root.findall('.//PubmedArticle')):
    # Extract identifier
    identifier = extract_identifier(article)
    # Check the presence of each attribute in the current article
    presence = check_presence(article, attributes)
    # Append the result to the DataFrame, including the identifier
    df_with_id.loc[len(df_with_id)] = [identifier] + presence


# Display the first few rows of the DataFrame to verify the output
# Define the file path to save the DataFrame as an Excel file
excel_file_path = '/mnt/data/ResearchPapers_attributes.xlsx'

# Save the DataFrame to an Excel file
df.to_excel('ResearchPapers_attributes.xlsx', index=False)

# Provide the path to the user for download
excel_file_path