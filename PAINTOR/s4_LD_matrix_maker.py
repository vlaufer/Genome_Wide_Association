# This script is a modified version of the script housed at: https://github.com/gkichaev/PAINTOR_V3.0/tree/master/PAINTOR_Utilities
# The modifications are:
# 1) The function Match_Ref_Panel_Alleles() appeared twice, so it is removed in this version
# 2) The lines relating to AT and GC SNPs in the Read_Locus() function are removed. 
#    Instead, extra functionality has been added to Match_Ref_Panel_Alleles() to accommodate these.
# 3) Added additional comments
# 4) Minor formatting issues

## Additional note 1: read this script along with CheckLD.py. Might be able to merge them or remove some redundant steps?
## Additional note 2: Would be good to get this to run on each file in the folder, but probably easier to just write a wrapper script 

## Import Modules
import sys
import os
import numpy as np
import gzip
from optparse import OptionParser
from subprocess import Popen, PIPE

def Read_Locus(file_name, effect_allele, alt_allele, position, chromosome_field):
    """Read fine mapping file and return a matrix with [positions, effect allele, alternate allele]"""
    file_stream = open(file_name, 'r')
    header = file_stream.readline().strip().split()
    try:
        chrom_index = header.index(chromosome_field)
        effect_index = header.index(effect_allele)
        alt_index = header.index(alt_allele)
        pos_index = header.index(position)
    except(ValueError):
        print("Error: Header is mis-specified. Please check and try-again.")
    all_positions = []
    all_chromo=[]
    all_data = []
    all_data.append(header)
    counter = 0
    for lines in file_stream:
        counter += 1
        temp = lines.strip().split()
        #drop ambiguous snps from input data and warn!
        A1_allele = temp[effect_index].upper()
        A0_allele = temp[alt_index].upper()
# AT GC removal commented out
#        if (A1_allele == "A" and A0_allele == "T") or (A1_allele == "T" and A0_allele == "A") or \
#         (A1_allele == "G" and A0_allele == "C") or (A1_allele == "C" and A0_allele == "G"):
#            print("Warning! Ambiguous SNP (AT or GC) in input locus. Dropping row " + str(counter) + " from data:")
#            print(temp)
#        else:
#            all_positions.append(int(temp[pos_index]))
#            all_data.append(temp)
        all_positions.append(int(temp[pos_index]))
        all_data.append(temp)
        all_chromo.append(int(temp[chrom_index]))
    file_stream.close()
    return [all_positions, all_data, all_chromo]

def Read_Locus(file_name, effect_allele, alt_allele, position, chromosome):
    """Read fine mapping file and return a matrix with [positions, effect allele, alternate allele]"""
    file_stream = open(file_name, 'r')
    header = file_stream.readline().strip().split()
    try:
        chrom_index = header.index(chromosome)
        effect_index = header.index(effect_allele)
        alt_index = header.index(alt_allele)
        pos_index = header.index(position)
    except(ValueError):
        print("Error: Header is mis-specified. Please check and try-again.")
    all_positions = []
    all_chromo = []
    all_data = []
    all_data.append(header)
    counter = 0
    for lines in file_stream:
        counter += 1
        temp = lines.strip().split()
        #drop ambiguous snps from input data and warn!
        A1_allele = temp[effect_index].upper()
        A0_allele = temp[alt_index].upper()
# AT GC removal commented out
#        if (A1_allele == "A" and A0_allele == "T") or (A1_allele == "T" and A0_allele == "A") or \
#         (A1_allele == "G" and A0_allele == "C") or (A1_allele == "C" and A0_allele == "G"):
#            print("Warning! Ambiguous SNP (AT or GC) in input locus. Dropping row " + str(counter) + " from data:")
#            print(temp)
#        else:
#            all_positions.append(int(temp[pos_index]))
#            all_data.append(temp)
        all_positions.append(int(temp[pos_index]))
        all_chromo.append(int(temp[chrom_index][3:]))
        all_data.append(temp)
    file_stream.close()
    return [all_positions, all_data, all_chromo]



def Extract_Pop_Ids(file_name, population):
    """Get population ids from mapping file"""
    file_stream = open(file_name, 'r')
    header = file_stream.readline().strip().split()
    all_ids = []
    for lines in file_stream:
        temp = lines.strip().split()
        if (temp[2] == population):
            all_ids.append(temp[0])
    file_stream.close()
    return all_ids


