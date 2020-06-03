import os
import sys

import keyboard
import asyncio
import psutil
from win32 import win32api, win32print

import map_files
import utility


def prepareFilesToPrint(folder):
    # Scans folder for files with naming convention and puts them in a seperate array to print
    filesToPrint = []

    for file in os.listdir(folder.value):
        if utility.checkFileName(file):
            filesToPrint.append(file)

    return filesToPrint


def preparePrinter():
    # Opens the printer and defines attributes such as duplex mode
    name = win32print.GetDefaultPrinter()
    printdefaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
    handle = win32print.OpenPrinter(name, printdefaults)
    attributes = win32print.GetPrinter(handle, 2)
    attributes['pDevMode'].Duplex = 2  # Lange Seite spiegeln
    win32print.SetPrinter(handle, 2, attributes, 0)

    return handle


async def printFiles(filesToPrint):
    for file in filesToPrint:
        win32api.ShellExecute(
            0, "print", file, '"%s"' % win32print.GetDefaultPrinter(), ".", 0)


def cleanup(handle):
    win32print.ClosePrinter(handle)
    for p in psutil.process_iter():
        if 'AcroRd' in str(p):
            p.kill()


async def printTaskFiles():
    # Iterates over files in downloads folder and prints them if they are task sheets
    os.chdir("C:/Users/Gebker/Downloads/")
    filesToPrint = prepareFilesToPrint(utility.Folder.DOWNLOADS)

    if filesToPrint.__len__() == 0:
        print("No Files to print. Exiting...")
        sys.exit()

    print("=============================================================")
    print("The following files will be printed:")
    for file in filesToPrint:
        print(file)
    print("=============================================================")

    input("Press ENTER to print. Exit with ESC")
    while True:
        try:
            if keyboard.is_pressed('ENTER'):
                print("ENTER pressed. Printing...")
                handle = preparePrinter()
                await printFiles(filesToPrint)
                cleanup(handle)
                print("Done printing. Mapping files now...")
                map_files.scanFolders()
                break
            elif keyboard.is_pressed('ESC'):
                print("ESC pressed. Exiting...")
                sys.exit()
        except:
            break


if __name__ == "__main__":
    asyncio.run(printTaskFiles())
