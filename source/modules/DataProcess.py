import os
import PyPDF2

def get_banned_words(filepath: str) -> set[str]:
    """
    Reads a file at the given `filepath` and returns a sorted set of banned words.

    Parameters:
        filepath (str): The path to the file containing the banned words.

    Returns:
        set[str]: A sorted set of banned words.
    """
    banned_words = set()
    with open(filepath, 'r') as file:
        for line in file:
            banned_words.add(line.strip())
    return sorted(banned_words)

def get_pdf_name(folderPath: str) -> list[str]:
    """
    Get the names of PDF files in the specified folder path.

    Parameters:
        folderPath (str): The path to the folder containing the PDF files.

    Returns:
        list[str]: A list of PDF file names in the folder, sorted alphabetically.
    """
    fileList = os.listdir(folderPath)
    pdfNameList = []
    for file in fileList:
        if file.endswith(".pdf"):
            pdfNameList.append(file.removesuffix(".pdf"))
    return sorted(pdfNameList)

def get_double_word_list_from_file(word_list: list[str], banned_words: set[str]) -> set[str]:
    """
    Generate a set of two-word tags from a given list of words, excluding any tags that contain banned words.

    Parameters:
    - word_list (list[str]): A list of words from which to generate two-word tags.
    - banned_words (set[str]): A set of words that should be excluded from the generated two-word tags.

    Returns:
    - two_word_tags (set[str]): A set of two-word tags generated from the input word list, excluding any tags that contain banned words.
    """
    two_word_tags = set()
    for i in range(len(word_list) - 1):
        tag = word_list[i] + "_" + word_list[i+1]
        if all(word not in banned_words for word in tag.split("_")):
            two_word_tags.add(tag)
    return two_word_tags


def get_word_list_from_file(filename: str, banned_words: set[str]) -> set[str]:
    """
    Generate a set of words from a given filename, excluding banned words and double words.

    Parameters:
        filename (str): The name of the file to extract words from.
        banned_words (set[str]): A set of words that should be excluded from the generated word list.

    Returns:
        set[str]: A sorted set of words extracted from the filename, excluding banned words and double words.
    """
    word_list = filename.strip().split()
    single_word_set = set(word_list)
    double_word_set = get_double_word_list_from_file(word_list, banned_words)
    tuned_word_list = single_word_set.difference(banned_words, banned_words)
    tuned_word_list = tuned_word_list.union(double_word_set)
    return sorted(tuned_word_list)

def get_tuned_word_list_from_folder(folderPath: str, banned_words: set[str]) -> set[str]:
    """
    Generate a sorted set of tuned words from a given folder path by filtering out specific banned words.

    Parameters:
    - folderPath (str): The path to the folder containing files.
    - banned_words (set[str]): A set of words to exclude from the tuned word list.

    Returns:
        tuned_word_list (set[str]): A sorted set of unique words extracted from the file names in the folder after removing banned words.
    """
    word_set = set()
    filename_list = get_pdf_name(folderPath)
    for filename in filename_list:
        word_set = word_set.union(get_word_list_from_file(filename, banned_words))
    return sorted(word_set)

def get_page_count(pdf_path: str) -> int:
    """
    Returns the number of pages in a PDF file given its path.

    Parameter:
    - pdf_path (str): A string representing the path to the PDF file.

    Return:
       page_count (int): An integer representing the number of pages in the PDF file.
    """
    pdfFileObj = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    Pages = pdfReader.numPages
    return str(Pages)

def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)

def break_tag_set_to_list(tag_set: set[str]) -> dict[str, list[str]]:
    """
    Given a set of tags, this function breaks down the set into a dictionary where each key represents the first letter of a tag and the corresponding value is a list of all the tags that start with that letter. 

    Parameter:
    - tag_set (set[str]): A set of strings representing the tags.

    Return:
        tag_set_display (dict[str, list[str]]): A dictionary where each key represents the first letter of a tag and the corresponding value is a list of all the tags that start with that letter.
    """
    tag_set_display = {"a":[], "b":[], "c":[], "d":[], "e":[], "f":[], "g":[], "h":[], "i":[], "j":[], "k":[], "l":[], "m":[], "n":[], "o":[], "p":[], "q":[], "r":[], "s":[], "t":[], "u":[], "v":[], "w":[], "x":[], "y":[], "z":[]}
    for tag in tag_set:
        if any(word in tag for word in ["C++", "C#"]):
            # replace C++ and C# with C_pp and C_sharp in the double word
            tag = tag.replace("C++", "C_pp").replace("C#", "C_sharp")
        
        tag_set_display[tag[0].lower()].append(tag)
    return tag_set_display
