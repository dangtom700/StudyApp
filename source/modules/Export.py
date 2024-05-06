import modules.DataProcess as DataProcess
import modules.path as path
from csv import reader
import json

def AnnounceFinish() -> None:
    print("Process executed successfully finished.")

def mirrorFile_to_destination(source: str, destination: str) -> None:
    with open(source, 'r') as read_obj, open(destination, 'w') as write_obj:
        for line in read_obj:
            write_obj.write(line)

def exportTagSet(folderPath: str, banned_words: set[str]) -> None:
    """
    Export the tag set to a file in the specified folder path.

    Parameters:
        folderPath (str): The path to the folder where the tag set will be exported.
        banned_words (set[str]): A set of words to be excluded from the tag set.

    Returns:
        None

    This function retrieves the tuned word list from the specified folder path using the
    `get_tuned_word_list_from_folder` function from the `DataProcess` module. It then breaks
    the word set into a displayable format using the `break_tag_set_to_list` function from the
    `DataProcess` module. The function writes the tag set to a file specified by the
    `TagCatalog_path` constant from the `path` module. The file is opened in write mode and
    the total number of tags is written as a header. For each character in the displayable
    tag set, the function writes the character and the number of tags associated with it.
    If there are no tags for a character, a message indicating that there are no tags in
    that category is written. The function then writes each tag associated with the character.
    Finally, the function calls the `mirrorFile_to_destination` function to mirror the tag
    catalog file to the Obsidian tag catalog path.

    Note: The `DataProcess` module and the `path` module must be imported for this function
    to work properly.
    """
    word_set = sorted(DataProcess.get_tuned_word_list_from_folder(folderPath, banned_words))
    tag_set_display = DataProcess.break_tag_set_to_list(word_set)
    CHARACTER = tag_set_display.keys()

    with open(path.TagCatalog_path, "w") as outputFile:
        outputFile.write("\n# Tags (Total: " + str(len(word_set)) + ")\n")
        for char in CHARACTER:
            outputFile.write(f"\n## {char.upper()} ({len(tag_set_display[char])})\n\n")
            if tag_set_display[char] == []:
                outputFile.write("There is no tag in this category.")
            for tag in tag_set_display[char]:
                outputFile.write(f" #{tag}")
            outputFile.write("\n")
    mirrorFile_to_destination(path.TagCatalog_path, path.Obsidian_TagCatalog_path)

def exportPDF_info(folderPath: str, banned_words: set[str]) -> None:
    """
    A function to export information about PDF files based on the input folder path and banned words.
    This function retrieves PDF filenames, processes various data about the PDFs, and writes the information to a file.
    
    Parameters:
        folderPath (str): The path to the folder containing the PDF files.
        banned_words (set[str]): A set of words to be excluded during the information extraction process.
    
    Returns:
        None
    """
    filename_list = DataProcess.get_pdf_name(folderPath)

    with open(path.PDF_info_path, "w") as outputFile:
        outputFile.write("Title;Title Length (char);Title Length (word);Multi-Tags;Tag Number;Pages;File Size (byte);Updated Time\n")
        for filename in filename_list:
            outputFile.write(f"{filename};")
            outputFile.write(f"{len(filename)};")
            outputFile.write(f"{len(filename.strip().split())};")
            word_list = DataProcess.get_word_list_from_file(filename, banned_words)
            for word in word_list:
                outputFile.write(f" #{word} ")
            outputFile.write(f";{len(word_list)};")
            outputFile.write(f"{DataProcess.get_page_count(folderPath + '/' + filename + ".pdf")};")
            outputFile.write(f"{DataProcess.get_file_size(folderPath + '/' + filename + ".pdf")};")
            outputFile.write(f"{DataProcess.get_updated_time(folderPath + '/' + filename + ".pdf")}\n")

def exportPDF_index(folderPath: str) -> None:
    """
    A function to export the PDF index to two separate files: PDF_index_path and Obsidian_PDF_index_path. 
    The PDF index contains a list of filenames along with their corresponding indices. 
    The function retrieves the list of PDF filenames using DataProcess.get_pdf_name() and writes the index for each filename to the specified paths. 
    The Obsidian export includes a link to each PDF file in the format [[BOOKS/{filename}.pdf|{filename}]].
    Parameters:
        folderPath (str): The path to the folder containing the PDF files.
    Returns:
        None
    """
    filename_list = DataProcess.get_pdf_name(folderPath)

    with open(path.PDF_index_path, "w") as outputFile:
        outputFile.write("\n# PDF index (Total: " + str(len(filename_list)) + ")\n\n")
        for index, filename in enumerate(filename_list, start= 1):
            outputFile.write(f"{index}. {filename}\n")

    # Export to Obsidian
    with open(path.Obsidian_PDF_index_path, "w") as outputFile:
        outputFile.write("\n# PDF index (Total: " + str(len(filename_list)) + ")\n\n")
        for index, filename in enumerate(filename_list, start= 1):
            outputFile.write(f"{index}. [[BOOKS/{filename}.pdf|{filename}]]\n")


