import shutil

import requests
import json

symbols = ['*', '"', '[MeSH Terms]']


def readFile(mode, file):
    if mode is "c":
        queryContent = file.read()
        # lineSeperator("-")
        # print("Sub-Clause Content: " + queryContent)
        generatedMesh = requestForSearchDetails(queryContent)
        return generatedMesh
    else:
        meshContent = file.read()
        meshs = meshContent.split("\n")
        cleanedMeshs = cleanTerms(meshs)
        # lineSeperator("-")
        # print("Original MeSH Terms: ")
        # for mesh in cleanedMeshs:
        #     print(mesh)
        return cleanedMeshs


def requestForSearchDetails(query):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term=" + query
    response = requests.get(url, params=None)
    res = json.loads(response.content)
    translationStack = res["esearchresult"]["translationstack"]
    # generatedQuery = res["esearchresult"]["querytranslation"]
    generatedMesh = getATMMeSHTerms(translationStack)
    # print("Generated Query: " + generatedQuery)
    # lineSeperator("-")
    # print("Generated MeSH Terms: ")
    # for mesh in generatedMesh:
    #     print(mesh)
    return generatedMesh


def cleanTerms(bucket):
    res = []
    for item in bucket:
        for char in symbols:
            item = item.replace(char, "")
        res.append(item.lower())
    res = list(dict.fromkeys(res))
    return res


def getATMMeSHTerms(translationstack):
    mesh = []
    for item in translationstack:
        if type(item) is not str and item["field"] == "MeSH Terms":
            mesh.append(item["term"])
    res = cleanTerms(mesh)
    return res


def findMatch(original, generated):
    hitMesh = set(original) & set(generated)
    return hitMesh


def writeFile(path, filename, data):
    f = open(path + "/" + filename, "w+")
    f.write(data)
    return


# From https://gist.github.com/greenstick/b23e475d2bfdc3a82e34eaa1f6781ee4
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', autosize=False):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        autosize    - Optional  : automatically resize the length of the progress bar to the terminal window (Bool)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    if autosize:
        cols, _ = shutil.get_terminal_size(fallback=(length, 1))
        length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def lineSeperator(fill='#', length=100):
    styling = '%s' % fill
    cols, _ = shutil.get_terminal_size(fallback=(length, 1))
    length = cols - len(styling)
    bar = fill * length
    print('\r%s' % styling.replace(fill, bar), end='\r')
    print()