def Filter_VCF_rows(file_name, pos, chromo):
        """Extract all the rows in the VCF file that have matching positions in the locus file + header using Tabix"""
        out_rows = []
        chromosome=min(chromo)
        min_position=min(pos)
        max_position=max(pos)
        file_stream=gzip.open(file_name, 'r')
        for header_lines in file_stream:
                if(header_lines[0:6] == b"#CHROM"):
                        out_rows.append(header_lines.strip().split())
                        break
        file_stream.close()

        pos_set = set()
        [pos_set.add(int(i)) for i in pos]
        pos_present = dict((i, False) for i in pos)
        query = '{}:{}-{}'.format(chromosome, min_position, max_position)
        process = Popen(['tabix', '-f', file_name, query], stdout=PIPE)
        for line in process.stdout:
                line_split = line.strip().split()
                curr_pos = int(line_split[1])
                if(curr_pos in pos_set):
                        out_rows.append(line_split)
                        pos_present[curr_pos] = True
        return [out_rows, pos_present]

def Extract_Pop_Haps(vcf_rows, pop_ids):

    """Extract (continental) population haplotypes and return a numpy matrix with haplotypes"""
    header = vcf_rows[0]
    header_str = [item.decode("utf-8") for item in header]
    extract_index = [header_str.index(ids) for ids in pop_ids]
    pop_haps =[]
    for rows in vcf_rows[1::]:
        hap_list = [rows[i].decode("utf-8").split("|") for i in extract_index]
        hap = [int(item) for sublist in hap_list for item in sublist]
        pop_haps.append(hap)
    return np.matrix(pop_haps)


def Match_Ref_Panel_Alleles(vcf_rows, input_data, pos_header, effect_header, alt_header, Z_header):

    """Determine if reference panel alleles match input data alleles.
        If alleles in data do not match what was extracted from ref panel output the reference panel row is deleted"""
    header_vcf = vcf_rows[0]
    A1_index = header_vcf.index(b"ALT")
    A0_index = header_vcf.index(b"REF")
    pos_index_vcf = header_vcf.index(b"POS")
    out_vcf = []
    out_vcf.append(header_vcf)

    final_locus = []
    header_input = input_data[0]
    final_locus.append(header_input)

    pos_index = header_input.index(pos_header)
    effect_index = header_input.index(effect_header)
    alt_index = header_input.index(alt_header)
    z_index = header_input.index(Z_header)
    position = [int(pos[pos_index]) for pos in input_data[1::]]
    effect_allele = [effect[effect_index] for effect in input_data[1::]]
    alt_allele = [alt[alt_index] for alt in input_data[1::]]

    for rows in vcf_rows[1::]:
        vcf_pos = int(rows[pos_index_vcf])
        vcf_A1 = rows[A1_index].decode("utf-8")
        vcf_A0 = rows[A0_index].decode("utf-8")
        curr_snp = position.index(vcf_pos)
        data_A1 = effect_allele[curr_snp].upper()
        data_A0 = alt_allele[curr_snp].upper()
        # check if reference panel matches input data. drop SNPs that do not have the same alleles in ref panel.
        if vcf_A1 == data_A1 and vcf_A0 == data_A0:
            out_vcf.append(rows)
            final_locus.append(input_data[curr_snp+1])
        # This may need to be more nuanced for AT / GC SNPs
        elif vcf_A1 == data_A0 and vcf_A0 == data_A1:
            out_vcf.append(rows)
            flip_line = input_data[curr_snp+1]
            zflip = -1*float(flip_line[z_index])
            flip_line[z_index] = str(zflip)
            final_locus.append(flip_line)
        else:
            print("Warning! Found alleles " + str(vcf_A1) + " and " + str(vcf_A0) + " in refernce panel\n")
            print("Expecting alleles " + str(effect_allele[curr_snp]) + " and " + str(alt_allele[curr_snp]) + "\n")
    return [out_vcf, final_locus]


