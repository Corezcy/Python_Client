import os
import sys


def checkReport(log):
    '''
    打开文件
    在终端显示文件
    '''
    report_path = "./report/"  # 文件保存路径，如果不存在就会被重建
    if not os.path.exists(report_path):  # 如果路径不存在
        os.makedirs(report_path)
    print("*---------        Checking         ----------*")
    path = './report'
    filenum = len([lists for lists in os.listdir(path)
                   if os.path.isfile(os.path.join(path, lists))])

    if filenum == 0:
        print("No report in folder !")
        log.warning("No report in folder !")
        return

    print('filenum :', filenum)
    file_address = []
    i = 1
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        file_address.append(sub_path)
        print(str(i) + ". " + sub_path)
        i += 1
    print()
    report_num = int(input("Please enter report number :"))
    print()

    with open(file_address[report_num - 1], 'r') as f:
        print(f.read())

    pass