def updateStat(PDF_info_file: str) -> None:

    # Rewrite this code for cleaning look

    # CSV format:Title;Title Length (char);Title Length (word);Multi-Tags;Tag Number;Pages;File Size (byte);Updated Time

    with open(PDF_info_file, "r") as csv_file:
        csvreader = reader(csv_file, delimiter = ';')
        data = list(zip(*csvreader))

    title, title_length_char, title_length_word,multi_tag, tag_number, pages, file_size, updated_time = data

    title_length_char_property = DataProcess.analyze_characteristic_of_property(title_length_char)
    title_length_word_property = DataProcess.analyze_characteristic_of_property(title_length_word)
    tag_number_property = DataProcess.analyze_characteristic_of_property(tag_number)
    pages_property = DataProcess.analyze_characteristic_of_property(pages)
    file_size_property = DataProcess.analyze_characteristic_of_property(file_size)

    timestamp_history = DataProcess.get_ordered_timestamps(updated_time)
    keys = title_length_char_property.keys()

    with open(path.TableStat_path, "w") as outputFile:
        outputFile.write("# Statistic of PDFs\n")
        outputFile.write("\n## Title Stat\n\n")
        outputFile.write("| Characteristic| Title Length (char)| Title Length (word)|\n")
        outputFile.write("| --- | --- | --- |\n")
        for key in keys:
            outputFile.write(f"| {key} | {title_length_char_property[key]} | {title_length_word_property[key]} |\n")
        outputFile.write("\n## Keywords Stat\n\n")
        outputFile.write("| Characteristic| Tag Number | Pages | File Size (byte)|\n")
        outputFile.write("| --- | --- | --- | --- |\n")
        for key in keys:
            outputFile.write(f"| {key} | {tag_number_property[key]} | {pages_property[key]} | {file_size_property[key]} |\n")
        outputFile.write("\n")

        outputFile.write("## Time Stamp History\n\n")
        counter = 0
        for timestamp in timestamp_history:
            if timestamp == timestamp_history[0]:
                outputFile.write(f"Start at {timestamp}\n")
                continue
            if timestamp == timestamp_history[-1]:
                outputFile.write(f"Most Recent at {timestamp}\n")
                continue
            if timestamp == timestamp_history[-2]:
                counter = 2
            outputFile.write(f"=> {timestamp}")
            counter += 1
            if counter < 3:
                outputFile.write(" ")
            else:
                outputFile.write("\n")
                counter = 0
            

    mirrorFile_to_destination(path.TableStat_path, path.Obsidian_TableStat_path)

    with open(path.PropertyStat_tokens_path, "w") as outputFile:
        dict_list = [title_length_char_property, title_length_word_property, tag_number_property, pages_property, file_size_property]
        json_string = json.dumps(dict_list)
        outputFile.write(json_string)

def exportPDF_tokens(PDF_info_file: str) -> None:
    """
    Export PDF tokens from a given PDF info file.

    Parameters:
        PDF_info_file (str): The path to the PDF info file.

    Returns:
        None
    """
    with open(PDF_info_file, "r") as csv_file:
        csvreader = reader(csv_file, delimiter = ';')
        data = list(zip(*csvreader))
    title, title_length_char, title_length_word, multi_tags, tag_number, pages, file_size_byte, updated_time = data
    with open(path.PDF_tokens_path, "w") as outputFile:
        outputFile.write("[\n")
        for i in range(len(title)):
            outputFile.write(f"\t{{\n")
            outputFile.write(f"\t\t\"title\": \"{title[i]}\",\n")
            outputFile.write(f"\t\t\"title_length_char\": \"{title_length_char[i]}\",\n")
            outputFile.write(f"\t\t\"title_length_word\": \"{title_length_word[i]}\",\n")
            outputFile.write(f"\t\t\"multi_tags\": \"{multi_tags[i]}\",\n")
            outputFile.write(f"\t\t\"tag_number\": \"{tag_number[i]}\",\n")
            outputFile.write(f"\t\t\"pages\": \"{pages[i]}\",\n")
            outputFile.write(f"\t\t\"file_size_byte\": \"{file_size_byte[i]}\",\n")
            outputFile.write(f"\t\t\"updated_time\": \"{updated_time[i]}\"\n")
            if i == len(title) - 1:
                outputFile.write("\t}\n")
            else:
                outputFile.write("\t},\n")
        outputFile.write("]\n")