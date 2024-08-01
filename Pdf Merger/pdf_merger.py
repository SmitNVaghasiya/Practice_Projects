# #!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from blinker import signal

# Define signals
file_selected = signal('file_selected')
progress_updated = signal('progress_updated')
merge_completed = signal('merge_completed')

def select_files():
    """Prompt the user to select PDF files for merging using a file dialog."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    pdf_files = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[("PDF Files", "*.pdf")],
        multiple=True
    )
    root.destroy()  # Close the root window
    file_selected.send(pdf_files)
    return pdf_files

def merge_pdfs(file_list, output_filename):
    """Merge the selected PDFs and save the output file."""
    writer = PdfWriter()
    total_files = len(file_list)

    for index, file_path in enumerate(file_list):
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                writer.add_page(page)
            progress_percentage = ((index + 1) / total_files) * 100
            progress_updated.send(progress_percentage)
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    with open(output_filename, 'wb') as output_file:
        writer.write(output_file)
    merge_completed.send(output_filename)

def on_file_selected(sender):
    print(f"Files selected: {sender}")

def on_progress_updated(sender):
    print(f"Progress: {sender:.2f}%")

def on_merge_completed(sender):
    print(f"Merging completed. Output saved as: {sender}")
    try:
        os.startfile(sender)  # Works only on Windows
    except AttributeError:
        messagebox.showinfo("Saved", f"File saved as {sender}")

def main():
    # Connect signals to their respective handlers
    file_selected.connect(on_file_selected)
    progress_updated.connect(on_progress_updated)
    merge_completed.connect(on_merge_completed)

    # Select files and merge them
    selected_files = select_files()
    if selected_files:
        root = tk.Tk()
        root.withdraw()
        output_filename = filedialog.asksaveasfilename(
            title="Save Merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        root.destroy()

        if output_filename:
            merge_pdfs(selected_files, output_filename)

if __name__ == "__main__":
    main()
