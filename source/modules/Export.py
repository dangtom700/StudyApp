import modules.DataProcess as DataProcess
import modules.path as path
from datetime import datetime
from os.path import getmtime

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
        for index, filename in enumerate(filename_list, start= 1):
            outputFile.write(f"{index};{filename};")
            outputFile.write(f"{len(filename)};")
            outputFile.write(f"{len(filename.strip().split())};")
            word_list = DataProcess.get_word_list_from_file(folderPath + '/' + filename, banned_words)
            outputFile.write(f"{word_list};")
            outputFile.write(f"{len(word_list)};")
            outputFile.write(f"{DataProcess.get_page_count(folderPath + '/' + filename)};")
            format_time = datetime.fromtimestamp(getmtime(folderPath + '/' + filename)).strftime('%Y-%m-%d %H:%M:%S')
            outputFile.write(f"{format_time}\n")

def exportPDF_index(folderPath: str) -> None:
    pass

def updateStat(filename = "PDF_info.csv") -> None:
    pass

def exportPDF_tokens(filename = "PDF_info.csv") -> None:
    pass