

def rLines(file):
    completeLine = ""
    insideQuotes = False
    
    for rawLine in file:
        line = rawLine.strip()
        completeLine += (" " if completeLine else "") + line 
        insideQuotes ^= line.count('"') % 2  
        
        if not insideQuotes:
            yield completeLine
            completeLine = ""
    
    if completeLine:
        yield completeLine


def splitLine(line, delimiter=';', quotechar='"'):
    parts = []
    current = []
    insideQuotes = False
    
    for char in line:
        if char == quotechar:
            insideQuotes = not insideQuotes
        elif char == delimiter and not insideQuotes:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    
    parts.append("".join(current).strip())
    return parts


def parseCSV(fPath):
    composers = set()
    trackDist = {}
    trackPerPeriod = {}
    
    with open(fPath, "r", encoding="utf-8") as file:
        headerFields = splitLine(next(file).strip())
        
        nameIndex = headerFields.index("nome")
        periodIndex = headerFields.index("periodo")
        composerIndex = headerFields.index("compositor")
        
        for line in rLines(file):
            campos = splitLine(line.strip())
            if len(campos) < max(nameIndex, periodIndex, composerIndex) + 1:
                continue  
            
            nome, periodo, compositor = campos[nameIndex].strip(), campos[periodIndex].strip(), campos[composerIndex].strip()
            composers.add(compositor)
            
            trackDist[periodo] = trackDist.get(periodo, 0) + 1
            trackPerPeriod.setdefault(periodo, []).append(nome)
    
    return composers, trackDist, trackPerPeriod

def main():
    
    composers, trackDist, trackPerPeriod = parseCSV('obras.csv')
    print("Compositores:")
    print(sorted(composers))
    print("\nDistribuição de Obras:")
    for periodo, quantidade in (trackDist.items()):
        print(f"{periodo}: {quantidade}")
    
    print("\nObras por Período:")
    for periodo, obras in sorted(trackPerPeriod.items()):
        print(f"{periodo}:")
        print((sorted(obras)))
        print()

if __name__ == "__main__":
    main()