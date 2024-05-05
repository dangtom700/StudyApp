import numpy as np
import matplotlib as mpl
import PyQt5
import argparse
import modules.DataProcess as DataProcess
import modules.Export as Export
import modules.path as path

def app():
    
    parser = argparse.ArgumentParser(prog="Study Logging and Database",
                                     description="This project is to meant to store record of learning activities. The files and record of activities are then transfer into database that show user the timeline and activities done in that day.",
                                     add_help=True,
                                     allow_abbrev=True)
    
    parser.add_argument("--exportTagSet", action= True, help="Export a tag set to a file named 'tags.md' in the specified folder path")
    parser.add_argument("--exportPDF_info", action= True, help="Export a CSV file with the size and tags of the files in the specified folder path")
    parser.add_argument("--exportPDF_index", action= True, help="Export a list of PDF file in a given directory in .md format")
    parser.add_argument("--updateStat", action= True, help="Update the statistics of PDF files")
    parser.add_argument("--exportPDF_tokens", action= True, help="Export a CSV file with the tokens of the files in the specified folder path")

    args = parser.parse_args()

    if args.exportTagSet:
        banned_word = DataProcess.get_banned_words(path.ban_path)
        Export.exportTagSet(path.BOOKS_folder_path, banned_word)
        Export.AnnounceFinish()

    if args.exportPDF_info:
        banned_word = DataProcess.get_banned_words(path.ban_path)
        Export.exportPDF_info(path.BOOKS_folder_path, banned_word)
        Export.AnnounceFinish()

    if args.exportPDF_index:
        Export.exportPDF_index(path.BOOKS_folder_path)
        Export.AnnounceFinish()

    if args.updateStat:
        Export.updateStat(path.PDF_info_path)
        Export.AnnounceFinish()

    if args.exportPDF_tokens:
        Export.exportPDF_tokens(path.PDF_info_path)
        Export.AnnounceFinish()

if __name__ == '__main__':
    app()
