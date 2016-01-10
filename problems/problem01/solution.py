def readFromInput(filename):
    return open(filename).readline()


def getHearsFromLine(line):
    hearts, i = 0, 0
    while i < len(line)-1:
        if line[i] == '<' and line[i+1] == '3':
            hearts += 1
            i += 1

        i += 1

    return hearts

if __name__ == "__main__":
    line = readFromInput('input')
    hearts = getHearsFromLine(line)
    print hearts
