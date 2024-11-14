import PyPDF2

def search_in_pdf(file_path, search_word):
    word_count = 0
    page_matches = []

    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(reader.pages)

            for page_num in range(total_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                
                # Count occurrences on the current page
                occurrences = text.lower().count(search_word.lower())
                if occurrences > 0:
                    page_matches.append((page_num + 1, occurrences))
                word_count += occurrences

    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except Exception as e:
        return f"An error occurred: {e}"

    if word_count > 0:
        result = f"The word '{search_word}' was found {word_count} time(s) in the PDF.\n"
        result += "Occurrences by page:\n"
        for page, count in page_matches:
            result += f"  Page {page}: {count} time(s)\n"
        return result
    else:
        return f"The word '{search_word}' was not found in the PDF."

# Example usage:
file_path = 'C:\\Users\\ADMIN\\Desktop\\aiml_ref\\ML.pdf'  # Replace with your PDF file path
search_word = 'Machine learning'  # Replace with the word you want to search for
print(search_in_pdf(file_path, search_word))
