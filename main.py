'''这个项目用于计算机计算行列式'''
'''main函数的整体打算是通过正则表达式和分支语句做成交互式命令行系统'''
from fraction import Fraction as Frac
from fraction import multiply as mul
from fraction import plus_minus as pm
from matrix import Matrix

if __name__ == "__main__":
    flag = True
    while flag:
        cmd = input(">>>")
        if cmd == 'exit':
            '''退出命令'''
            flag = False
            print("感谢使用")
