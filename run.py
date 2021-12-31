import os
import sys
from app.main import main
from pathlib import Path


root = os.path.dirname(__file__)
default_doc_root = os.path.join(root,'docs')

def get_filename():
    fn = []
    if len(sys.argv) == 1:
        for file in os.listdir("docs"):
            if file.endswith(".txt"):
                fn.append(os.path.join(default_doc_root,file))
    else:
        for f in sys.argv[1:]:
            if f.endswith(".txt"):
                fn.append(f)
            else:
                print("the file type error(.txt expected): " + f)
    return fn

fl = get_filename()

for f in fl:
    try:
        gift_txt = main(f)
        if len(gift_txt) == 0:
            print(
                "Ooops,failed to convert doc to gift! Maybe your doc doesn't meet the requirements.For details, please refer to the readme.md.")
        else:
            with open('gift\\' + Path(f).stem + '.gift.txt', "w") as text_file:
                text_file.write(gift_txt)
                print("Congratulation! Gift file has been saved in docs direcotry.")
    except FileNotFoundError:
        print("Wrong file or file path: " + f)
    except Exception:
        print(sys.exc_info()[2])


# filename = os.path.join(os.path.dirname(__file__), "docs\\ldz-wlhl20211231.txt")
#
# print(filename)
# gift_txt = main(filename)
# if len(gift_txt) == 0:
#     print("Ooops,failed to convert doc to gift! Maybe your doc doesn't meet the requirements.For details, please refer to the readme.md.")
# else:
#     with open("docs\\Output.txt", "w") as text_file:
#         text_file.write(gift_txt)
#         print("Congratulation! Gift file has been saved in docs direcotry.")