import os
from app.main import main

filename = os.path.join(os.path.dirname(__file__), "docs\\t1.txt")
gift_txt = main(filename)
if len(gift_txt) == 0:
    print("Ooops,failed to convert doc to gift file! Please check the source doc.")
else:
    with open("Output.txt", "w") as text_file:
        text_file.write(gift_txt)
        print("Congratulation! Gift file has been saved in docs direcotry.")