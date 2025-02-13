def sumOnOff(text):
    on = True
    sum = 0
    buffer = ""
    
    i = 0
    while i < len(text):
        char = text[i]
        
        if char.isdigit():
            buffer += char
        else:
            if buffer:
                if on:
                    sum += int(buffer)
                buffer = ""
            
            if text[i:i+2].lower() == "on":
                on = True
                i += 1
            elif text[i:i+3].lower() == "off":
                on = False
                i += 2
            elif char == "=":
                print(sum)
        
        i += 1
    
    if buffer and on:
        sum += int(buffer)


test = "12Off12on21offola34tudo70bemcomoon10estasOn="
sumOnOff(test)
