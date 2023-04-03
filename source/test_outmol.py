import os
import re
import shutil

test_dir = r"C:\Users\Administrator\Desktop\C6N7_archive\outmol_test"

os.chdir(test_dir)
try:
    shutil.rmtree("results")
except Exception:
    pass
try:
    os.mkdir("results")
except Exception:
    pass

print(os.getcwd())
flag = "Message: DMol3 job finished successfully"
regex = r"^\S*" + flag
#
for dir_2 in os.listdir():
    # print(dir_2)
    if not os.path.isdir(dir_2):
        # print(dir_2)
        the_path = "./" + dir_2
        f = open(the_path)
        date = f.read()
        f.close()
        matches = re.findall(regex, date, re.MULTILINE)
        if not matches:
            print(dir_2)
            shutil.copy(the_path, "./results")
