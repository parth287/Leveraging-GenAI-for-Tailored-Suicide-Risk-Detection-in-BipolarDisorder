import pandas as pd

# Load the Excel file
file_path = '/Users/parth.doshi/Desktop/Parth/Masters/DAEN690/Data_Extraction/Mannual Annotations.xlsx'  # Update this with your file path
df = pd.read_excel(file_path)

# Assuming 'PMID' and 'Attribute Name' are the column names
# Create a new DataFrame marking the presence of an attribute with 1
df['Presence'] = 1

# Pivot the DataFrame using max to handle duplicates, filling absent values with 0
pivot_df = df.pivot_table(index='PMID', columns='Attribute Name', values='Presence', aggfunc='max', fill_value=0)
# print(pivot_df)

required_columns = ["Age", "Psychoeducation", "Bipolar Disorder I (BD I)", "Bipolar Disorder II (BD II)", "Hypomania",
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
    "maintainance therapy"]


# Add missing columns that are not in the pivoted DataFrame but required in the final format, initialize with zeros
for col in required_columns:
    if col not in pivot_df.columns:
        pivot_df[col] = 0

# Reorder and select the required columns to match the specific format
pivot_df = pivot_df[required_columns]
print(pivot_df)

# Optionally, you can reset the index to make 'PMID' a column and rename the index if necessary
pivot_df.reset_index(inplace=True)
pivot_df.rename(columns={'index': 'PMID'}, inplace=True)
# pivot_df.drop('Attribute Name')

# # Save the resulting DataFrame back to an Excel file if required
output_path = 'Formatted_MannualAnnotations.xlsx'  # Specify your output file path
pivot_df.to_excel(output_path, index=False)

print(pivot_df)


