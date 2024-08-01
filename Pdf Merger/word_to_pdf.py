import tkinter as tk
from tkinter import filedialog, messagebox
import docx2pdf
import os


def convert_docx_to_pdf():
    docx_filename = filedialog.askopenfilename(filetypes=[("Word File", "*.docx")])

    if not docx_filename:
        return

    base_filename = os.path.splitext(os.path.basename(docx_filename))[0]

    pdf_filename = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        initialfile=base_filename,
    )

    if not pdf_filename:
        return

    try:
        docx2pdf.convert(docx_filename, pdf_filename)

        # Check if the PDF filename ends with ".pdf" extension
        if not pdf_filename.lower().endswith(".pdf"):
            raise ValueError("Invalid PDF filename")

        os.startfile(pdf_filename)
    except Exception as e:
        messagebox.showerror("Error", f"File conversion failed: {e}")


def main():
    root = tk.Tk()
    root.withdraw()
    convert_docx_to_pdf()
    root.destroy()


if __name__ == "__main__":
    main()
