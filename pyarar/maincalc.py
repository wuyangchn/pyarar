#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : maincalc.py
# @Author : Yang Wu
# @Date   : 2021/12/25
# @Email  : wuy@cug.edu.cn

from pyarar import calcFuncs as ProFunctions
from pyarar import sample

def corrBlank(sp: sample.Sample):
    if sp.CorrBlank:
        sp.Ar36TempList, sp.Ar36TempErrorList \
            = ProFunctions.corr_blank(sp.Ar36MList, sp.Ar36MErrorList, sp.Ar36BList, sp.Ar36BErrorList)
        sp.Ar37TempList, sp.Ar37TempErrorList \
            = ProFunctions.corr_blank(sp.Ar37MList, sp.Ar37MErrorList, sp.Ar37BList, sp.Ar37BErrorList)
        sp.Ar38TempList, sp.Ar38TempErrorList \
            = ProFunctions.corr_blank(sp.Ar38MList, sp.Ar38MErrorList, sp.Ar38BList, sp.Ar38BErrorList)
        sp.Ar39TempList, sp.Ar39TempErrorList \
            = ProFunctions.corr_blank(sp.Ar39MList, sp.Ar39MErrorList, sp.Ar39BList, sp.Ar39BErrorList)
        sp.Ar40TempList, sp.Ar40TempErrorList \
            = ProFunctions.corr_blank(sp.Ar40MList, sp.Ar40MErrorList, sp.Ar40BList, sp.Ar40BErrorList)

def corrDiscr(sp: sample.Sample):
    def _func(a0, e0, f):
        k1 = [ProFunctions.error_mul((a0[i], e0[i]), (f[0], f[1])) for i in range(len(a0))]
        k0 = [a0[i] * f[0] for i in range(len(a0))]
        return k0, k1
    if sp.CorrDiscr:
        # Mass Discrimination based on the mass of Ar40, Ar36 | Ar37 | Ar38 | Ar39
        MDF, sMDF = sp.MDF, sp.MDFError
        M36, M37, M38, M39, M40 = sp.Ar36Mass, sp.Ar37Mass, sp.Ar38Mass, sp.Ar39Mass, sp.Ar40Mass
        c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M36, M40)  # 36Ar
        sp.Ar36TempList, sp.Ar36TempErrorList = _func(sp.Ar36TempList, sp.Ar36TempErrorList, c)
        c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M37, M40)  # 37Ar
        sp.Ar37TempList, sp.Ar37TempErrorList = _func(sp.Ar37TempList, sp.Ar37TempErrorList, c)
        c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M38, M40)  # 38Ar
        sp.Ar38TempList, sp.Ar38TempErrorList = _func(sp.Ar38TempList, sp.Ar38TempErrorList, c)
        c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M39, M40)  # 39Ar
        sp.Ar39TempList, sp.Ar39TempErrorList = _func(sp.Ar39TempList, sp.Ar39TempErrorList, c)

def corrDecay(sp: sample.Sample):
    def _func(a0, e0, f):
        k1 = ProFunctions.error_mul((a0, e0), (f[0], f[1]))
        k0 = a0 * f[0]
        return k0, k1
    # Decay Correction
    t2 = sp.IrradiationEndTimeList  # irradiation end time in second
    t3 = sp.IrradiationDurationList  # irradiation duration time in hour
    if sp.Corr37ArDecay:
        for row in range(len(sp.Ar37TempList)):
            c = ProFunctions.corr_decay(sp.MDateTimeList[row], t2, t3, sp.Ar37Const, sp.Ar37ConstError)  # 37Ar
            sp.Ar37TempList[row], sp.Ar37TempErrorList[row] \
                = _func(sp.Ar37TempList[row], sp.Ar37TempErrorList[row], c)
    if sp.Corr39ArDecay:
        for row in range(len(sp.Ar39TempList)):
            c = ProFunctions.corr_decay(sp.MDateTimeList[row], t2, t3, sp.Ar39Const, sp.Ar39ConstError)  # 39Ar
            sp.Ar39TempList[row], sp.Ar39TempErrorList[row] \
                = _func(sp.Ar39TempList[row], sp.Ar39TempErrorList[row], c)

