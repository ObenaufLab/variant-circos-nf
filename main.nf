#!/usr/bin/env nextflow

/*
* MIT License
*
* Copyright (c) 2017 Tobias Neumann
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*/

def helpMessage() {
    log.info"""
    ================================================================
     guidemapper-nf
    ================================================================
    DESCRIPTION
    Usage:
    nextflow run obenauflab/variant-circos-nf
    Options:
        -params-file        YAML-file with the following entries:
        
                            genome: hg38/mm10
                            cnvFile: vcf file with copy-number variations
                            snvFile: vcf file with single-nucleotide variations
                            translocationFile: vcf file with translocations
                            circosName: Name of the circos directory folder

    Profiles:
        standard            local execution
        singularity         local execution with singularity
        ii2                 SLURM execution with singularity on IMPIMBA2
        
    Docker:
    obenauflab/variant-circos-nf:latest
    
    Author:
    Tobias Neumann (tobias.neumann@imp.ac.at)
    """.stripIndent()
}

process circos {

	echo true
	
	//baseName = workflow.scriptFile.getParent()
	
	tag { name }	
	
	output:
    file("${params.circosName}") into publishChannel
 
    script:
    """
    mkdir -p ${params.circosName}
    cp -r ${workflow.scriptFile.getParent() + "/circos"}/* ${params.circosName}
    
    VCFtoCircosCNVConverter.py -v ${params.cnvFile} > ${params.circosName}/data/cnv.txt
    
    bedtools makewindows -g ${workflow.scriptFile.getParent()}/data/hg38.chrom.sizes -w 1000000 > ${params.circosName}/data/hg38windows.bed
	bedtools coverage -a ${params.circosName}/data/hg38windows.bed -b ${params.snvFile} -counts | sed -e 's/chr/hs/g' > ${params.circosName}/data/snv.txt
	
	VCFtoCircosTranslocationConverter.py -v ${params.translocationFile} > ${params.circosName}/data/translocations.txt
	
	sed -i 's/GENOME/karyotype.human.hg38.txt/g' ${params.circosName}/etc/circos.conf
	
	(cd  ${params.circosName} ; circos)

    """
}

