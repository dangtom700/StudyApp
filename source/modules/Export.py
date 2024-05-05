import modules.DataProcess as DataProcess
import modules.path as path
from datetime import datetime
from os.path import getmtime
from csv import reader

def AnnounceFinish() -> None:
    print("Process executed successfully finished.")

def execute_exportTagSet(destinationPath: str, CHARACTER: set[str], tag_set_display: dict[str, list[str]]) -> None:
    with open(destinationPath, "w") as outputFile:
        outputFile.write("# Tags\n")
        for char in CHARACTER:
            outputFile.write(f"\n## {char.upper()}\n\n")
            if tag_set_display[char] == []:
                outputFile.write("There is no tag in this category.")
            for tag in tag_set_display[char]:
                outputFile.write(f" #{tag}")
            outputFile.write("\n")

def exportTagSet(folderPath: str, banned_words: set[str]) -> None:
    word_set = sorted(DataProcess.get_tuned_word_list_from_folder(folderPath, banned_words))
    tag_set_display = DataProcess.break_tag_set_to_list(word_set)
    CHARACTER = tag_set_display.keys()

    execute_exportTagSet(path.TagCatalog_path, CHARACTER, tag_set_display)
    execute_exportTagSet(path.Obsidian_TagCatalog_path, CHARACTER, tag_set_display)

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

def updateStat(PDF_info_file: str) -> None:
    with open(PDF_info_file, "r") as csv_file:
        csvreader = reader(csv_file, delimiter = ';')
        data = list(zip(*csvreader))
    title, title_length_char, title_length_word, multi_tags, tag_number, pages, updated_time = data
    with open(path.TableStat_path, "w") as outputFile:
        outputFile.write("| Characteristic| Title Length (char)| Title Length (word)| Tag Number | Pages |\n")
        outputFile.write("| --- | --- | --- | --- | --- |\n")
        outputFile.write(f"|Maximum| {max(title_length_char)} | {max(title_length_word)} | {max(tag_number)} | {max(pages)} |\n")
        outputFile.write(f"|Minimum| {min(title_length_char)} | {min(title_length_word)} | {min(tag_number)} | {min(pages)} |\n")
        outputFile.write(f"|Avarage| {sum(title_length_char) / len(title_length_char):.2f} | {sum(title_length_word) / len(title_length_word):.2f} | {sum(tag_number) / len(tag_number):.2f} | {sum(pages) / len(pages):.2f} |\n")
        outputFile.write(f"|Total| {sum(title_length_char)} | {sum(title_length_word)} | {sum(tag_number)} | {sum(pages)} |\n")
        sorted(title_length_char)
        sorted(title_length_word)
        sorted(tag_number)
        sorted(pages)
        outputFile.write(f"|Median| {title_length_char[len(title_length_char) // 2]} | {title_length_word[len(title_length_word) // 2]} | {tag_number[len(tag_number) // 2]} | {pages[len(pages) // 2]} |\n")

        outputFile.write(f"\nLongest title by characters: {title[title_length_char.index(max(title_length_char))]}")
        outputFile.write(f"\nShortest titleby charcters: {title[title_length_char.index(min(title_length_char))]}")
        outputFile.write(f"\nLongest title by words: {title[title_length_word.index(max(title_length_word))]}")
        outputFile.write(f"\nShortest title by words: {title[title_length_word.index(min(title_length_word))]}")

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