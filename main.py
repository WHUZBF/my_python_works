import copy
from fraction import Fraction as Frac
from fraction import multiply as mul
from fraction import plus_minus as pm
from matrix import Matrix as Mat
from matrix import mat_mul as by
from matrix import merge
from matrix import identity_matrix as make_E
from matrix import mat_plus_minus as mpm
import re
import json
'''这个项目用于计算机计算行列式'''
'''main函数的整体打算是通过正则表达式和分支语句做成交互式命令行系统'''
'''还有许多计算功能有待完善'''
if __name__ == "__main__":
    '''主程序'''
    matrixs = {}    #创建矩阵字典,方便存放矩阵和它的名称
    flag = True
    caculate_flag=0
    draft_flag = 0
    while flag:
        #清空变量
        mat_2,mat_1,ans = None,None,None    #除了结果，全部删除
        #mat_1 和 mat_2 是计算矩阵,mat_3是结果矩阵 ans存储一般性结果(纯数字)
        try:
            cmd = input(">>>")
            #一些flag的定义
            flag_1=False
            match_1 = re.match('(.+) (.+)',cmd)   #创建命令匹配正则表达式第一种
            # 关于矩阵运算的专用符号
            match_mat = re.match("(.+) (.+) (.*)", cmd)
            if match_1:
                #匹配成功标志
                flag_1 = 1
            if cmd == 'exit':
                '''退出命令'''
                flag = False
                print("感谢使用")
            elif cmd == 'help':
                '''查看帮助文档'''
                '''设想使用json做成一个字典型文档,方便查看各个函数的精确用法'''
                with open('矩阵计算器官方使用文档.json') as h:
                    for text in h.read():
                        print(text,end = '')
                    print("\n")
            elif cmd == 'view_all':
                '''查看矩阵列表'''
                print(matrixs.keys())
            #双语言模式
            elif flag_1 and match_1.group(1) == 'define':
                '''定义矩阵'''
                matrixs[match_1.group(2)] = Mat(data=[],print_D_T=False)
            elif flag_1 and match_1.group(1) == 'revise':
                '''修改矩阵'''
                re_mat = matrixs.get(match_1.group(2),"Error") #尝试在矩阵字典中寻找矩阵
                if re_mat == "Error":
                    print(">>>Error:该矩阵尚未定义")
                else:
                    re_mat.revise_data()
            elif flag_1 and match_1.group(1)=='view':
                #查看矩阵
                mat_1=matrixs.get(match_1.group(2),"Error")
                if mat_1 == 'Error':
                    print(">>>矩阵未定义")
                else:
                    mat_1.output_data(mat_1.data,"请您过目")
            elif flag_1 and match_1.group(1) == 'save_as':
                # 保存上次运行的结果
                matrixs[match_1.group(2)] = mat_3
            elif cmd == 'caculate_mod':
                '''更改为计算模式'''
                text = "当前模式为计算模式,输入modend退出"
                print(text.center(40,'-'))
                caculate_flag = True
            elif cmd == 'draft_mod':
                '''更改为草稿模式'''
                text = "当前计算模式为草稿模式,输入modend退出"
                print(text.center(40, '-'))
                seq=[] #新建一个操作序列
                while True:
                    mat_name = input("输入一个矩阵开始:")
                    matrix = matrixs.get(mat_name,False)
                    if matrix:
                        break
                    else:
                        print("输入错误请重新输入")
                draft_mat = copy.deepcopy(matrix)   #新建一个操作矩阵
                draft_flag = True
            elif cmd == "modend":
                '''退出模式'''
                print("已退出计算/草稿模式".center(40,'-'))
                caculate_flag,draft_flag = False,False

            #以下为计算模式的命令
            elif caculate_flag and match_mat and match_mat.group(2) == 'by':
                '''求矩阵的乘积'''
                mat_1=matrixs.get(match_mat.group(1),"Error")
                mat_2=matrixs.get(match_mat.group(3),"Error")
                if mat_1 == 'Error' or mat_2 == 'Error':
                    print(">>>Error:矩阵尚未定义")
                else:
                    mat_3=by(mat_1,mat_2)
                    if mat_3:
                        mat_3.output_data(mat_3.data,"ans = ")
            elif caculate_flag and match_mat and (match_mat.group(2) == 'plus' or match_mat.group(2) == 'minus'):
                '''求矩阵的加减法'''
                mod = 1
                if match_mat.group(2)=='minus':
                    mod = -1
                mat_1 = matrixs.get(match_mat.group(1), "Error")
                mat_2 = matrixs.get(match_mat.group(3), "Error")
                if mat_1 == 'Error' or mat_2 == 'Error':
                    print(">>>Error:矩阵尚未定义")
                else:
                    mat_3 = mpm(mat_1,mat_2,mod)
                    if mat_3:
                        mat_3.output_data(mat_3.data,"ans = ")

            #下面是单目运算
            elif caculate_flag and match_1.group(1) and match_1.group(2):
                mat_1 = matrixs.get(match_1.group(2), "Error")
                if mat_1 == 'Error':
                    print(">>>Error:矩阵尚未定义或语法错误")
                else:
                    if match_1.group(1)=='reverse':
                        #求逆矩阵
                        mat_3 = mat_1.reverse()
                        if mat_3:
                            mat_3.output_data(mat_3.data,">>>逆矩阵为:")
                    elif match_1.group(1) =='det':
                        #求行列式
                        mat_1.det()
                    elif match_1.group(1)=='trac':
                        #求迹
                        ans = mat_1.trac()
                        if ans:
                            print(f">>>矩阵的迹为:{ans.str}")
                    elif match_1.group(1) == 'adj':
                        #求伴随矩阵
                        mat_3 = mat_1.adjugate()
                        if mat_3:
                            mat_3.output_data(mat_3.data,">>>伴随矩阵为:")
                    elif match_1.group(1)=='simplify' or match_1.group(1)=='simplest':
                        #求最简式或者简化阶梯型
                        mod = 0
                        if match_1.group(1)=='simplest':
                            mod = 1
                        mat_3 = mat_1.simplify(mod)
                        mat_3.output_data(mat_3.data,'ans = ')
                    elif match_1.group(1) == 'LU':
                        #矩阵进行LU分解
                        mat_1.LU()
                    elif match_1.group(1) == 'schmidt':
                        #矩阵进行正交化
                        mat_3=mat_1.schmidt()

                    else:
                        print(">>>未知命令")
            elif draft_flag:
                '''草稿模式运算,不使用正则表达式'''
                operate = None
                string = cmd.split()     #获取一个操作列表
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
                        f=draft_mat.exchange(int(string[1]),int(string[2]),mod = string[-1])
                        if f:
                            operate = f'{string[-1]}[{int(string[1])}]<->{string[-1]}[{int(string[2])}]'

                    elif string[0] == 'times':
                        m = re.match("(.+)/(.+)", string[3])  # 支持录入负数
                        if m:
                            k=Frac(int(m.group(1)), int(m.group(2)))  # 一定要注意这里的类型转换
                        else:
                            k=Frac(int(string[3]),1)  # 不是输入的分数时直接转换为整数类型

                        f=draft_mat.k_r(int(string[1]),int(string[2]),k,mod = string[-1])
                        if f:
                            operate = f'{string[-1]}[{int(string[1])}]+({k.str}){string[-1]}[{int(string[2])}]'

                    elif string[0]=='mul':
                        m = re.match("(.+)/(.+)", string[2])  # 支持录入负数
                        if m:
                            k = Frac(int(m.group(1)), int(m.group(2)))  # 一定要注意这里的类型转换
                        else:
                            k = Frac(int(string[2]),1)  # 不是输入的分数时直接转换为整数类型

                        f=draft_mat.times(int(string[1]),k,mod = string[-1])
                        if f:
                            operate = f'{k.str}{string[-1]}[{int(string[1])}]'
                    seq.append(operate)     #添加操作到序列之中
                    draft_mat.output_data(draft_mat.data,'操作后矩阵为:')

            else:
                print(">>>无法识别的命令")
        except Exception as e:
            print(">>>未知错误")