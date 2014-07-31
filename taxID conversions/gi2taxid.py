# Code to look up a batch of input gi numbers and output their taxIDs in an Excel-friendly format.
# PROGRAM REQUIREMENTS
#       gi_taxid_prot.dmp (gi --> taxid dmp file from NCBI database)
#       an input file 'gi_list.txt' (tab delimited txt) gi# queries, one gi per row, one column
#       name for an output file to be created (also tab delim).  Format will be gi# taxid

# imports necessary gzip file.
import gzip

# opens gi number file and saves 'locally'
gi_set = set(line.strip() for line in open('gi_list.txt', 'r'))

# sets namesfile to open and read ('r') from taxid.gz file
with gzip.open('gi_taxid_prot.dmp.gz', 'r') as taxidfile:
    # sets up an empty list called taxID_matches
    taxid_matches = []
    # sets up counting lines processed
    n = 0
    # Reads string and splits into items (lineparts) in a list based on delimitor '\t'
    for line in taxidfile:
        n = n + 1
        # Breaks each line at delimitors, and strips the '\t|\n' off the end of the line
        linepart = line.strip('\t|\n').split('\t')
        if linepart[0] in gi_set:
            taxid_matches.append(line)
        # prints a line every 1 million lines.
        if n%1000000 == 0:
            print str(n/1000000) + ' million lines'
    write_file = open('taxid_matches.txt','w')
    for line in taxid_matches:
        write_file.write(line)
    write_file.close()
    taxidfile.close()

