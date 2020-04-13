# This function removes words with length less than 3.
def non_stop_words(my_line):
    new_line = ''
    step_word= ''
    for i in my_line.split():
        if len(i) < 3:
            step_word = step_word + ' ' + i
        else:
            new_line = new_line + ' ' + i
    # Write to a file.
    #print ("\n\nSTOP WORD: " + step_word)
    return new_line.lower()

# This function removes anything other than spaces, newline, and alphabets.
def remove_special_char(aline):
    normalized_line = ''
    special_char = ''
    for ch in aline:
        if 'A' <= ch <='Z' or 'a' <= ch <='z' or ch == ' ' or ch =='\t' or ch =='\n' :
            normalized_line = normalized_line + ch            
        else:
            normalized_line = normalized_line +  ' '  
            special_char = special_char + ' ' + ch
    # Write to a file.
    #print ("\n\nSpecial Char: " + special_char)            
    return normalized_line

inputFile = open(r'Test (Family).txt', 'r')
outputFile = open(r'Test (FClean).txt', 'w')

for new_line in inputFile.readlines():
    nnn_line = non_stop_words(remove_special_char(new_line))
    #print (nnn_line)
    outputFile.write(nnn_line)
    outputFile.write('\n')

inputFile.close()
outputFile.close()

print ("DONE!")
