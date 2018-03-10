import csv
import sys

superblock = []
group = []
free_blocks = []
free_inodes = []
inodes = []
directories = []
indirects = []
doubleindirects = []
tripleindirects = []


def populateArrays(filename):
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0] == "SUPERBLOCK":
                superblock.append(row)
            elif row[0] == "GROUP":
                group.append(row)
            elif row[0] == "BFREE":
                free_blocks.append(row)
            elif row[0] == "IFREE":
                free_inodes.append(row)
            elif row[0] == "INODE":
                inodes.append(row)
            elif row[0] == "DIRENT":
                directories.append(row)
            elif row[0] == "INDIRECT" and row[2] == "1":
                indirects.append(row)
            elif row[0] == "INDIRECT" and row[2] == "2":
                doubleindirects.append(row)
            elif row[0] == "INDIRECT" and row[2] == "3":
                tripleindirects.append(row)



if __name__ == "__main__":
    if len(sys.argv)!=2:
         sys.stderr.write('Need to pass file name as an argument\n')
         exit(1)
    filename = sys.argv[1]
    populateArrays(filename)
    print (superblock)
    print(group)
    print(indirects)
    print(doubleindirects)
    print(tripleindirects)
