import shutil
import requests
import json

symbols = ['*', '"', '[MeSH Terms]']


def readFile(path, mode, file):
    if mode is "c":
        queryContent = file.read()
        # lineSeperator("-")
        writeFile(path, "atm_progress", "*********************************************************\n")
        # print("Sub-Clause Content: " + queryContent)
        writeFile(path, "atm_progress", "Sub-Clause Content: \n" + queryContent + "\n")
        generatedMesh = requestForSearchDetails(path, queryContent)
        return generatedMesh
    else:
        meshContent = file.read()
        meshs = meshContent.split("\n")
        cleanedMeshs = cleanTerms(meshs)
        # lineSeperator("-")
        writeFile(path, "atm_progress", "*********************************************************\n")
        # print("Original MeSH Terms: ")
        writeFile(path, "atm_progress", "Original MeSH Terms: \n")
        for mesh in cleanedMeshs:
            #     print(mesh)
            writeFile(path, "atm_progress", mesh + "\n")
        return cleanedMeshs


def requestForSearchDetails(path, query):
    configF = open("config.json", "r")
    config = json.loads(configF.read())
    url = config["url"] + "?db=pubmed&api_key=" + config["key"] + "&retmode=json&term=" + query
    response = requests.get(url, params=None)
    res = json.loads(response.content)
    translationStack = res["esearchresult"]["translationstack"]
    # generatedQuery = res["esearchresult"]["querytranslation"]
    generatedMesh = getATMMeSHTerms(translationStack)
    # print("Generated Query: " + generatedQuery)
    # writeFile(path, "progress", "Generated Query: \n" + generatedQuery)
    # lineSeperator("-")
    writeFile(path, "atm_progress", "*********************************************************\n")
    # print("Generated MeSH Terms: ")
    writeFile(path, "atm_progress", "Generated MeSH Terms: \n")
    for mesh in generatedMesh:
        #     print(mesh)
        writeFile(path, "atm_progress", mesh + "\n")
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
    f = open(path + "/" + filename, "a+")
    f.write(data)
    return


# From https://gist.github.com/greenstick/b23e475d2bfdc3a82e34eaa1f6781ee4
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', autosize=False):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    if autosize:
        cols, _ = shutil.get_terminal_size(fallback=(length, 1))
        length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end='\r')
    if iteration == total:
        print()


def lineSeperator(fill='#', length=100):
    styling = '%s' % fill
    cols, _ = shutil.get_terminal_size(fallback=(length, 1))
    length = cols - len(styling)
    bar = fill * length
    print('\r%s' % styling.replace(fill, bar), end='\r')
    print()
