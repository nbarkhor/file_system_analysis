import csv
import sys

superblock = []
numBlocks=0
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
            global numBlocks, superblock, group, free_blocks, free_inodes, inodes, directories, indirects, doubleindirects, tripleindirects
            if row[0] == "SUPERBLOCK":
                superblock.append(row)
                numBlocks=int(superblock[0][1])
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

def findInvalidBlocks():
    first_unreserved_block = int(group[0][8]) + int((int(superblock[0][2])*int(superblock[0][4])/int(superblock[0][3]))) #int(superblock[0][6]) + 4 #superblock+group+block bitmap + inode bitmap +inodes
    for inode in inodes:
        for x in range (12,24):
            if int(inode[x])<0 or int(inode[x])>numBlocks:
                print ("INVALID BLOCK {0} IN INODE {1} AT OFFSET {2}".format(inode[x],inode[1],x-12))
            elif int(inode[x])>0 and int(inode[x])<first_unreserved_block:
                print ("RESERVED BLOCK {0} IN INODE {1} AT OFFSET {2}".format(inode[x],inode[1],x-12))
        if int(inode[24])<0 or int(inode[24])>numBlocks:
            print ("INVALID INDIRECT BLOCK {0} IN INODE {1} AT OFFSET 12".format(inode[24],inode[1]))
        elif int(inode[24])>0 and int(inode[24])<first_unreserved_block:
            print ("RESERVED INDIRECT BLOCK {0} IN INODE {1} AT OFFSET 12".format(inode[24],inode[1]))
        if int(inode[25])<0 or int(inode[25])>numBlocks:
            print ("INVALID DOUBLE INDIRECT BLOCK {0} IN INODE {1} AT OFFSET 268".format(inode[25],inode[1]))
        elif int(inode[25])>0 and int(inode[25])<first_unreserved_block:
            print ("RESERVED DOUBLE INDIRECT BLOCK {0} IN INODE {1} AT OFFSET 268".format(inode[25],inode[1]))
        if int(inode[26])<0 or int(inode[26])>numBlocks:
            print ("INVALID TRIPLE INDIRECT BLOCK {0} IN INODE {1} AT OFFSET 65804".format(inode[26],inode[1]))
        elif int(inode[26])>0 and int(inode[26])<first_unreserved_block:
            print ("RESERVED TRIPLE INDIRECT BLOCK {0} IN INODE {1} AT OFFSET 65804".format(inode[26],inode[1]))


if __name__ == "__main__":
    if len(sys.argv)!=2:
         sys.stderr.write('Need to pass file name as an argument\n')
         exit(1)
    filename = sys.argv[1]
    populateArrays(filename)
    findInvalidBlocks()
