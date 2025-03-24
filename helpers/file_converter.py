import nbformat
import os
from pathlib import Path

""" Helpers to convert the .ipynb test files to .txt files"""

def rename_files(file_path):
    base, ext = os.path.splitext(file_path)
    if ext.lower() == '.ipynb':
        renamed_file_path = base + '.txt'
        renamed_file_path = convert_ipynb_to_txt(file_path,  renamed_file_path)
    
def convert_ipynb_to_txt(ipynb_file_path, output_txt_file_path):
    # Load the .ipynb file
    with open(ipynb_file_path, 'r') as f:
        notebook = nbformat.read(f, as_version=4)

    # Open the output text file
    with open(output_txt_file_path, 'w') as output_file:
        # Extract code and markdown cells
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                output_file.write(f"Code Cell:\n{cell.source}\n\n")
            elif cell.cell_type == 'markdown':
                output_file.write(f"Markdown Cell:\n{cell.source}\n\n")
    #print(f"Output saved to: {output_txt_file_path}")
    return output_txt_file_path