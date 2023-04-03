import os
import re
import shutil

path = r"C:\Users\Administrator\Desktop\C6N7_archive\GeomOpt"
os.chdir(path)
print(os.getcwd())
try:
    os.mkdir("../outmol_test")
except Exception:
    pass
regex = r"^\S*\.outmol"
dir_1 = os.listdir(path)
for dir_2 in dir_1:
    # print(dir_2)
    if os.path.isdir(dir_2):
        dir_3 = os.listdir(dir_2)
        # print(dir_3)
        for dir_4 in dir_3:
            matches = re.findall(regex, dir_4, re.MULTILINE)
            if matches:
                print(matches[0])
                the_path = r"./" + dir_2 + "/" + matches[0]
                print(the_path)
                shutil.copy(the_path, "../outmol_test")
