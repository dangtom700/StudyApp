import numpy as np
import matplotlib as mpl
import csv
import modules.DataProcess as DataProcess

def AnnounceFinish() -> None:
    print("Process executed successfully finished.")

def exportTagSet(folderPath: str, banned_words: set[str]) -> None:
    word_set = sorted(DataProcess.get_tuned_word_list_from_folder(folderPath, banned_words))
    tag_set_display = DataProcess.break_tag_set_to_list(word_set)
    CHARACTER = tag_set_display.keys()
    with open("tags.md", "w") as outputFile:
        outputFile.write("# Tags\n")
        for char in CHARACTER:
            outputFile.write(f"## {char.upper()}\n")
            for tag in tag_set_display[char]:
                outputFile.write(f" #{tag}")

def exportPDF_info(folderPath: str, banned_words: set[str]) -> None:
    pass

def exportPDF_index(folderPath: str) -> None:
    pass

def updateStat(filename = "PDF_info.csv") -> None:
    pass

def exportPDF_tokens(filename = "PDF_info.csv") -> None:
    pass