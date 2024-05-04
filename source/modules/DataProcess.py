import os
import PyPDF2

def get_banned_words(filepath: str) -> set[str]:
    banned_words = set()
    with open(filepath, 'r') as file:
        for line in file:
            banned_words.add(line.strip())
    return sorted(banned_words)

def get_pdf_name(folderPath: str) -> list[str]:
    fileList = os.listdir(folderPath)
    pdfNameList = []
    for file in fileList:
        if file.endswith(".pdf"):
            pdfNameList.append(file)
    return sorted(pdfNameList)

def get_word_list_from_file(filename: str, banned_words: set[str]) -> set[str]:
    word_list = set(filename.strip().split())
    tuned_word_list = word_list.difference(banned_words)
    return sorted(tuned_word_list)

def get_tuned_word_list_from_folder(folderPath: str, banned_words: set[str]) -> set[str]:
    word_set = set()
    filename_list = get_pdf_name(folderPath)
    for filename in filename_list:
        word_set = word_set.union(get_word_list_from_file(filename, banned_words))
    return sorted(word_set)

def get_page_count(pdf_path: str) -> int:
    pdfFileObj = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    return pdfReader.numPages()

