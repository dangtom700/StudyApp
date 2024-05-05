import modules.DataProcess as DataProcess
import modules.path as path
from os.path import getmtime
from csv import reader
from time import ctime

def AnnounceFinish() -> None:
    print("Process executed successfully finished.")

def mirrorFile_to_destination(source: str, destination: str) -> None:
    with open(source, 'r') as read_obj, open(destination, 'w') as write_obj:
        for line in read_obj:
            write_obj.write(line)

def exportTagSet(folderPath: str, banned_words: set[str]) -> None:
    word_set = sorted(DataProcess.get_tuned_word_list_from_folder(folderPath, banned_words))
    tag_set_display = DataProcess.break_tag_set_to_list(word_set)
    CHARACTER = tag_set_display.keys()

    with open(path.TagCatalog_path, "w") as outputFile:
        outputFile.write("# Tags (Total: " + str(len(word_set)) + ")\n")
        for char in CHARACTER:
            outputFile.write(f"\n## {char.upper()} ({len(tag_set_display[char])})\n\n")
            if tag_set_display[char] == []:
                outputFile.write("There is no tag in this category.")
            for tag in tag_set_display[char]:
                outputFile.write(f" #{tag}")
            outputFile.write("\n")
    mirrorFile_to_destination(path.TagCatalog_path, path.Obsidian_TagCatalog_path)

def exportPDF_info(folderPath: str, banned_words: set[str]) -> None:
    filename_list = DataProcess.get_pdf_name(folderPath)

    with open(path.PDF_info_path, "w") as outputFile:
        outputFile.write("Title;Title Length (char);Title Length (word);Multi-Tags;Tag Number;Pages;Updated Time\n")
        for filename in filename_list:
            outputFile.write(f"{filename};")
            outputFile.write(f"{len(filename)};")
            outputFile.write(f"{len(filename.strip().split())};")
            word_list = DataProcess.get_word_list_from_file(folderPath + '/' + filename, banned_words)
            for word in word_list:
                outputFile.write(f" #{word} ")
            outputFile.write(f";{len(word_list)};")
            outputFile.write(f"{DataProcess.get_page_count(folderPath + '/' + filename + ".pdf")};")
            # Get the modification time in seconds since EPOCH
            modification_time = getmtime(folderPath + '/' + filename + ".pdf")
            # Convert the modification time to a recognizable timestamp
            formatted_modification_time = ctime(modification_time)
            outputFile.write(f"{formatted_modification_time}\n")

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