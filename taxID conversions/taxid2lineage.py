# Code to look up a batch of input taxids and output their taxonomic lineages in an Excel-friendly format.
#   The bulk of the run time is spent converting the data from names.dmp into a lookup table with lineage information.
#   Once the code has been run, the function MakeLineages('inputname', 'outputname') can be called from the command line.
#   MakeLineages takes an input file consisting only of one taxid per line and converts it into a tab-delimited table of
#       those taxids and their taxonomic groups (when available; leaves an empty space otherwise).
#   The taxorder list below defines which taxonomic groups are tracked, and can be changed with no other alterations to the code.

# PROGRAM REQUIREMENTS
#       nodes.dmp and names.dmp files downloaded from the NCBI taxonomy database.
#       an input file (tab delimited txt) containing the taxIDs to be assigned lineages.  One column, one taxID per row, no header.
#       name for an output file to be created (also tab delim).  Format will be taxID, kingdom --> species

# sets namesfile to open and read ('r') from names.dmp
namesfile = open('names.dmp', 'r')

# sets up an empty dictionary called namesdict
namesdict = {}

# A small list, converted into a dict, that gives the ranking of taxonomic groups
taxorder = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
rank = {}
for n in range(len(taxorder)):
    rank[taxorder[n]] = n

# Given an argument, returns a list of n copies of that argument, where n is the number of taxonomic groups under consideration
def emptylist():
    return [None for n in range(len(rank))]
listoflists = [[] for n in range(len(rank))]

# Reads string and splits into items (lineparts) in a list based on delimitor '\t|\t'
for line in namesfile:
    # Breaks each line at delimitors, and strips the '\t|\n' off the end of the line
    lineparts = line.strip('\t|\n').split('\t|\t')
    # For each scientific name, makes that name the value associated with the taxid key (as an integer value) in namesdict
    # Also puts in an empty list of size 7 to hold lineage information later.
    if lineparts[3] == 'scientific name':
        namesdict[int(lineparts[0])] = [lineparts[1], emptylist(), None]
namesfile.close()


#sets nodesfile to open and read ('r') from nodes.dmp
nodesfile = open('nodes.dmp', 'r')
# A list of seven (currently empty) sublists into which we will sort everything by taxonomic group
taxon = listoflists
# Reads and splits each string into items, just like before
for line in nodesfile:
        lineparts = line.strip('\t|\n').split('\t|\t')
        # Anything in a major taxonomic group gets dropped into the appropriate sublist of groups, along with parent taxid
        # Otherwise the parent taxid goes straight into the original namesdict, replacing the lineage information
        if lineparts[2] in rank:
            taxon[rank[lineparts[2]]].append((int(lineparts[0]), int(lineparts[1])))
            namesdict[int(lineparts[0])][2] = int(lineparts[1])
        else:
            namesdict[int(lineparts[0])][1] = int(lineparts[1])
            namesdict[int(lineparts[0])][2] = lineparts[2]
            
# Modifies the 'root' taxon to act like a kingdom, so the program will know to stop if it follows a lineage to the root
namesdict[1][1] = emptylist()
nodesfile.close()


# Build taxonomic lineage
# Handle the kingdoms (taxon 0) first, because they are the only ones with no parents as far as we're concerned
for item in taxon[0]:
    # For all child,parent pairs in first (0th) item/taxonomic level in taxon, pick out only the first (child) taxID (0th).
    # In namesdict, return the emptylist (2nd piece) belonging to that child taxID; for kingdom, return the first (0th) entry.
    # Define this first (0th) entry as the name of the taxID (first/0th piece returned by searching namesdict for child's taxID)
    # KEY NOTE-- what we are changing is on the LEFT.  We are changing it TO what is on the RIGHT.
    namesdict[item[0]][1][0] = namesdict[item[0]][0]


# For taxa beyond kingdom, build upon previous foundation-- change values for position in taxon list and position in namesdict empty list
# Create a 'while loop' to continue.
n = 1
while len(rank) > n:
    for item in taxon[n]:
        parentID = item[1]
        # If the parent's lineage is just another taxid, that means it's in a category we're not looking at, so we follow it back.
        while type(namesdict[parentID][1]) == int:
            parentID = namesdict[parentID][1]
        # Parent first, then child
        # Parent has already been defined-- can just specificy empty list (second '1st' part of namesdict values)
        #   The [:] is telling PYTHON to make a new copy of the list that can be subsequently modified without changing the original.
        namesdict[item[0]][1] = namesdict[parentID][1][:]
        # Look at nth position in empty list from namesdisct, redefine said position with name of 0th (child) taxID in the nth taxon group
        namesdict[item[0]][1][n] = namesdict[item[0]][0]
    n = n+1
print "dictionaries written"

# The function MakeLineages is called from the terminal after running the program.
#   It takes two strings as arguments: the name of the input file (consisting of one taxid
#   per row and nothing else) and the name of the output file.
def MakeLineages(inputfilename, outputfilename):
    inputfile = open(inputfilename, 'r')
    outputfile = open(outputfilename, 'w')
    # Writes a header line consisting of the label 'TaxID' followed by taxonomic level names
    outputline = 'TaxID\t'+'\t'.join(taxorder)+'\n'
    outputfile.write(outputline)
    for taxid in inputfile:
        # Extracts the taxid as an integer from each line, or throws an error if that's not possible
        try:
            taxid = int(taxid.strip('\n'))
        except:
            print 'The taxid "'+taxid+'" is not in the correct format.'
            quit()
        # Looks up the taxid in the namesdict, then repeatedly looks up parents until it finds a proper lineage
        taxinfo = namesdict[taxid]
        while type(taxinfo[1]) == int:
            taxinfo = namesdict[taxinfo[1]]
        lineage = taxinfo[1][:]
        # For printing purposes, replaces all the 'None' entries with single spaces
        for n in range(len(lineage)):
            if lineage[n] == None:
                lineage[n] = ' '
        # Turns the lineage list into a tab-delimited string and writes it to the output file
        outputline = str(taxid)+'\t'+'\t'.join(lineage)+'\n'
        outputfile.write(outputline)
    print 'done'
    inputfile.close()
    outputfile.close()

  
# 30 Rock Easter egg!
def bar_mitzvah(input):
    if input == 'boys':
        return 'men'
    elif input == 'men':
        return 'wolves'
    else:
        return input+"!!!!!!!!!"

