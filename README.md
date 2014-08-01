NCBI_ftp
==============

Python code for working with the downloadable NCBI ftp databases.  Currently limited to the taxonomy databases (ftp://ftp.ncbi.nih.gov/pub/taxonomy/).

For gi --> taxID --> taxonomic lineage, files needed are gi_taxid_prot.dmp and taxdump.zip (specifically, nodes.dmp and names.dmp).  
    
User-created files (tab-delimited, one column, one item per line, no header) needed are: an input file of gi numbers and an input file of taxIDs. 
