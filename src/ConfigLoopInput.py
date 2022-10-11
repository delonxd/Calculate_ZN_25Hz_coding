import pandas as pd
import itertools


# 25Hz电码化混合
def init_input_ZN_25Hz_coding_mix_test():
    ret = {
        '备注': ['无'],
        '线路名称': ['无'],
        '车站名称': ['无'],

        '主串区段': ['I'],
        '被串区段': ['II'],

        '主串区段长度(m)': [500, 600],
        '被串区段长度(m)': [500, 600],

        '主串坐标': [0],
        '被串坐标': [0],
        '并行长度(m)': [None],

        '线间距': [None],
        '耦合系数': [24, 10],

        '主串频率(Hz)': [1700, 2000, 2300, 2600],
        # '主串频率(Hz)': [2300],
        '被串频率(Hz)': [1700, 2000, 2300, 2600],

        '主串电容数(含TB)': [5, 6, 7],
        '被串电容数(含TB)': [5, 6, 7],

        '主串电容值(μF)': [25, 40, 46, 55, 60, 80],
        '被串电容值(μF)': [25, 40],

        '主串道床电阻(Ω·km)': [10000, 2],
        '被串道床电阻(Ω·km)': [10000, 2],

        '主串方向': ['右发'],
        '被串方向': ['右发'],

        '主串电缆长度(km)': [10, 12.5],
        '被串电缆长度(km)': [10, 12.5],

        '主串分路电阻(Ω)': [1e-7, 0.15],
        '被串分路电阻(Ω)': [1e-7, 0.15],

        '主串电平级': [1, 2],
        '电源电压': ['最大', 34],

        '分路间隔(m)': [1],

        'FT1-U二次侧输出电压(V)': [40, 100],
        '调整电阻(Ω)': [50, 100, 150, 200],
        '调整电感(H)': [None],
        '调整电容(F)': [None],
        '调整RLC模式': ['串联', '并联'],

        'NGL-C1(μF)': [1],

        'WGL-C1(μF)': [1],
        'WGL-C2(μF)': [20],
        'WGL-L1-R(Ω)': [None],
        'WGL-L1-L(H)': [0.5],
        'WGL-L2-R(Ω)': [None],
        'WGL-L2-L(mH)': [5],
        'WGL-BPM变比': [4, 5],

        '扼流变压器变比': [3, 4],
        'BE-Rm(Ω)': [110],
        'BE-Lm(H)': [0.024],
    }
    return ret


# 25Hz电码化混合
def init_input_ZN_25Hz_coding_mix():
    ret = {
        '备注': ['无'],
        '线路名称': ['无'],
        '车站名称': ['无'],

        '主串区段': ['I'],
        '被串区段': ['II'],

        '主串区段长度(m)': [500],
        '被串区段长度(m)': [500],

        '主串坐标': [0],
        '被串坐标': [0],
        '并行长度(m)': [None],

        '线间距': [None],
        '耦合系数': [24],

        '主串频率(Hz)': [1700, 2000, 2300, 2600],
        # '主串频率(Hz)': [2300],
        '被串频率(Hz)': [1700, 2000, 2300, 2600],

        '主串电容数(含TB)': [5, 6, 7],
        '被串电容数(含TB)': [5, 6, 7],

        '主串电容值(μF)': [25, 40, 46, 55, 60, 80],
        '被串电容值(μF)': [25],

        '主串道床电阻(Ω·km)': [10000],
        '被串道床电阻(Ω·km)': [10000],

        '主串方向': ['右发'],
        '被串方向': ['右发'],

        '主串电缆长度(km)': [10],
        '被串电缆长度(km)': [10],

        '主串分路电阻(Ω)': [1e-7],
        '被串分路电阻(Ω)': [1e-7],

        '主串电平级': [1],
        '电源电压': ['最大'],

        '分路间隔(m)': [1],

        'FT1-U二次侧输出电压(V)': [40],
        '调整电阻(Ω)': [50, 100, 150, 200],
        '调整电感(H)': [None],
        '调整电容(F)': [None],
        '调整RLC模式': ['串联'],

        'NGL-C1(μF)': [1],

        'WGL-C1(μF)': [1],
        'WGL-C2(μF)': [20],
        'WGL-L1-R(Ω)': [None],
        'WGL-L1-L(H)': [0.5],
        'WGL-L2-R(Ω)': [None],
        'WGL-L2-L(mH)': [5],
        'WGL-BPM变比': [4],

        '扼流变压器变比': [3],
        'BE-Rm(Ω)': [110],
        'BE-Lm(H)': [0.024],
    }
    return ret


def config_loop_df(src: dict):

    key_list = []
    value_list = []

    for key, value in src.items():
        key_list.append(key)
        value_list.append(value)
    key_list.insert(0, '序号')

    clist = []
    for index, row in enumerate(itertools.product(*value_list)):
        tmp = list(row)
        tmp.insert(0, index + 1)
        clist.append(tmp)

    ret = pd.DataFrame(clist, columns=key_list)

    return ret


def config_loop_df_test(src: dict):

    key_list = []
    for key in src.keys():
        key_list.append(key)
    key_list.insert(0, '序号')

    row0 = []
    changes = []

    for index, value in enumerate(src.values()):
        tmp = list(value)
        row0.append(tmp[0])
        if len(tmp) > 1:
            changes.append([index, tmp[1]])

    value_list = []
    for index, value in changes:
        value_list.append(row0)
        tmp = row0.copy()
        tmp[index] = value
        value_list.append(tmp)

    clist = []
    for index, row in enumerate(value_list):
        tmp = list(row)
        tmp.insert(0, index + 1)
        clist.append(tmp)

    ret = pd.DataFrame(clist, columns=key_list)

    return ret


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 100000)

    d0 = init_input_ZN_25Hz_coding_mix_test()
    # s1 = config_loop_df(d0)
    s1 = config_loop_df_test(d0)

    print(s1)