def Write_Output(outname, final_data, computed_ld, drop_mono):
    locus_name = outname + ".processed"
    locus_out = open(locus_name, 'w')
    ld_name = outname + ".ld"
    if(drop_mono == True):
        poly_index = [i for i in range(len(computed_ld)) if np.isnan(computed_ld[i,i]) != True]
        ld_filt = computed_ld[poly_index].T[poly_index]
        np.savetxt(ld_name,ld_filt, fmt='%1.4e')
        locus_out.write(" ".join(final_data[0]) + "\n")
        for i in poly_index:
            locus_out.write(" ".join(final_data[i+1])+"\n")
    else:
        np.savetxt(ld_name, computed_ld, fmt='%1.4e')
        for lines in final_data:
            locus_out.write(" ".join(lines)+"\n")
    locus_out.close()

def Filter_Missing_SNPs_ref(input_data, present_snps, pos_header):
    filtered_data = []
    header = input_data[0]
    pos_index = header.index(pos_header)
    filtered_data.append(header)
    for snps in input_data[1::]:
        snps[1]=snps[1]
        snp_position = int(snps[pos_index])
        if(present_snps[snp_position]):
            filtered_data.append(snps)
        else:
            print("Warning! SNP not found in reference panel :")
            print(" ".join(snps) + "\n")

    return filtered_data

def main():

    ##defaults
    drop_mono=False
    ##
    parser = OptionParser()
    parser.add_option("-l", "--locus", dest="locus")
    parser.add_option("-r", "--reference", dest="reference")
    parser.add_option("-c", "--chrom_head", dest="chrom_head")
    parser.add_option("-e", "--effect_allele", dest="effect_allele")
    parser.add_option("-a", "--alt_allele", dest="alt_allele")
    parser.add_option("-p", "--population", dest="population")
    parser.add_option("-o", "--out_name", dest="out_name")
    parser.add_option("-i", "--position", dest="position")
    parser.add_option("-m", "--map_file", dest="map_file")
    parser.add_option("-z", "--Zhead", dest="Zhead")
    parser.add_option("-d", "--drop_mono", dest="drop_mono")

    (options, args) = parser.parse_args()

    locus_name = options.locus
    reference =  options.reference
    chrom_head = options.chrom_head
    effect_allele = options.effect_allele
    alt_allele = options.alt_allele
    population = options.population
    out_name = options.out_name
    position = options.position
    map_file = options.map_file
    Zhead = options.Zhead
    drop_mono = options.drop_mono

    if os.path.isfile(out_name + ".processed") is True:
        print("output file already exists; exiting")
        exit()
    else:
        print(out_name + ".processed does not exist yet, creating")
    usage = \
    """ Need the following flags specified (*)
        Usage:
        --locus [-l] specify input file with fine-mapping locus (assumed to be ordered by position) *
        --reference [-r]  specify reference VCF file corresponding to chromosome of locus *
        --map_file [-m] specify reference map file that maps population ids to individuals *
        --position [-i] specify the name of the field in header corresponding to the SNP positions *
        --effect_allele [-e] specify the name of the field in header corresponding to effect allele (i.e the allele encoded as 1) *
        --alt_allele [-a] specify the name of the field in header corresponding to alternate allele (i.e the allele encoded as 0) *
        --population [-p] specify name of continental population {AFR, AMR, EAS, EUR, SAS} to compute LD with *
        --out_name [-o] specify the stem of the output files *
        --Zhead [-z] specify the name of Zscore field in header *
        """

    if(locus_name == None or reference == None or effect_allele == None or alt_allele == None or population == None or out_name == None or position == None):
        sys.exit(usage)
	
    drop_mono=False
    [all_positions, all_data, chromo_i] = Read_Locus(locus_name,effect_allele,alt_allele,position, chrom_head)
    [vcf_rows, found_positions] = Filter_VCF_rows(reference,all_positions,chromo_i)
    pop_ids = Extract_Pop_Ids(map_file,population)
    filtered_data = Filter_Missing_SNPs_ref(all_data, found_positions, position)
    [final_reference, flipped_data] = Match_Ref_Panel_Alleles(vcf_rows, filtered_data, position, effect_allele, alt_allele, Zhead)
    pop_haps = Extract_Pop_Haps(final_reference, pop_ids)
    ld_mat = np.corrcoef(pop_haps)
    Write_Output(out_name, flipped_data, ld_mat, drop_mono)


if __name__ == "__main__": main()
