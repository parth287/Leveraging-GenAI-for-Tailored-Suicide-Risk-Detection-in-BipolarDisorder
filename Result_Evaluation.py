import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_confusion_matrix(cm, attribute):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=['Positive', 'Negative'], yticklabels=['Positive', 'Negative'])
    
    # Move the x-axis labels to the top
    plt.gca().xaxis.set_ticks_position('top')
    plt.gca().xaxis.set_label_position('top')
    
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(f'Confusion Matrix for {attribute}')
    plt.show()

# Load the Excel files

manual_annotations_path = '/Users/parth.doshi/Desktop/Parth/Masters/DAEN690/Data_Extraction/output_excel_file.xlsx'  # Update with your file path
chatgpt_annotations_path = '/Users/parth.doshi/Desktop/Parth/Masters/DAEN690/Data_Extraction/ChatGPTAnnotation_ResearchPapers_attributes.xlsx'  # Update with your file path


df_manual = pd.read_excel(manual_annotations_path)
df_chatgpt = pd.read_excel(chatgpt_annotations_path)

# Sort and align DataFrames
df_manual.sort_values('PMID', inplace=True)
df_chatgpt.sort_values('PMID', inplace=True)
df_chatgpt = df_chatgpt[df_manual.columns]

# Initialize dictionary and matrix for storing data
confusion_matrices = {}
aggregate_matrix = None

# Process each attribute
for attribute in df_manual.columns.drop('PMID'):
    y_true = df_manual[attribute]
    y_pred = df_chatgpt[attribute]
    if len(np.unique(y_true)) > 1:  # Check for more than one unique class
        cm = confusion_matrix(y_true, y_pred, labels=[1, 0])
        confusion_matrices[attribute] = cm
        report = classification_report(y_true, y_pred, target_names=['Absent', 'Present'], zero_division=0)
        print(f"Classification Report for {attribute}:\n{report}\n")
        if aggregate_matrix is None:
            aggregate_matrix = cm
        else:
            aggregate_matrix += cm
    else:
        print(f"Skipping {attribute}: Not enough class variation for meaningful report.")

# Aggregate confusion matrix plot
if aggregate_matrix is not None:
    plot_confusion_matrix(aggregate_matrix, 'Aggregate')
else:
    print("No aggregate confusion matrix to display.")


