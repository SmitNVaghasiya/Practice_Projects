import PyPDF4
import os


def remove_pages(pdf_filename="test.pdf", result_file="output.pdf"):
    try:
        if not pdf_filename or not os.path.exists(pdf_filename):
            print(f"Error: The file {pdf_filename} does not exist.")
            return

        page_numbers = input("Enter the page numbers to remove, separated by commas: ")
        try:
            page_numbers = set(map(int, page_numbers.split(",")))
        except ValueError:
            print(
                "Error: Invalid input. Please enter valid page numbers separated by commas."
            )
            return

        pdf_reader = PyPDF4.PdfFileReader(pdf_filename)
        pdf_writer = PyPDF4.PdfFileWriter()
        num_pages = pdf_reader.getNumPages()

        for page_num in range(num_pages):
            if page_num + 1 not in page_numbers:
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)

        with open(result_file, "wb") as new_pdf_file:
            pdf_writer.write(new_pdf_file)

        print("\nFile saved successfully!")
        os.startfile(result_file)

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    remove_pages()


if __name__ == "__main__":
    main()
