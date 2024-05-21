import os
from os.path import getmtime
from time import ctime
from datetime import datetime
import statistics
from math import ceil
import random

def get_banned_words(filepath: str) -> set[str]:
    """
    Reads a file at the given `filepath` and returns a sorted set of banned words.

    Parameters:
        filepath (str): The path to the file containing the banned words.

    Returns:
        set[str]: A sorted set of banned words.

    This function reads a file at the given `filepath` and adds each line to a set of banned words.
    The lines are stripped of any leading or trailing whitespace before being added to the set.
    The set is then sorted and returned.
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

def get_double_word_list_from_file(word_list: list[str]) -> set[str]:
    two_word_tags = set()
    for i in range(len(word_list) - 1):
        tag = word_list[i] + "_" + word_list[i+1]
        two_word_tags.add(tag)
    return two_word_tags

def get_triple_word_list_from_file(word_list: list[str]) -> set[str]:
    three_word_tags = set()
    for i in range(len(word_list) - 2):
        tag = word_list[i] + "_" + word_list[i+1] + "_" + word_list[i+2]
        three_word_tags.add(tag)
    return three_word_tags

def get_word_list_from_file(filename: str, banned_words: set[str]) -> set[str]:
    """
    Generate a set of words from a given filename, excluding banned words and double words.

    Parameters:
        filename (str): The name of the file to extract words from.
        banned_words (set[str]): A set of words that should be excluded from the generated word list.

    Returns:
        set[str]: A sorted set of words extracted from the filename, excluding banned words and double words.

    This function splits the filename into words, creates a set of tuned words by removing duplicates, and then
    adds double and triple word tags to the set. It replaces "C++" with "C_pp" and "C#" with "C_sharp" in the
    tuned words. Finally, it removes the banned words from the set and returns the sorted set of tuned words.
    """
    words = filename.strip().split()
    tuned_words = set(words)
    double_words = get_double_word_list_from_file(words)
    triple_words = get_triple_word_list_from_file(words)

    tuned_words = tuned_words.union(double_words)
    tuned_words = tuned_words.union(triple_words)
    tuned_words = {word.replace("C++", "C_pp").replace("C#", "C_sharp") for word in tuned_words}
    tuned_words = tuned_words.difference(banned_words)
    return sorted(tuned_words)

def get_tuned_word_list_from_folder(folderPath: str, banned_words: set[str]) -> set[str]:
    """
    Generate a sorted set of tuned words from a given folder path, excluding banned words.

    Args:
        folderPath (str): The path to the folder containing the PDF files.
        banned_words (set[str]): A set of words to be excluded from the generated word list.

    Returns:
        set[str]: A sorted set of tuned words extracted from the PDF files in the folder, excluding banned words.

    This function retrieves the filenames of PDF files in the specified folder path using the `get_pdf_name` function.
    It then iterates over each filename and calls the `get_word_list_from_file` function to extract the words from the PDF file.
    The extracted words are added to the `word_set` set using the `union` method. Finally, the `word_set` is sorted and returned.

    Note: The `get_pdf_name` and `get_word_list_from_file` functions must be imported for this function to work properly.
    """
    word_set = set()
    filename_list = get_pdf_name(folderPath)
    for filename in filename_list:
        word_set = word_set.union(get_word_list_from_file(filename, banned_words))
    return sorted(word_set)

def get_file_size(file_path: str) -> int:
    """
    Calculate the file size in kilobytes for a given file path.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        int: The file size in kilobytes.
    """
    return int(ceil(os.path.getsize(file_path)/1024))

def get_updated_time(file_path: str) -> str:
    """
    Given a file path, this function retrieves the modification time of the file and converts it to a recognizable timestamp.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        str: The modification time of the file in the format of '%a, %b %d, %Y, %H:%M:%S'.
    """
    # Get the modification time in seconds since EPOCH
    modification_time = getmtime(file_path)
    # Convert the modification time to a recognizable timestamp
    formatted_modification_time = ctime(modification_time)
    formatted_modification_time = datetime.fromtimestamp(modification_time).strftime('%a, %b %d, %Y, %H:%M:%S')
    return formatted_modification_time

def get_current_time() -> str:
    """
    Returns the current date and time in the format of day of the week, abbreviated month, day of the month, and year.

    :return: A string representing the current date and time in the format of '%a, %b %d, %Y'.
    :rtype: str
    """
    return datetime.now().strftime('%a, %b %d, %Y')

def break_tag_set_to_list(tag_set: set[str]) -> dict[str, list[str]]:
    """
    Given a set of tags, this function breaks down the set into a dictionary where each key represents the first letter of a tag and the corresponding value is a list of all the tags that start with that letter. 

    Parameter:
    - tag_set (set[str]): A set of strings representing the tags.

    Return:
        tag_set_display (dict[str, list[str]]): A dictionary where each key represents the first letter of a tag and the corresponding value is a list of all the tags that start with that letter.
    """
    tag_set_display = {"a":[], "b":[], "c":[], "d":[], "e":[], "f":[], "g":[], "h":[], "i":[], "j":[], "k":[], "l":[], "m":[], "n":[], "o":[], "p":[], "q":[], "r":[], "s":[], "t":[], "u":[], "v":[], "w":[], "x":[], "y":[], "z":[], "mics": []}
    for tag in tag_set:
        if tag[0].isnumeric() == True:
            tag_set_display["mics"].append(tag)
        else:
            tag_set_display[tag[0].lower()].append(tag)
    return tag_set_display

def analyze_characteristic_of_property(property: list[str]) -> dict[str,int]:
    """
    Analyzes the characteristic of a given property.

    Args:
        property (list[str]): A list of strings representing the property values. The first element of the list is the property name.

    Returns:
        dict[str, int]: A dictionary containing the following characteristics of the property:
            - "Property" (str): The name of the property.
            - "Minimum" (int): The minimum value of the property.
            - "Maximum" (int): The maximum value of the property.
            - "Total" (int): The sum of all the property values.
            - "Avarage" (float): The average value of the property rounded to 3 decimal places.
            - "Harmonic Mean" (float): The harmonic mean of the property rounded to 3 decimal places.
            - "Median" (int): The median value of the property.
            - "Mode" (int): The mode value of the property.
            - "Population Standard Deviation" (float): The population standard deviation of the property rounded to 3 decimal places.
            - "Standard Deviation" (float): The standard deviation of the property rounded to 3 decimal places.
            - "Population Variance" (float): The population variance of the property rounded to 3 decimal places.
            - "Variance" (float): The variance of the property rounded to 3 decimal places.
    """
    int_property = list(map(int, property[1:]))
    sorted(int_property)
    min_property = min(int_property)
    max_property = max(int_property)
    total_property = sum(int_property)
    avg_property = statistics.mean(int_property)
    harmean_property = statistics.harmonic_mean(int_property)
    median_property = statistics.median(int_property)
    mode_property = statistics.mode(int_property)
    population_stdev_property = statistics.pstdev(int_property)
    standard_deviation_property = statistics.stdev(int_property)
    pvariance_property = statistics.pvariance(int_property)
    variance_property = statistics.variance(int_property)

    return {"Property": property[0],
            "Minimum": min_property,
            "Maximum": max_property,
            "Total": total_property,
            "Avarage": round(avg_property,3),
            "Harmonic Mean": round(harmean_property,3),
            "Median": median_property,
            "Mode": mode_property,
            "Population Standard Deviation": round(population_stdev_property,3),
            "Standard Deviation": round(standard_deviation_property,3),
            "Population Variance": round(pvariance_property,3),
            "Variance": round(variance_property,3)}

def get_ordered_timestamps(timestamps: list[str]) -> list[datetime]:
    """
    Given a list of timestamps, this function returns a list of datetime objects sorted in ascending order.
    
    Parameters:
        timestamps (list[str]): A list of timestamps in the format '%a, %b %d, %Y, %H:%M:%S'.
        
    Returns:
        list[datetime]: A list of datetime objects sorted in ascending order.
    """
    ordered_dates = sorted(
        map(
            datetime.strptime, timestamps[1:],
            ['%a, %b %d, %Y, %H:%M:%S'] * (len(timestamps) - 1)
        )
    )
    return ordered_dates

def pick_random_number_items(input_list: list[str], number_of_items: int) -> list[str]:
    """
    Picks a random number of items from a given input list.

    Parameters:
        input_list (list[str]): The list from which to pick the random items.
        number_of_items (int): The number of items to pick randomly.

    Returns:
        list[str]: A list containing the randomly picked items.
    """
    random_items = random.sample(input_list, number_of_items)
    return random_items