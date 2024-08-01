import PyPDF4
import os


pdf_reader = PyPDF4.PdfFileReader("test.pdf")
num_pages = pdf_reader.getNumPages()

new_pdf_file = PyPDF4.PdfFileWriter()

temp = input("Enter the list items separated by spaces: ").split()

pages_going_to_change = [int(item) - 1 for item in temp if int(item) > 0]

pages_going_to_remain_same = [
    i for i in range(num_pages) if i not in pages_going_to_change
]

for i in pages_going_to_change + pages_going_to_remain_same:
    new_pdf_file.addPage(pdf_reader.getPage(i))

with open("new_my_pdf.pdf", "wb") as f:
    new_pdf_file.write(f)

os.startfile("new_my_pdf.pdf")
