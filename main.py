import copy
import other
from fraction import Fraction as Frac
from fraction import multiply as mul
from fraction import plus_minus as pm
from matrix import Matrix as Mat
from matrix import mat_mul as by
from matrix import merge
from matrix import identity_matrix as make_E
from matrix import mat_plus_minus as mpm
from matrix import load_matrix
from matrix import FloatMatrix
from matrix import dot_mul
from matrix import dot_calculate
from matrix import BoolMatrix
import re
import json
import time
'''这个项目用于计算机计算行列式'''
'''main函数的整体打算是通过正则表达式和分支语句做成交互式命令行系统'''
'''还有许多计算功能有待完善'''


version = 'v1.2.0'
print('-'*10+f"欢迎使用矩阵计算器  需要帮助请使用help  版本号：{version}"+'-'*10)   # 使用format格式字符串
print('*'*16+"我的github地址是'github.com/WHUZBF'"+'*'*16)


def guess(input_cmd):
    """宏定义guess不要在意太多局部变量"""
    str_ = input_cmd.split(" ")[0]
    deg = {}
    for key in doc_lib.keys():
        if key in ['', 'calculate']:
            continue  # 直接略过
        degree = other.string_distance_dp(key, str_)
        deg[key] = 1 - degree / (max(len(key), len(str_)))
    best_fit = max(deg.values())
    if best_fit == 1:
        print("...命令正确,请查看是否在对应模式下")
        you_want = str_
    elif best_fit >= 0.5:
        you_want = max(deg, key=lambda k: deg[k])
        print(f"...或许您想输入  {you_want}")
    else:
        you_want = None
    del deg
    return you_want


