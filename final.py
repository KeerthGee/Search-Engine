import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

def search_in_pdf(file_path, search_word):
    word_count = 0
    total_words = 0
    page_matches = []

    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(reader.pages)

            for page_num in range(total_pages):
                page = reader.pages[page_num]
                text = page.extract_text() or ""  # Handle cases where text is None
                
                # Count total words on this page
                total_words += len(text.split())

                # Count occurrences of the search word on this page
                occurrences = text.lower().count(search_word.lower())
                if occurrences > 0:
                    page_matches.append((page_num + 1, occurrences))
                word_count += occurrences

    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except Exception as e:
        return f"An error occurred: {e}"

    if word_count > 0:
        result = f"Total words in PDF: {total_words}\n"
        result += f"The word '{search_word}' was found {word_count} time(s) in the PDF.\n"
        result += "Occurrences by page:\n"
        for page, count in page_matches:
            result += f"  Page {page}: {count} time(s)\n"
        return result
    else:
        return f"Total words in PDF: {total_words}\nThe word '{search_word}' was not found in the PDF."

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def search_word():
    file_path = entry_file_path.get()
    search_word = entry_search_word.get().strip()
    if not file_path or not search_word:
        messagebox.showerror("Input Error", "Please select a PDF file and enter a search word.")
        return

    result = search_in_pdf(file_path, search_word)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, result)

# Create the main window
root = tk.Tk()
root.title("PDF Search Tool")
root.geometry("600x400")

# File path input
frame_file = tk.Frame(root)
frame_file.pack(pady=10)
tk.Label(frame_file, text="Select PDF File:").pack(side=tk.LEFT, padx=5)
entry_file_path = tk.Entry(frame_file, width=40)
entry_file_path.pack(side=tk.LEFT, padx=5)
tk.Button(frame_file, text="Browse", command=browse_file).pack(side=tk.LEFT)

# Search word input
frame_word = tk.Frame(root)
frame_word.pack(pady=10)
tk.Label(frame_word, text="Enter Word to Search:").pack(side=tk.LEFT, padx=5)
entry_search_word = tk.Entry(frame_word, width=30)
entry_search_word.pack(side=tk.LEFT)

# Search button
tk.Button(root, text="Search", command=search_word, bg="lightblue").pack(pady=10)

# Output text area
text_output = tk.Text(root, height=15, width=70)
text_output.pack(pady=10)

# Run the application
root.mainloop()
