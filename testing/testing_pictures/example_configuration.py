import shutil

document_directories=[]
document_directories.append("~/Documents/cours1")       # in this directory, there are some pictures
document_directories.append("~/Documents/cours2")

not_to_be_done=[]
not_to_be_done.append("MBFDooRFPyNW")       # This is a multiple picture or something that will not work in automatic mode.

shutil.copyfile("~/Documents/cours1/common.py","common.py")     # This file is used by other in "cours1"
