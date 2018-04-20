#!/usr/bin/env python

# Date located in: -
from __future__ import print_function
import sys, os, re, gzip

from argparse import ArgumentParser, RawDescriptionHelpFormatter

magic_dict = {
    "\x1f\x8b\x08": "gz",
    "\x42\x5a\x68": "bz2",
    "\x50\x4b\x03\x04": "zip"
    }

max_len = max(len(x) for x in magic_dict)

def file_type(filename):
    with open(filename) as f:
        file_start = f.read(max_len)
    for magic, filetype in magic_dict.items():
        if file_start.startswith(magic):
            return filetype
    return "no match"

def parseTranslocations(line):
    if line[0] != "#":
        fields = line.rstrip().split("\t")
        
        infoFields = fields[7].split(";")
        
        isTranslocation = False
        for item in infoFields:
            if re.search('^SVTYPE=', item):
                if item.split("=")[1] == "BND":
                    isTranslocation = True
                continue
                
        if not isTranslocation:
            return
            
        chr = fields[0]
        chr = re.sub("chr","hs",chr)
        bait = fields[1]
        prey = fields[4]
        prey = re.sub("\s.*","",re.sub("^[\S]*\s","",re.sub("[\[\]]"," ",prey)))
        preyChr, preyPos = prey.split(":")
        preyChr = re.sub("chr","hs",preyChr)
        preyChr = re.sub("CHR","hs",preyChr)
        
        print(chr + "\t" + bait + "\t" + bait + "\t" + preyChr + "\t" + preyPos + "\t" + preyPos)

usage = "Convert translocation calls in VCF format to circos format"
parser = ArgumentParser(description=usage, formatter_class=RawDescriptionHelpFormatter)
parser.add_argument("-v", "--vcf", type=str, required=True, dest="vcfFile", help="CNV VCF file" )

args = parser.parse_args()

if file_type(args.vcfFile) == "gz":
    with gzip.open(args.vcfFile,'r') as f:
        for line in f:
            parseTranslocations(line)
            

else :
    with open(args.vcfFile,'r') as f:
        for line in f:
            parseTranslocations(line)