def correctFunc(self, all_param):
    # 初始化
    print('运行CorrectFunc')
    result = [];
    Cl36_partial = [[], []]
    for i in range(12):
        result.append([])
    # result列表的顺序：
    # 编号、温度、36Ar、s、37Ar、s、38Ar、s、39Ar、s、40Ar、s、
    MDF = float(all_param['Calculation']['MDF'])
    sMDF = float(all_param['Calculation']['sMDF'])  # sMDF为以百分数表示的相对误差
    k37 = (float(all_param['Calculation']['37ArConst']), float(all_param['Calculation']['37ArConstError']))  # Ar37衰变常数
    k39 = (float(all_param['Calculation']['39ArConst']), float(all_param['Calculation']['39ArConstError']))  # Ar39衰变常数
    k36 = (float(all_param['Calculation']['39ArConst']), float(all_param['Calculation']['39ArConstError']))  # Cl36衰变常数
    CorrBlank = bool(all_param['Calculation']['CorrBlank'])
    CorrDiscr = bool(all_param['Calculation']['CorrDiscr'])
    Corr37Decay = bool(all_param['Calculation']['Corr37ArDecay'])
    Corr39Decay = bool(all_param['Calculation']['Corr39ArDecay'])
    M40 = float(all_param['Calculation']['40ArMass'])  # M40 = 39.962383123
    M39 = float(all_param['Calculation']['39ArMass'])  # M39 = 38.964313
    M38 = float(all_param['Calculation']['38ArMass'])  # M38 = 37.9627322
    M37 = float(all_param['Calculation']['37ArMass'])  # M37 = 36.9667759
    M36 = float(all_param['Calculation']['36ArMass'])  # M36 = 35.96754628
    # M41 = 40.9645008
    # M35 = 34.9752567

    t1 = []  # 同位素测试时间
    t3_1 = all_param['Irradiation']['duration']  # 辐照持续时间，irradiation子窗口中设置,单位为小时
    try:
        t3_2 = all_param['Irradiation']['duration_list']
    except KeyError:
        t3 = [t3_1]
    else:
        t3 = t3_2
        pass
    t2_1 = all_param['Irradiation']['dateTime']  # 辐照结束时间
    try:
        t2_2 = all_param['Irradiation']['dateTime_list']
    except KeyError:
        t2 = [t2_1]
    else:
        t2 = t2_2
        pass
    initial = self.read_intercept_and_blank_data()
    result[0:2] = initial[0][0:2]
    # 校正本底
    print('本底校正')
    # Blank correction, Ar36 | Ar37 | Ar38 | Ar39 | Ar40
    if CorrBlank:
        result[2], result[3] = ProFunctions.corr_blank(initial[0][2], initial[0][3], initial[1][3], initial[1][4])
        result[4], result[5] = ProFunctions.corr_blank(initial[0][5], initial[0][6], initial[1][5], initial[1][6])
        result[6], result[7] = ProFunctions.corr_blank(initial[0][8], initial[0][9], initial[1][7], initial[1][8])
        result[8], result[9] = ProFunctions.corr_blank(initial[0][11], initial[0][12], initial[1][9],
                                                       initial[1][10])
        result[10], result[11] = ProFunctions.corr_blank(initial[0][14], initial[0][15], initial[1][11],
                                                         initial[1][12])
    else:
        result[2], result[3] = initial[0][2], initial[0][3]
        result[4], result[5] = initial[0][5], initial[0][6]
        result[6], result[7] = initial[0][8], initial[0][9]
        result[8], result[9] = initial[0][11], initial[0][12]
        result[10], result[11] = initial[0][14], initial[0][15]
    # 基于40Ar的质量歧视
    print('质量歧视校正')
    # Mass Discrimination, Ar36 | Ar37 | Ar38 | Ar39
    c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M36, M40) if CorrDiscr else [1, 0]  # 36Ar
    result[3] = [ProFunctions.error_mul((result[2][i], result[3][i]), (c[0], c[1])) for i in range(len(result[2]))]
    result[2] = [result[2][i] * c[0] for i in range(len(result[2]))]
    c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M37, M40) if CorrDiscr else [1, 0]  # 37Ar
    result[5] = [ProFunctions.error_mul((result[4][i], result[5][i]), (c[0], c[1])) for i in range(len(result[4]))]
    result[4] = [result[4][i] * c[0] for i in range(len(result[4]))]
    c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M38, M40) if CorrDiscr else [1, 0]  # 38Ar
    result[7] = [ProFunctions.error_mul((result[6][i], result[7][i]), (c[0], c[1])) for i in range(len(result[6]))]
    result[6] = [result[6][i] * c[0] for i in range(len(result[6]))]
    c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M39, M40) if CorrDiscr else [1, 0]  # 39Ar
    result[9] = [ProFunctions.error_mul((result[8][i], result[9][i]), (c[0], c[1])) for i in range(len(result[8]))]
    result[8] = [result[8][i] * c[0] for i in range(len(result[8]))]
    # 37Ar和39Ar的衰变校正
    print('衰变校正')
    # Decay Correction
    delta_t = []
    for row in range(len(initial[0][17])):  # 读取excel文件中的质谱测试时间
        t1.append([])
        t1[row].append(int(initial[0][19][row]))
        t1[row].append(int(initial[0][18][row]))
        t1[row].append(int(initial[0][17][row]))
        t1[row].append(int(initial[0][20][row]))
        t1[row].append(int(initial[0][21][row]))
        c = ProFunctions.corr_decay(t1[row], t2, t3, k37[0], k37[1])  # 37Ar
        result[5][row] = ProFunctions.error_mul((result[4][row], result[5][row]), (c[0], c[1])) \
            if Corr37Decay else result[5][row]
        result[4][row] = result[4][row] * c[0] if Corr37Decay else result[4][row]
        c = ProFunctions.corr_decay(t1[row], t2, t3, k39[0], k39[1])  # 39Ar
        result[9][row] = ProFunctions.error_mul((result[8][row], result[9][row]), (c[0], c[1])) \
            if Corr39Decay else result[9][row]
        result[8][row] = result[8][row] * c[0] if Corr39Decay else result[8][row]
        delta_t.append(c[2])
    return result, delta_t
