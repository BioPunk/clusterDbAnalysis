#!/usr/bin/python

# THIS is a dumb genbank parser
# Biopython is too smart and doesn't let me make a fna file with multiple contigs
# if the contig name is longer than 10 characters.
#
# It is mostly intended to be used on the genbank files from RAST - it might not work
# with genbank files from other websites...
#
# Contig IDs cannot have spaces.

import fileinput, optparse, re, sys

usage="%prog -f [genbank_file] > fna file"
description="""Make a contig nucleic acid FASTA file out of a genbank file. Contig names MUST have no spaces.
You should pass to this an organism ID so that the contig names are unique for particular organisms (and so that they match what is in the database)
If no organism ID is passed and it cannot be inferred from the file name we throw an error."""
parser = optparse.OptionParser(usage=usage, description=description)
parser.add_option("-t", "--tab", help="Instead of a FASTA file, print a tab-delimited file with contig in column 1 and sequence in column 2", action="store_true", dest="tab", default=False)
parser.add_option("-o", "--org", help="Organism ID (e.g. 83333.1) (D=Try to read from filename)", action="store", type="str", dest="orgid", default=None)
parser.add_option("-f", "--file", help="genbank file [D: None]", action="store", type="str", dest="genbank", default=None)
(opts, args) = parser.parse_args()

if opts.genbank == None:
    sys.stderr.write("ERROR: Genbank file (-f) must be provided\n")
    exit(2)

orgname = ""
if opts.orgid is None:
    sys.stderr.write("WARNING: No organism ID provided. Attempting to read the organism ID from the filename\n")
    idFinder = re.compile("\d+\.\d+")
    mtch = idFinder.search(opts.genbank)
    if mtch is None:
        sys.stderr.write("WARNING: No IDs in expected format \d+\.\d+ found in file name. You must specify -o to append organism IDs to the contig names\n")
    else:
        orgname = mtch.group(0)
        sys.stderr.write("Found organism ID: %s\n" %(orgname))
else:
    orgname = opts.orgid

spaceRemover = re.compile("\s\s+")
sequenceCleaner = re.compile("[\s\d]*")

contig = ""
seq = ""
issequence = False
for line in open(opts.genbank, "r"):
    if line.startswith("LOCUS"):
        sub = spaceRemover.sub(" ", line)
        spl = sub.split(" ")
        contig = "%s.%s" %(orgname, spl[1])
    # a line ORIGIN designates the beginning of the DNA sequence
    if line.startswith("ORIGIN"):
        issequence = True
        seq = ""
        continue
    # A line "//" designates the end of the DNA sequence...
    if line.startswith("//"):
        if opts.tab:
            print "%s\t%s" %(contig, seq)
        else:
            print ">%s\n%s" %(contig, seq)
        issequence = False
        continue
    if issequence:
        # We need to remove spaces and numbers (location tags)
        seq = seq + sequenceCleaner.sub("", line)