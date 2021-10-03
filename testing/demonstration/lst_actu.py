from pytex.src import PytexTools

myRequest = PytexTools.Request("mesure")
myRequest.original_filename = "demo.tex"
myRequest.ok_filenames_list = ["e_pictures"]
myRequest.ok_filenames_list.extend(["1_demo"])
myRequest.new_output_filename="0-actu.pdf"
