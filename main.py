# Python >= 3.9.10
# PyPDF2 : python3 -m pip install pypdf2

# Import PyPDF2 Module
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

# Import the os, base 64 module
import os
import base64

watermark = "watermark.pdf"
input_dir = "pdf_to_watermark"
output_dir = "watermarked"

class Reader:

    def __init__(self, path: str, input_dir: str) -> None:
        # Get the current working directory
        self.path = path
        self.input_dir = input_dir
        self.files = []

    def getPDFs(self) -> []:
        print("\n--- Listing PDFs in : " + self.path + " ---\n")
        
        # List files from cwd
        for file in os.listdir(self.path + self.input_dir):
            file_name, file_extension = os.path.splitext(file)
            
            # Only process PDF
            if(file_extension.lower() == ".pdf"):
                self.files.append(file)
                print("- " + file)
        return self.files


class Writer:

    def __init__(self, path: str, watermark : str, input_dir: str,  output_dir : str) -> None:
        # Get the current working directory
        self.path = path
        self.input_dir = input_dir
        self.output_dir = output_dir
        watermark_path = self.path + watermark
        try :
            watermark_pdf = PdfFileReader(open(watermark_path, "rb"), strict=False)
            self.watermark_page = watermark_pdf.getPage(0)
        except Exception:
            print("Cannot read PDF : " + watermark_path)
        self.write_output_dirs()

    def write_output_dirs(self) -> None:
        os.makedirs(self.path + self.output_dir, exist_ok=True)

    def watermark(self, file: str) -> None:
        print("Adding watermark to : " + file)
        try:
            input_pdf = PdfFileReader(open(self.input_dir + "/" + file, "rb"), strict=False)
            output_pdf = PdfFileWriter()
            print("Pages : " + str(input_pdf.getNumPages()))
            # For each page add watermark
            for i in range(input_pdf.getNumPages()):
                # Get page i
                pdf_page = input_pdf.getPage(i)
                # Merge it with watermark page
                pdf_page.mergePage(self.watermark_page)
                # Add merged page to the output_pdf
                output_pdf.addPage(pdf_page)
            # Write output file
            output_path = self.path + self.output_dir + '/' +  file
            output_pdf.write(open(output_path, "w+b"))
            print("Success!")
        except Exception:
            print("Cannot write PDF : " + output_path)

    def worker_watermark(self, files: []) -> None:
        nb_files = str(len(files))
        print("\n--- Watermarking " + nb_files + " PDF ---\n")
        i = 0
        for pdf in files:
            i += 1
            print("\n--- [" + str(i) + "/" + nb_files + "] ---")
            self.watermark(pdf)
        print("\nAll done! Wartermarked files are in " + self.path + self.output_dir )

if __name__ == '__main__':
    cwd = os.getcwd() + "/" # Get current working directory
    writer = Writer(cwd, watermark, input_dir, output_dir) # Init CWD
    reader = Reader(cwd, input_dir) # Init Reader
    pdfs = reader.getPDFs()
    writer.worker_watermark(pdfs)
