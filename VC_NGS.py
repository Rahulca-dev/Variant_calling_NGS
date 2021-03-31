import gzip, sys, os, fileinput, argparse, subprocess, glob, pysam, re
import time

tic = time.perf_counter()



def validation(fastq_file):
	print (fastq_file)
	fastq = fastq_file.split(".")
	print("-"*95 + "Validation Protocol" + "-"*95)


	with open(fastq_file, "r") as f:
		read = f.readlines()
		count = 1;
		for line in read:
			if line == re.match("^@",line):
				count +=1;
			if count == 2:
				line = re.match("/(w+)/")
				count +=1;
			if count ==3:
				line = re.match("/+/")
				count +=1;
			if count ==4:
				line = re.match("/(w+)/")
		print("File validated")
	print("-"*95 + "File Validated" + "-"*95)

	pass

def FastQC_S(fastq_file, output_dir, options=['--extract',]):
    """
    Run the fastqc program on a specified fastq file and return the output directory path.

    Parameters
    ----------
    fastq_path : str
        Path to the fastq file to analyze.
    output_dir : str
        Directory where output will be written. It will be created if it does not exist.
    options : list of str (optional)
        Command-line flags and options to fastqc. Default is --extract.

    Returns
    -------
    output_dir : str
        The path to the directory containing the detailed output for this fastq file.
        It will be a subdirectory of the specified output dir.
    """
    os.mkdir(output_dir)

    command = "fastqc {} -o {} {}".format(' '.join(options), output_dir, fastq_file)

    subprocess.check_call(command, shell=True)

    # Fastqc creates a directory derived from the basename
    fastq_dir = os.path.basename(fastq_file)
    if fastq_dir.endswith(".gz"):
        fastq_dir = fastq_dir[0:-3]
    if fastq_dir.endswith(".fq"):
        fastq_dir = fastq_dir[0:-3]
    if fastq_dir.endswith(".fastq"):
        fastq_dir = fastq_dir[0:-6]
    fastq_dir = fastq_dir + "_fastqc"

    # Delete the zip file and keep the uncompressed directory
    zip_file = os.path.join(output_dir, fastq_dir + ".zip")
    os.remove(zip_file)

    output_dir = os.path.join(output_dir, fastq_dir)
    return output_dir


def FastQC_P(fastq_file):
	print("Fastqc_paired_end")
	pass



path = os.getcwd();
parser = argparse.ArgumentParser(description='VC_NGS Pipeline for variant analysis.')
parser.add_argument('-f','--fastq', help='Input file name',required=True)
parser.add_argument('-ref','--refgenome',help='Output file name', required=True)
parser.add_argument('-read','--Read', type = int, required=True)
parser.add_argument('-o','--output',help='Output file name', required=True)

args = parser.parse_args()
fastq_file = args.fastq
ref_file = args.refgenome
File_type = args.Read
out = args.output
print(File_type)


if File_type == 1:
	validation(fastq_file)
	FastQC_S(fastq_file,out)


elif File_type == 2:
	validation(fastq_file)
	FastQC_P(fastq_file,out)

else:
	print("Invalid File_type")
