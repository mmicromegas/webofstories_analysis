import requests
from bs4 import BeautifulSoup
import sys

# https://realpython.com/beautiful-soup-web-scraper-python/

storytellers = []
for i in range(1,6):
    URL = "https://www.webofstories.com/storytellers?s={}&sortBy=alpha_asc&filterBy=all".format(i)
    #URL = "https://www.webofstories.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("table")
    #storytellers_elements_themeStoryVertical = results.find_all("div", class_="themeStoryVertical")
    storytellers_elements_first = results.find_all("div", class_="first")

    for name in storytellers_elements_first:
        storytellers.append(name.get_text().strip().split('-')[0].lower().replace(" ",".").rstrip("\t").rstrip("\r\n"))

#print(storytellers[46:])
#sys.exit()

#for name in storytellers:
#for name in storytellers[45:]:

#for name in ["jj.norwich"]:
#for name in ["benoit.mandelbrot"]:
#for name in ["jj.lipski"]:
#for name in ["redmond.ohanlon"]:
#for name in ["francois.jacob","julia.hartwig","w.d.snodgrass","jacek.kuron","murray.gell-mann","Avnery","jc.carriere"]:
#for name in ["antony.hewish"]:
for name in ["jj.norwich","benoit.mandelbrot","jj.lipski","redmond.ohanlon","antony.hewish",
             "francois.jacob","julia.hartwig","w.d.snodgrass","jacek.kuron","murray.gell-mann","Avnery","jc.carriere"]:
    # Open a file with access mode 'a'
    filename = "stories/{}.txt".format(name.replace(".","-"))
    file_object = open(filename, 'a', encoding="utf-8")
    file_object.write(name+ "\n")
    writeBiography = True
    for j in range(1,380):
        try:
            URL = "https://www.webofstories.com/play/{}/{}".format(name,j)
            print(URL)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")

            if writeBiography:
                biography = soup.find("div", {"id": "biography"})
                file_object.write(biography.get_text())
                writeBiography=False

            transcript = soup.find("div", class_="transcriptTabContent")
            # Append at the end of file
            file_object.write(transcript.get_text())
            #biography = soup.find("div", {"id": "biography"})
            #info = soup.find("div", {"id": "info"})
            #print(transcript.get_text())
            #print(biography.get_text().strip())
            #print("   ")
            #print(repr(info.get_text().strip()))
        except:
            pass

    # Close the file
    file_object.close()
