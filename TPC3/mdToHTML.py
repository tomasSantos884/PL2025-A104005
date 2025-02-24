import re

def convert(filepath):
    ol = 0
    
    def header(line):
        if ol == 1:
            return "</ol><h1>" + line[2:] + "</h1>"
        else:
            return "<h1>" + line[2:] + "</h1>"
    
    def bold(line):
        if ol == 1:
            return "</ol><b>" + line + "</b>"
        else:
            return "<b>" + line + "</b>"
    
    def italic(line):
        if ol == 1:
            return "</ol><i>" + line + "</i>"
        else:
            return "<i>" + line + "</i>"
    
    def ol(line):
        nonlocal ol
        if ol == 0:
            ol = 1
            return "<ol><li>" + line + "</li>"
        else:
            return "<li>" + line + "</li>"
    
    def link(line):
        if ol == 1:
            return "</ol><a href=\"" + line + "\">" + line + "</a>"
        else:
            return "<a href=\"" + line + "\">" + line + "</a>"
    
    def image(line):
        if ol == 1:
            return "</ol><img src=\"" + line + "\">"
        else:
            return "<img src=\"" + line + "\">"
    
    def default(line):
        return line
    
    switch = {
        "#": header,
        "**": bold,
        "*": italic,
        "[": link,
        "!": image
    }
    
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if re.match(r'^\d+\.$', line):
                result = ol(line)
            elif (line == ""):
                continue
            else:
                result = switch.get(line[0], default)(line)
            print(result)
            
            
convert('test.md')