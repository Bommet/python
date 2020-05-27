import json
import os

from taskMapPrint import utility


def scanFolders():
    # Scans all Folders specified in enum "Folders"
    os.chdir("C:/Users/Gebker/OneDrive - Universität Münster/Dokumente")

    for folder in utility.Folder:
        print("\n")
        print("==========================================================================")
        print(folder.name)

        scanAndMoveFilesInDirectory(folder)

        print("==========================================================================")

    input("\n\n=====================================================\nEnter zum Bestätigen\n=====================================================")


def scanAndMoveFilesInDirectory(folder):
    # Scans given folder for files with namin convention and moves them to their specific directory
    for file in os.listdir(folder.value):
        print("----------------------------------------------------------------------------------------")
        print(file)

        pathNameBefore = os.path.abspath(folder.value + file)
        fachOrdnerName = utility.checkFileName(file)

        if fachOrdnerName == "":
            print("checkFileName --> fachOrdnerName --> " + fachOrdnerName)
            continue

        pathNamesAfter = buildNewPath(file, fachOrdnerName, folder)

        if pathNamesAfter == None:
            continue

        if os.path.exists(pathNamesAfter["pathWithout"]) == False:
            print("scanAndMoveFilesInDirectory --> mkdir")
            os.mkdir(pathNamesAfter["pathWithout"])

        os.replace(pathNameBefore, pathNamesAfter["pathWith"])
        print("Moved " + file + " successfully to: " +
              pathNamesAfter["pathWith"])


def buildNewPath(file, fachOrdnerName, folder):
    # Builds a new path name based on the filename, the directory name correlating to the filename by convention and the source folder
    pathNameAfterWithoutFile = os.path.abspath(
        os.getcwd() + "/Uni/Module/" + fachOrdnerName + "/Aufgaben")

    blattMitNummer = ""
    if folder == utility.Folder.SCANS:
        afterBIndex = file.index("_B") + 2
        blattMitNummer = "/Blatt" + file[afterBIndex: afterBIndex + 2]
    elif folder == utility.Folder.DOWNLOADS:
        afterKürzelIndex = file.index("_Blatt")+1
        blattMitNummer = "/" + file[afterKürzelIndex: afterKürzelIndex + 7]

    if blattMitNummer:
        print("buildNewPath --> blattNummer --> " + blattMitNummer)
        pathNameAfterWithoutFile = os.path.abspath(
            pathNameAfterWithoutFile + blattMitNummer)
        pathNameAfterWithFile = os.path.abspath(
            pathNameAfterWithoutFile + "/" + file)

        return {"pathWithout": pathNameAfterWithoutFile, "pathWith": pathNameAfterWithFile}
    else:
        return


if __name__ == "__main__":
    scanFolders()
