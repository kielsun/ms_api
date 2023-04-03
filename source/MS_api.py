import re
import name_file as fn
import math
import sqlite3


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def get_energy_by_name(conn, table_name, name):
    cursor = conn.cursor()
    cursor.execute("SELECT Energy FROM {} WHERE Gas_name=?".format(table_name),
                   (name, ))
    rows = cursor.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return None


def get_date(filepath):
    f = open(filepath)
    date = f.read()
    f.close()
    return date


def get_infos(file):
    infos = fn.file_name(file)
    return infos


def test_outmol(date):
    flag = "Message: DMol3 job finished successfully"
    regex = r"^\S*" + flag
    matches = re.findall(regex, date, re.MULTILINE)
    if not matches:
        return False


def opt_eg(date):
    sentence = re.findall("opt== .*", date, re.M)
    n = len(sentence)
    # n_k = 3 * k - 3
    res = float(str(sentence[n - 1]).split()[2])
    return res


def Q_t(date, infos):
    str1 = "Charge partitioning by Hirshfeld method:"
    str2 = "Message: License checkin of MS_dmol successful"
    regex = r"^\s*([A-Z])\s*\d+.*?([-\d]+\.\d+)\s*([-\d]+\.\d+)"
    Q_nums = 0
    test_str = str(date.split(str1)[1].split(str2)[0].split(")")[1])
    matches = re.findall(regex, test_str, re.MULTILINE)
    # print(matches)
    nums = infos[-1]
    # print(nums)
    mos = infos[2]
    # print(mos)
    for temp in matches[-nums:]:
        # print(temp)
        Q_nums = Q_nums + float(temp[1])
        # print(num)
    return Q_nums, Q_nums / mos


def H2Ev(ha: float):
    return ha * 27.2114


def E_ad(base: float, system: float, gas: float, n=1) -> float:
    return (system - base - (n * gas)) / n


def delay_time(E_ad: float, T: float) -> float:
    v0 = 10**(-12)
    kT = 0.025852 * T / 300
    # print(E_ad)
    delay_t = v0 * math.exp(-E_ad / kT)
    return delay_t


# f = open("outmol_date/H2S_2.outmol")
# date = f.read()
# sentence = re.findall("opt== .*", date, re.M)
# n = len(sentence)
# # n_k = 3 * k - 3
# fw = open("test.out", "w")
# res = sentence[n - 1]
# res2 = str(res).split()[2]
# fw.write(str(sentence))
# print(res2)
