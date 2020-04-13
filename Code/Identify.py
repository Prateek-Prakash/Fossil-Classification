#This method checks if more than 50% of a string is capital letters.
def is_almost_capital(Line):
    no_of_capital = 0.0
    if len(Line) < 1:
        return 0
    for ch in Line:
        if 'A' <= ch <= 'Z':
            no_of_capital = no_of_capital + 1

    return (100 * (no_of_capital / len(Line))) > 50



# This method checks if the word starts with either ? or capital letter to find species.
def is_begining(word):
    return word.startswith('?') or  'A' <= word[0]<='Z'


# This method ispart of species identification where it checks the year and it tries to handle noisy years.
def is_year(word):
    no_count = 0.0
    for ch in word[0:4]:
        if '0' <= ch <='9':
            no_count = no_count + 1
    return (100 * (no_count/4) >= 50)


# This method returns true when the line is species. It calls the previous three methods.
def is_species(line):
    line.replace('\t', ' ')
    splitted_line = line.split(' ')
    # Add delimiters to move the species to appropriate column in excel
    species = "\n## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##"
    
    if len(splitted_line) < 3:
        return False
    if (is_begining(splitted_line[0])):
        word_idx = 1
        while (word_idx < len(splitted_line) and (not is_year(splitted_line[word_idx])) and word_idx < 5):
            word_idx = word_idx + 1
    
        if (word_idx < len(splitted_line) and is_year(splitted_line[word_idx])):
            temp_line =""
            for i1 in range (1, word_idx):
                temp_line = temp_line.strip() + splitted_line[i1]

            for i2 in range (0, word_idx+1):
                species = species + splitted_line[i2] + " "
           
            # copy the remaining string as description
            description = "##"
            if (word_idx < len(splitted_line)):
                for i3 in range (word_idx + 1, len(splitted_line)):
                    description = description + splitted_line[i3] + " "

            if is_almost_capital(temp_line) and temp_line[-1] == ',':
                # The following line shows species name.
                print (splitted_line[0:word_idx+1])
                print (species)
                outpuFile.write(species)
                outpuFile.write(description.replace("\n", ""))
                return True

    # if the line does not start with keyword consider it as description
    else:
        if (not is_line_species(line)):
            description = line
            description = description.replace("\n", " ")
            outpuFile.write(description)
            return True
        else:
            return False

    return False

# This method returns True if the line starts with classification keyword
def is_line_class(line):
    if line.startswith('superclass') or line.startswith('class')  or line.startswith('subclass') or line.startswith('order') or line.startswith('suborder') or line.startswith('superfamily') or line.startswith('family') or line.startswith('subfamily'):
        return True
    
    return False

# This method returns True if the line starts with classification keyword
def is_line_species(line):
    line.replace('\t', ' ')
    splitted_line = line.split(' ')
    
    if len(splitted_line) < 3:
        return False
    if (is_begining(splitted_line[0])):
        word_idx = 1
        while (word_idx < len(splitted_line) and (not is_year(splitted_line[word_idx])) and word_idx < 5):
            word_idx = word_idx + 1
    
        if (word_idx < len(splitted_line) and is_year(splitted_line[word_idx])):
            return True
    
    return False

# This method returns True if the line is a classification
def is_class(line):
    aline = line
    aline = aline.strip().lower()
    if is_line_class(aline):
        line.replace('\t', ' ')
        splitted_line = line.split(' ')
        nwords = len(splitted_line)
        clsline = ""
        description = "##"

		# Add delimiters to move data to appropriate column in excel
        if aline.startswith('class'):
            clsline = "\n## ##"
        elif aline.startswith('subclass'):
            clsline = "\n## ## ## ##"
        elif aline.startswith('order'):
            clsline = "\n## ## ## ## ## ##"
        elif aline.startswith('suborder'):
            clsline = "\n## ## ## ## ## ## ## ##"
        elif aline.startswith('superfamily'):
            clsline = "\n## ## ## ## ## ## ## ## ## ##"
        elif aline.startswith('family'):
            clsline = "\n## ## ## ## ## ## ## ## ## ## ## ##"
        elif aline.startswith('subfamily'):
            clsline = "\n## ## ## ## ## ## ## ## ## ## ## ## ## ##"
            
        if len(splitted_line) < 3:
            return False
        if (is_begining(splitted_line[0])):
            word_idx = 1
            while (word_idx < len(splitted_line) and (not is_year(splitted_line[word_idx])) and word_idx < 8):
                word_idx = word_idx + 1
            
            #if (word_idx < len(splitted_line) and is_year(splitted_line[word_idx])):
            if (word_idx < len(splitted_line)):
                for i2 in range (0, word_idx + 1):
                    clsline = clsline + splitted_line[i2] + " "
                     
            # copy the remaining string as description
            if (word_idx < len(splitted_line)):
                for i3 in range (word_idx + 1, len(splitted_line)):
                    description = description + splitted_line[i3] + " "

            # The following line shows species name.
            print (splitted_line[0:word_idx+1])
            print (clsline)
            outpuFile.write(clsline)
            description = description.replace("\n", "")
            outpuFile.write(description)
            return True

    # if the line does not start with keyword consider it as description
    else:
        # If this is not a species line then it must be description
        if (not is_line_species(line) and (not is_line_class(line))):
            description = line
            description = description.replace("\n", " ")
            outpuFile.write(description)
            return True
        else:
            return False

    return False
    
#Your input file with full path.
inputFile = open(r'D:\Temp\Data Mining\Try 2 - Generates Csv with Description\cv1_394-510\1.txt', 'r')
#Your output file with full path.
outpuFile = open(r'D:\Temp\Data Mining\Try 2 - Generates Csv with Description\cv1_394-510\Csv_394-510.txt', 'w')

#Iterate over every individual line and check what is it exactly. You may want to add more taxas as needed, depends on your dataset.
outpuFile.write( "SUPERCLASS##DESCRIPTION##CLASS##DESCRIPTION##SUBCLASS##DESCRIPTION##ORDER##DESCRIPTION##SUBORDER##DESCRIPTION##SUPERFAMILY##DESCRIPTION##FAMILY##DESCRIPTION##SUBFAMILY##DESCRIPTION##SPECIES##DESCRIPTION\n")
for line in inputFile.readlines():
    aline = line
    line = line.strip().lower()
    if is_class(aline):
        print ('Class: ' + aline)
    elif is_species(aline):
        print ('Species: ' + aline)

#close the output file.
outpuFile.close()
