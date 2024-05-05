import os
import PyPDF2
import csv
from itertools import izip

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

def break_tag_set_to_list(tag_set: set[str]) -> dict[str, list[str]]:
    tag_set_display = {"a":[], "b":[], "c":[], "d":[], "e":[], "f":[], "g":[], "h":[], "i":[], "j":[], "k":[], "l":[], "m":[], "n":[], "o":[], "p":[], "q":[], "r":[], "s":[], "t":[], "u":[], "v":[], "w":[], "x":[], "y":[], "z":[]}
    for tag in tag_set:
        tag_set_display[tag[0]].append(tag)
    return tag_set_display
    