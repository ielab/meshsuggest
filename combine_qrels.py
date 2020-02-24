from qrels_paths import *
import re


def main():
    for path in SEARCH_QRELS_PATHS[:4]:
        out = open(SEARCH_QRELS_PATHS[4], "a+")
        fragments = path.rsplit("/", 1)
        actualPath = fragments[0]
        year = fragments[1]
        with open(actualPath, "r") as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for each in content:
            splitedLine = re.split(r' +', each)
            line = "{} 0 {} {}\n".format("{}_{}".format(year, splitedLine[0]), splitedLine[2], splitedLine[3])
            out.write(line)


if __name__ == '__main__':
    main()
