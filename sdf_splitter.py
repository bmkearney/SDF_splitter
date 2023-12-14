import argparse
import os
import unicodedata
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split .sdf file into N entries each.")
    parser.add_argument("sdffile", help="filename you want to split")
    parser.add_argument("-n", dest="N", metavar="N", type=int, default=1, help="the max number of entries in each split file. default=1")
    parser.add_argument("-v", dest="verbose", action="store_true", help="explain what is being done")
    parser.add_argument("-c", dest="common", action="store_true", help="use common name")
    args = parser.parse_args()
    file = args.sdffile
    CN=args.common
    foldername = file.replace(".sdf", '')

    filename, file_extension = os.path.splitext(file)
    if(os.path.exists('./'+foldername) == 0):
        os.makedirs('./'+foldername)
    N = args.N
    
    string = ""
    filename_record=""
    mol_count = 0
    file_count = 0
    filename_flag = 0
    for line in open(file, encoding="cp932", errors="ignore"):
        string += line
        if(filename_flag==1):
            if(CN):
                filename_record=line.strip()
                invalid = ':"/\|?*[] '
                for char in invalid:
                    filename_record = filename_record.replace(char, '')
                filename_record = filename_record.replace("'", "")
                filename_record = filename_record.replace('->', "to-")
                filename_record = filename_record.replace('<', "(")
                filename_record = filename_record.replace('>', ")")
                filename_record = filename_record.replace('', "")
                filename_record = filename_record.replace('±', "+-")
                filename_record = re.sub(r'[^\x00-\x7f]',r'', filename_record)
            filename_flag=0
        if(line.startswith(">  <compound_names>")):#NP Atlas
            filename_flag=1
        if(line.startswith("> <SYSTEMATIC_NAME>")):#ZINC
            filename_flag=1
        if(line.startswith("> <GENERIC_NAME>")):#HMDB
            filename_flag = 1
        if(line.startswith("$$$$")):
            mol_count += 1
            filename_flag = 0
            if(mol_count % N == 0):
                file_count += 1
                if(filename_record==""):
                    output = filename + "_" + str(file_count) + ".sdf"
                else:
                    output = filename_record+".sdf"

                if(os.path.exists("./"+foldername+"/"+output)):
                    output=output[:-4]+"_DUP_"+str(file_count)+".sdf"
                try:
                    file = open("./"+foldername+"/"+output, "w")
                except:
                    file = open("./"+foldername+"/UNKNOWN_"+str(file_count)+".sdf", "w")
                file.write(string)
                file.close()
                if args.verbose:
                    print("output : %s" % output)
                string = ""
                filename_record=""
            
    if(string != ""):
        file_count += 1
        file = open(filename+"_"+str(file_count)+".sdf", "w")
        file.write(string)
        file.close()

    print("%d compounds are divided into %d files." % (mol_count, file_count))
