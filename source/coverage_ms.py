import os
import pandas as pd
import MS_api as ms

conn = ms.connect_to_db(r"../date/ms_date.db")

dr_name = r"../date/outmol"

path = dr_name
dr_res = dr_name + "_results/"
gas_dir = "../date/VOC_outmol"
# logs_dr = "./" + dr_res + "Q_logs"
dirs = os.listdir(path)
try:
    os.makedirs(dr_res)
except Exception:
    pass
# base = -4873.1549808
base = -4949.2939523
flag = "Message: DMol3 job finished successfully"
regex = r"^\S*" + flag

minf_list = []
mineg_list = []
Q_sum_list = []
Q_average_list = []
Ead_list = []
de_time_300 = []
de_time_350 = []
de_time_400 = []
gas_eg = {}
system_eg = {}
try:
    for dir in dirs:
        files = os.listdir(path + "/" + dir)
        # print(files)
        min_engery = 0
        for file in files:
            filepath = path + "/" + dir + "/" + file
            date = ms.get_date(file)
            infos = ms.get_infos(file)
            if not os.path.isdir(filepath) and ms.test_outmol(date):
                eg = ms.opt_eg(date)
                if eg < min_engery:
                    try:
                        Q_sum, Q_average = ms.Q_t(date, infos)
                    except Exception:
                        print(file + "没有计算电荷转移!")
                        Q_sum = None
                        Q_average = None
                    min_engery = eg
                    min_f = file
        gas_name = infos[0]
        gas_n = int(infos[2])
        system_eg[file] = [eg, gas_name, gas_n]
        minf_list.append(min_f)
        mineg_list.append(min_engery)
        Q_sum_list.append(Q_sum)
        Q_average_list.append(Q_average)
except Exception:
    for file in dirs:
        filepath = path + "/" + file
        # print(file)
        if not os.path.isdir(filepath):
            date = ms.get_date(filepath)
            infos = ms.get_infos(file)
            # print(date)
            print(infos)
            eg = ms.opt_eg(date)
            # print(eg)
            try:
                Q_sum, Q_average = ms.Q_t(date, infos)
            except Exception:
                print(file + " 没有计算电荷转移!")
                Q_sum = None
                Q_average = None
        gas_name = infos[0]
        gas_n = int(infos[2])
        system_eg[file] = [eg, gas_name, gas_n]
        minf_list.append(file)
        mineg_list.append(eg)
        Q_sum_list.append(Q_sum)
        Q_average_list.append(Q_average)
for each in system_eg:
    # print(gas_eg[system_eg[each][1]])
    # print(system_eg[each][0])
    Ead = ms.E_ad(
        base, system_eg[each][0],
        ms.get_energy_by_name(conn, "Demol3_Gas", system_eg[each][1]),
        system_eg[each][2])
    Ead_ev = ms.H2Ev(Ead)
    Ead_list.append(Ead_ev)
    de_time_300.append(ms.delay_time(Ead_ev, 300))
    de_time_350.append(ms.delay_time(Ead_ev, 350))
    de_time_400.append(ms.delay_time(Ead_ev, 400))
conn.close()

eg_list = [
    minf_list, mineg_list, Ead_list, Q_sum_list, Q_average_list, de_time_300,
    de_time_350, de_time_400
]
# print(eg_list)
eg_list = list(map(list, zip(*eg_list)))
date = pd.DataFrame(eg_list)
date.columns = [
    "system", "E_s", "E_ad", "sum_Q", "ave_Q", "delay_t_300", "delay_t_350",
    "delay_t_400"
]
date.to_excel(dr_res + "/Q_summary.xlsx")

# print(files)
