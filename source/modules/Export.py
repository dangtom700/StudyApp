import modules.DataProcess as DataProcess
import modules.path as path
from datetime import datetime
from os.path import getmtime
from csv import reader

def AnnounceFinish() -> None:
    print("Process executed successfully finished.")

def exportTagSet(folderPath: str, banned_words: set[str]) -> None:
    word_set = sorted(DataProcess.get_tuned_word_list_from_folder(folderPath, banned_words))
    tag_set_display = DataProcess.break_tag_set_to_list(word_set)
    CHARACTER = tag_set_display.keys()

    with open(path.TagCatalog_path, "w") as outputFile:
        outputFile.write("# Tags\n")
        for char in CHARACTER:
            outputFile.write(f"\n## {char.upper()}\n")
            for tag in tag_set_display[char]:
                outputFile.write(f" #{tag}")
            outputFile.write("\n")

def exportPDF_info(folderPath: str, banned_words: set[str]) -> None:
    filename_list = DataProcess.get_pdf_name(folderPath)

    with open(path.PDF_info_path, "w") as outputFile:
        outputFile.write("Index;Title;Title Length (char);Title Length (word);Multi-Tags;Tag Number;Pages;Updated Time\n")
        for filename in filename_list:
            outputFile.write(f"{filename};")
            outputFile.write(f"{len(filename)};")
            outputFile.write(f"{len(filename.strip().split())};")
            word_list = DataProcess.get_word_list_from_file(folderPath + '/' + filename, banned_words)
            for word in word_list:
                outputFile.write(f" #{word} ")
            outputFile.write(f"{len(word_list)};")
            outputFile.write(f"{DataProcess.get_page_count(folderPath + '/' + filename)};")
            format_time = datetime.fromtimestamp(getmtime(folderPath + '/' + filename)).strftime('%Y-%m-%d %H:%M:%S')
            outputFile.write(f"{format_time}\n")

def exportPDF_index(folderPath: str) -> None:
    filename_list = DataProcess.get_pdf_name(folderPath)

    with open(path.PDF_index_path, "w") as outputFile:
        for index, filename in enumerate(filename_list):
            outputFile.write(f"{index}. [[{filename}.pdf|{filename}]]\n")

def updateStat() -> None:
    pass

def exportPDF_tokens(PDF_info_file: str) -> None:
    with open(PDF_info_file, "r") as csv_file:
        csvreader = reader(csv_file, delimiter = ';')
        data = list(zip(*csvreader))
    title, title_length_char, title_length_word, multi_tags, tag_number, pages, updated_time = data
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
            outputFile.write(f"\t\t\"updated_time\": \"{updated_time[i]}\"\n")
            if i == len(title) - 1:
                outputFile.write("\t}\n")
            else:
                outputFile.write("\t},\n")
        outputFile.write("]\n")