if __name__ == "__main__":
    '''主程序'''
    matrixs = {}    # 创建矩阵字典,方便存放矩阵和它的名称
    flag = True
    calculate_flag = 0
    draft_flag = 0
    bool_flag = 0
    format_len = 5
    # 创建一个文档字典
    # 字典中使用逗号隔开
    doc_lib = {
        "define": "Mat.__init__",
        "exit": "other.Doc.flag",
        "view": "other.Doc.matrixs",
        "view_all": "other.Doc.matrixs",
        "view_f": "other.Doc.matrixs",
        "revise": "Mat.revise_data",
        "load": "load_matrix",
        "format": "other.Doc.format_len",
        "doc": "other.Doc.doc",
        "help": "other.Doc.help",
        "trac": "Mat.trac",
        "inv": "Mat.reverse",
        "adj": "Mat.adjugate",
        "det": "Mat.det",
        "simplify": "Mat.simplify",
        "simplest": "Mat.simplify",
        "save_as": "other.Doc.save_as",
        "LU": "Mat.LU",
        "schmidt": "Mat.schmidt",
        "eig": "Mat.eig",
        "unit": "Mat.unit",
        "transpose": "Mat.transpose",
        "rank": "Mat.mat_rank",
        "value": "other.Doc.value",
        "calculate": "other.Doc.calculate",
        "calculate_mode": "other.Doc.calculate_mode",
        "draft_mode": "other.Doc.draft_mode",
        "bool_mode": "other.Doc.bool_mode",
        "mode_end": "other.Doc.mode_end",
        "view_op": "other.Doc.view_op",
        "mul": "other.Doc.mul",
        "times": "other.Doc.times",
        "exchange": "other.Doc.exchange",
        "bool": "BoolMatrix.data_init",
        "not": "BoolMatrix.NOT",
        "!": "BoolMatrix.NOT",
        "and": "BoolMatrix.AND",
        "&": "BoolMatrix.AND",
        "or": "BoolMatrix.OR",
        "|": "BoolMatrix.OR",
        "xor": "BoolMatrix.XOR",
        "^": "BoolMatrix.XOR",
        "#": "BoolMatrix.BoolProduct",
        "#^": "BoolMatrix.BoolPower",
    }
    key_words = doc_lib.keys()

    while flag:
        # 清空变量
        mat_2, mat_1, ans = None, None, None    # 除了结果，全部删除
        # mat_1 和 mat_2 是计算矩阵,mat_3是结果矩阵 ans存储一般性结果(纯数字)
        try:
            cmd = input(">>>")
            cmd = cmd.strip()
            # 一些flag的定义
            flag_1 = False
            match_1 = re.match('(.+) (.+)', cmd)   #创建命令匹配正则表达式第一种
            # 关于矩阵运算的专用符号
            match_mat = re.match("(.+) (.+) (.*)", cmd)
            if match_1:
                # 匹配成功标志
                flag_1 = 1
            if cmd == 'exit':
                '''退出命令'''
                flag = False
                print("感谢使用")
            elif cmd == 'help':
                '''查看帮助文档'''
                filename = '矩阵计算器官方使用文档.txt'
                try:
                    with open(filename, encoding='utf-8') as h:
                        while True:
                            text = h.readline()
                            if not text:
                                break
                            print(text, end='')
                            time.sleep(0.5)
                except FileNotFoundError:
                    print("!未找到相关文件，可能已重命名或者删除!")
            elif cmd == 'view_all':
                '''查看矩阵列表'''
                item = matrixs.items()
                ls = []
                for i in item:
                    if type(i[1]) == FloatMatrix:
                        ls.append(i[0] + "(FloatMatrix)")
                    elif type(i[1]) == BoolMatrix:
                        ls.append(i[0] + "(BoolMatrix)")
                    else:
                        ls.append(i[0])
                print(ls)
            elif cmd == 'doc':
                print("所有文档条目如下:")
                print(doc_lib.keys())
            # 双语言模式
            elif flag_1 and match_1.group(1) == 'define':
                '''定义矩阵'''
                mat_name = match_1.group(2).strip()
                if mat_name in key_words:
                    print("...请不要使用关键字作为矩阵名称")
                else:
                    matrixs[mat_name] = Mat(data=[], print_D_T=False)
            elif flag_1 and match_1.group(1) == 'load':
                """加载矩阵"""
                matrixs[match_1.group(2)] = load_matrix()
            elif flag_1 and match_1.group(1) == 'revise':
                '''修改矩阵'''
                re_mat = matrixs.get(match_1.group(2), "Error")  # 尝试在矩阵字典中寻找矩阵
                if re_mat == "Error":
                    print(">>>Error:该矩阵尚未定义")
                else:
                    re_mat.revise_data()
            elif flag_1 and (match_1.group(1) == 'view' or match_1.group(1) == 'view_f'):
                # 查看矩阵
                mat_1=matrixs.get(match_1.group(2), "Error")
                if mat_1 == 'Error':
                    print(">>>矩阵未定义")
                else:
                    if match_1.group(1) == 'view_f':
                        mat_1.output(format_len)
                    else:
                        mat_1.output_data(mat_1.data, "请您过目")
            elif flag_1 and match_1.group(1) == 'save_as':
                # 保存上次运行的结果
                print("...保存成功!")
                if draft_flag:
                    # 这个时候已经保证了draft_mat的存在性
                    # 草稿模式下保存draft_mat
                    matrixs[match_1.group(2)] = draft_mat
                    continue
                matrixs[match_1.group(2)] = mat_3
            elif flag_1 and match_1.group(1) == 'doc':
                # 查文档
                doc_cmd = match_1.group(2)
                doc_want = doc_lib.get(doc_cmd, None)
                if doc_want:
                    doc_want += '.__doc__'
                    exec("print(" + doc_want + ")")   # python里面不分单双引号
                else:
                    print(">>>未找到相应文档")
                    deg = {}
                    for key in doc_lib.keys():
                        degree = other.string_distance_dp(key, doc_cmd)
                        deg[key] = 1 - degree / (max(len(key), len(doc_cmd)))
                    if max(deg.values()) >= 0.5:
                        you_want = max(deg, key=lambda k: deg[k])    # k目前是局部变量,屏蔽之前的全局变量
                        print(f"...或许您想输入  {you_want}")
                    del deg

            elif cmd == 'calculate_mode':
                if draft_flag:
                    print("请先退出草稿模式")
                    continue  # 直接下一次循环这个语句是在循环体内部
                elif bool_flag:
                    print("请先退出布尔模式")
                    continue
                '''更改为计算模式'''
                text = "当前模式为计算模式,输入mode_end退出"
                print(text.center(40,'-'))
                calculate_flag = True
            elif cmd == 'draft_mode':
                if calculate_flag:
                    print("请先退出计算模式")
                    continue
                elif bool_flag:
                    print("请先退出布尔模式")
                    continue
                '''更改为草稿模式'''
                text = "当前计算模式为草稿模式,输入mode_end退出"
                print(text.center(40, '-'))
                seq = []  # 新建一个操作序列
                while True:
                    mat_name = input("输入一个矩阵开始:")
                    matrix = matrixs.get(mat_name, False)
                    if matrix:
                        if type(matrix) == Mat:
                            break
                        else:
                            print("...仅支持普通矩阵")
                    elif mat_name == 'mode_end':
                        draft_flag = False
                        print("终止模式初始化")
                    else:
                        print("...输入错误请重新输入")
                draft_mat = copy.deepcopy(matrix)   # 新建一个操作矩阵
                draft_flag = True
            elif cmd == "bool_mode":
                '''进入bool模式'''
                if draft_flag:
                    print("请先退出草稿模式")
                    continue
                elif calculate_flag:
                    print("请先退出计算模式")
                    continue
                text = "当前模式为布尔模式,输入mode_end退出"
                print(text.center(40, '-'))
                bool_flag = True

            elif cmd == "mode_end":
                '''退出模式'''
                if calculate_flag:
                    print("已退出计算模式".center(40, '-'))
                elif draft_flag:
                    print("已退出草稿模式".center(40, '-'))
                elif bool_flag:
                    print("已退出布尔模式".center(40, '-'))
                else:
                    print("当前未进入任何特殊模式")
                    continue
                calculate_flag, draft_flag, bool_flag = False, False, False
            elif flag_1 and match_1.group(1) == 'format':
                format_len = int(match_1.group(2))

            # 以下为计算模式的命令
            elif calculate_flag and match_mat and match_mat.group(2) == '@':
                '''求矩阵的乘积'''
                mat_1=matrixs.get(match_mat.group(1),"Error")
                mat_2=matrixs.get(match_mat.group(3),"Error")
                if mat_1 == 'Error' or mat_2 == 'Error':
                    print(">>>Error:矩阵尚未定义")
                else:
                    mat_3=by(mat_1,mat_2)
                    if mat_3:
                        mat_3.output_data(mat_3.data,"ans = ")
            elif calculate_flag and match_mat and (match_mat.group(2) == '+' or match_mat.group(2) == '-'):
                '''求矩阵的加减法'''
                mod = 1
                if match_mat.group(2)=='-':
                    mod = -1
                mat_1 = matrixs.get(match_mat.group(1), "Error")
                mat_2 = matrixs.get(match_mat.group(3), "Error")
                if mat_1 == 'Error' or mat_2 == 'Error':
                    print(">>>Error:矩阵尚未定义")
                else:
                    mat_3 = mpm(mat_1,mat_2,mod)
                    if mat_3:
                        mat_3.output_data(mat_3.data,"ans = ")
            elif calculate_flag and match_mat and (match_mat.group(2) == ',' or match_mat.group(2) == ';'):
                '''合并矩阵'''
                way = match_mat.group(2)
                mat_1 = matrixs.get(match_mat.group(1), "Error")
                mat_2 = matrixs.get(match_mat.group(3), "Error")
                if mat_1 == 'Error' or mat_2 == 'Error':
                    print(">>>Error:矩阵尚未定义")
                else:
                    if way == ',':
                        mat_3 = merge(mat_1,mat_b)
                    elif way == ';':
                        mat_3 = merge(mat_1,mat_b,';')  # 还可以用value= 的方式写入参数，不受位置约束
                    mat_3.output_data(mat_3,"合并后矩阵为：")
            elif calculate_flag and match_mat and (match_mat.group(2) == '^' or match_mat.group(2) == 'f^'):
                '''求矩阵的n次方'''
                mat_1 = matrixs.get(match_mat.group(1), "Error")
                num = int(match_mat.group(3))
                if mat_1 == 'Error':
                    print(">>>Error:矩阵尚未定义")
                elif match_mat.group(2) == 'f^':
                    mat_3 = mat_1.pow_mat(num)
                    mat_3.output_fdata(f"矩阵的{num}次方为：", format_len)
                else:
                    mat_3 = mat_1.pow_mat(num)
                    mat_3.output_data(mat_3.data, f"矩阵的{num}次方为：")
            elif calculate_flag and match_mat and (match_mat.group(2) in ['*', '/']):
                '''对应元素乘积'''
                mod = match_mat.group(2)
                mat_1 = matrixs.get(match_mat.group(1), "Error")
                mat_2 = matrixs.get(match_mat.group(3), "Error")
                if mat_1 == 'Error' or mat_2 == 'Error':
                    print(">>>Error:矩阵尚未定义")
                elif (mat_1.r_num,mat_1.c_num) != (mat_2.r_num,mat_2.c_num) :
                    print(">>>非同型矩阵,无法计算")
                else:
                    try:
                        mat_3 = dot_mul(mat_1, mat_2, mod)
                        mat_3.output_data(mat_3.data, "ans=")
                    except ZeroDivisionError:
                        print(">>>计算过程中出现意外的无穷大")
            elif calculate_flag and match_mat and (match_mat.group(2) in ['.*', '.-', '.+', '.^']):
                mod = match_mat.group(2)
                num = match_mat.group(3).strip()
                if '/' in num:
                    num_s = num.split('/')
                    num = Frac(int(num_s[0]), int(num_s[1]))
                else:
                    num = int(num)
                mat_1 = matrixs.get(match_mat.group(1), "Error")
                if mat_1 == 'Error':
                    print(">>>Error:矩阵尚未定义")
                else:
                    mat_3 = dot_calculate(mat_1, num,mod)
                    if mat_3:
                        mat_3.output_data(mat_3.data, "ans=")
            # 下面是单目运算
            elif calculate_flag and match_1 and match_1.group(1) and match_1.group(2):
                mat_1 = matrixs.get(match_1.group(2), "Error")
                if mat_1 == 'Error':
                    print(">>>Error:矩阵尚未定义或语法错误")
                else:
                    if match_1.group(1) == 'inv':
                        # 求逆矩阵
                        mat_3 = mat_1.reverse()
                        if mat_3:
                            mat_3.output_data(mat_3.data,">>>逆矩阵为:")
                    elif match_1.group(1) =='det':
                        # 求行列式
                        mat_1.det()
                    elif match_1.group(1)=='trac':
                        # 求迹
                        ans = mat_1.trac()
                        if ans:
                            print(f">>>矩阵的迹为:{ans.str}")
                    elif match_1.group(1) == 'adj':
                        # 求伴随矩阵
                        mat_3 = mat_1.adjugate()
                        if mat_3:
                            mat_3.output_data(mat_3.data,">>>伴随矩阵为:")
                    elif match_1.group(1)=='simplify' or match_1.group(1)=='simplest':
                        # 求最简式或者简化阶梯型
                        mod = 0
                        if match_1.group(1)=='simplest':
                            mod = 1
                        mat_3 = mat_1.simplify(mod)
                        mat_3.output_data(mat_3.data,'ans = ')
                    elif match_1.group(1) == 'LU':
                        # 矩阵进行LU分解
                        mat_1.LU()
                    elif match_1.group(1) == 'schmidt':
                        # 矩阵进行正交化
                        mat_3 = mat_1.schmidt()
                    elif match_1.group(1) == 'eig':
                        # 计算矩阵特征值
                        ans = mat_1.eig()
                        print(f"特征值：\t{ans[0]}")
                        print("特征向量为：")
                        # print(ans[1])
                        max_len = 1
                        for value_array in ans[1]:
                            for value in value_array:
                               if len(str(value)) > max_len:
                                   max_len = len(str(value))
                        if max_len > format_len:
                            max_len = format_len

                        # print("pi2 = %.*f" % (3, PI)) # *表示从后面的元组中读取3，定义精度

                        for value_array in ans[1]:
                            print("\t\t[",end='')
                            for value in value_array:
                                value = float(str(value).lstrip("(").rstrip(")"))
                                value = "%.*f" % (max_len, value)
                                # print(value.center(max_len, ' ') + '  ', end='')
                                print(value.rjust(max_len+3, ' ') + '  ', end='')  # rjust右对齐
                            print("\b\b]")
                    elif match_1.group(1) == 'unit':
                        # 单位化矩阵
                        mat_3 = mat_1.unit()
                    elif match_1.group(1) == 'transpose':
                        # 转置矩阵
                        mat_3 = Mat(mat_1.transpose(), False)
                        mat_3.output_data(mat_3.data, "转置矩阵为：")
                    elif match_1.group(1) == 'rank':
                        # 求矩阵的秩
                        print(f"矩阵的秩为：  {mat_1.rank}")
                    elif match_1.group(1) == 'value':
                        # 将矩阵变为数值矩阵
                        mat_3 = FloatMatrix(mat_1.data)
                        mat_3.output_fdata("数值矩阵为：", format_len)
                    else:
                        print(">>>未知命令")
                        guess(cmd)

            elif draft_flag:
                '''草稿模式运算,不使用正则表达式'''
                operate = None
                string = cmd.split()     # 获取一个操作列表
                if string[0] == 'view_op':
                    print("进行的初等行变换为:")
                    for x in seq:
                        print(x, end=" >> ")
                    print("\b" * 4 + ' ' * 4)
                elif string[-1] != 'c' and string[-1] != 'r':
                    print('Error:输入错误')
                else:
                    for i in string:
                        i = i.strip()
                    if string[0] == 'exchange':
                        f = draft_mat.exchange(int(string[1]),int(string[2]),mod = string[-1])
                        if f:
                            operate = f'{string[-1]}[{int(string[1])}]<->{string[-1]}[{int(string[2])}]'

                    elif string[0] == 'times':
                        m = re.match("(.+)/(.+)", string[3])  # 支持录入负数
                        if m:
                            k = Frac(int(m.group(1)), int(m.group(2)))  # 一定要注意这里的类型转换
                        else:
                            k = Frac(int(string[3]),1)  # 不是输入的分数时直接转换为整数类型

                        f=draft_mat.k_r(int(string[1]),int(string[2]),k,mod = string[-1])
                        if f:
                            operate = f'{string[-1]}[{int(string[1])}]+({k.str})*{string[-1]}[{int(string[2])}]'

                    elif string[0] == 'mul':
                        m = re.match("(.+)/(.+)", string[2])  # 支持录入负数
                        if m:
                            k = Frac(int(m.group(1)), int(m.group(2)))  # 一定要注意这里的类型转换
                        else:
                            k = Frac(int(string[2]),1)  # 不是输入的分数时直接转换为整数类型

                        f=draft_mat.times(int(string[1]), k, mod=string[-1])
                        if f:
                            operate = f'{k.str}*{string[-1]}[{int(string[1])}]'
                    seq.append(operate)     # 添加操作到序列之中
                    draft_mat.output_data(draft_mat.data, '操作后矩阵为:')

            elif bool_flag:
                """布尔计算模式"""
                _cmd = cmd.rstrip().split()
                if _cmd[0] == 'bool':
                    """定义一个boolmatrix"""
                    mat_name = _cmd[1].strip()
                    if mat_name in key_words:
                        print("...请不要使用关键字作为矩阵名称")
                    else:
                        matrixs[mat_name] = BoolMatrix()
                elif _cmd[0] in ['!', 'not']:
                    mat_1 = matrixs.get(_cmd[1], None)
                    if not mat_1:
                        print("...矩阵未定义")
                        continue
                    mat_3 = mat_1.NOT()
                    mat_3.output_data(mat_3.data, f"NOT {_cmd[1]} = ")
                elif len(_cmd) == 3:
                    mat_1 = matrixs.get(_cmd[0], None)
                    mat_2 = matrixs.get(_cmd[2], None)
                    if _cmd[1] == "#^":
                        mat_2 = int(_cmd[2])
                    if (not mat_1) or ((_cmd[1] != '#^') and (not mat_2)):
                        print("...矩阵未定义")
                        continue

                    if _cmd[1] == "#^":
                        mat_3 = mat_1.BoolPower(mat_2)
                        mat_3.output_data(mat_3.data, f"A[{_cmd[0]}] = ")
                    elif _cmd[1] == "#":
                        mat_3 = mat_1.BoolProduct(mat_2)
                        mat_3.output_data(mat_3.data, f"{_cmd[0]} ⊙ {_cmd[2]} = ")
                    elif _cmd[1] in ["and", '&']:
                        mat_3 = mat_1.AND(mat_2)
                        mat_3.output_data(mat_3.data, f"{_cmd[0]} AND {_cmd[2]} = ")
                    elif _cmd[1] in ["or", '|']:
                        mat_3 = mat_1.OR(mat_2)
                        mat_3.output_data(mat_3.data, f"{_cmd[0]} OR {_cmd[2]} = ")
                    elif _cmd[1] in ["xor", '^']:
                        mat_3 = mat_1.XOR(mat_2)
                        mat_3.output_data(mat_3.data, f"{_cmd[0]} XOR {_cmd[2]} = ")
                else:
                    print("...未知命令")
                    guess(cmd)
            else:
                print(">>>无法识别的命令")
                guess(cmd)

        except Exception as e:
            print(">>>未知错误")

        # except FileNotFoundError:
        #     ...