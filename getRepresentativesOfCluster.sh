#!/bin/bash

# Use the representative sequences script from MYRAST to
# obtain representative sequences for a specified cluster / run ID pair

if [ $# -ne 2 ]; then
    echo "Usage: getRepresentativesOfCluster.sh [run ID] [cluster ID]"
    exit 0;
fi

# 1: Make into tab-delimited format needed for other functions
# 2: Get protein sequences
# 3: Get representative sequences using default parameters
echo $1 | ./src/clusterIdToTable.py $2 | ./src/db_getClusterGeneInformation.py \
    | ./src/annoteSeq2Fasta.py -g 3 -a 5 -s 6 > /tmp/fasta_$1_$2

# Get representatives
# We are using a similarity higher than default becuase our organisms are all so similar.
# 
cat /tmp/fasta_$1_$2 | svr_representative_sequences -b -s 0.98 > $1_$2_reps.faa

# Thou shalt clean up after thy self
rm /tmp/fasta_$1_$2