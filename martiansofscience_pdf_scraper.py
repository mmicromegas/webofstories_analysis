# https://www.geeksforgeeks.org/extract-text-from-pdf-file-using-python/

# importing required modules
import PyPDF2
import sys

# creating a pdf file object
pdfFileObj = open('pdf/The_Martians_of_Science_ Five_Physicists_Who_Changed_the_Twentieth_Century_PDFDrive.pdf','rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
# print(pdfReader.numPages)

NamesList = ["Theodore von Karman","Leo Szilard","Eugene P Wigner","John von Neumann","Edward Teller"]
NamesRangeDict = {NamesList[0]: [[29,32],[58,67]]}
NamesRangeDict[NamesList[1]] = [[32,34],[67,76]]
NamesRangeDict[NamesList[2]] = [[34,35],[76,83]]
NamesRangeDict[NamesList[3]] = [[35,36],[83,85]]
NamesRangeDict[NamesList[4]] = [[36,37],[85,89]]


#for name in NamesList:
#    for rg in NamesRangeDict[name]:
#        for i in range(rg[0],rg[1]):
#            print(i)

for name in NamesList:
    output = ""
    for rg in NamesRangeDict[name]:
        output += "** page range ** {}-{}: ".format(rg[0],rg[1])
        for i in range(rg[0],rg[1]):
            pageObj = pdfReader.getPage(i)
            output += pageObj.extractText()


    filename = "pdf/martians/{}.txt".format(name.replace(" ", "-"))
    file_object = open(filename, 'a', encoding="utf-8")
    file_object.write(name + "\n")

    file_object.write(output)
    # Close the file
    file_object.close()

# closing the pdf file object
pdfFileObj.close()

