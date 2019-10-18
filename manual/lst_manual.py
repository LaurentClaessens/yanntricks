from pytex.src import PytexTools

myRequest = PytexTools.Request()

myRequest.original_filename="yanntricks-manual.tex"

myRequest.ok_filenames_list=["e_yanntricks-manual"]
myRequest.ok_filenames_list.extend(["1_preparation"])
myRequest.ok_filenames_list.extend(["0_tests"])
myRequest.ok_filenames_list.extend(["<++>"])


myRequest.new_output_filename="0-yanntricks-manual.pdf"
