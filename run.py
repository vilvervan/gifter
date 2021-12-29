import os
from app.main import main

fn = os.path.join(os.path.dirname(__file__), "docs\\t1.txt")
main(fn)
