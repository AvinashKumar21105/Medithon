import PyPDF2


def pdf_to_text(pdf_path, output_path=None):
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            # Extract text from each page
            for page in reader.pages:
                text += page.extract_text()

            # Save to a text file if output_path is provided
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)
                print(f"Text extracted and saved to {output_path}")
            else:
                print("Extracted Text:")
                print(text)

            return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example Usage
pdf_path = "Patient-1.pdf"  # Replace with your PDF file path
output_path = "output.txt"  # Optional: Replace with your desired text file path
pdf_to_text(pdf_path, output_path)