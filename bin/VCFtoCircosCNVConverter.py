#!/usr/bin/env python

# Date located in: -
from __future__ import print_function
import sys, os, re

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

def parseCNVs(line):
    for line in f:
        if line[0] != "#":
            fields = line.rstrip().split("\t")
            chr = fields[0]
            start = fields[1]
            infoFields = fields[7].split(";")
            end = ""
            fc = ""
            for item in infoFields:
                if re.search('^END=', item):
                    end = item.split("=")[1]
                if re.search('^FOLD_CHANGE_LOG=', item):
                    fc = item.split("=")[1]
                  
            print(re.sub("chr", "hs", chr) + "\t" + start + "\t" + end + "\t" + fc)

usage = "Convert CNV calls in VCF format to circos format"
parser = ArgumentParser(description=usage, formatter_class=RawDescriptionHelpFormatter)
parser.add_argument("-v", "--vcf", type=str, required=True, dest="vcfFile", help="CNV VCF file" )

args = parser.parse_args()

if file_type(args.vcfFile) == "gz":
    with gzip.open(args.vcfFile,'r') as f:
        for line in f:
            parseCNVs(line)
            
else :
    with open(args.vcfFile) as f:
        for line in f:
            parseCNVs(line)