'''行列式的类'''
import re
from fraction import Fraction as Frac

#一些使用重构的函数
def choose(matrix,mod):
    if mod == 'r':
        mat = matrix.data[:]
        return mat
    elif mod == 'c':
        mat = matrix.D_T[:]
        return mat
    else:
        print("Error:Invalid argument")
        return 0


class Matrix:
    def __init__(self):
        self.order,self.c_num,self.r_num = 0,0,0  #定义矩阵阶数
        self.data = []  # 列表嵌套可以使用self.data[]来索引
        self.input_num()
        self.D_T = self.transpose()      #自动传入实参self
        self.output_data(self.D_T, '转置矩阵为')


    def output_data(self,data,msg='矩阵为:\n'):
        '''输出数据'''
        print(msg)
        for array in data:
            array = [num.str if not isinstance(num,int) else num for num in array]#列表解析处理分数变量的打印
            print(f'\t\t{array}')


    def input_num(self):
        '''输入矩阵的数据'''
        global element   #添加的全局变量语句
        data_str = input("输入数据,行与行之间用分号连接(包括最后一行),每个元素之间用逗号隔开:\n")
        if data_str[-1] != ';':
            data_str += ';'
        matches = re.findall('[^;]+;',data_str)   #提取每一行
        c_num = []
        for match in matches:
            elements = []
            for element in re.findall('[^,]*,',match.rstrip(';')+','):    #提取每一个数
                element=element.rstrip(',')  # 去掉逗号
                m = re.match('(\d*)/(\d*)',element)
                if m:
                     elements.append(Frac(m.group(1),m.group(2)))
                else:
                     elements.append(int(element))

            self.data.append(elements)
            c_num.append(len(elements))
        if len(set(c_num)) == 1:
            if c_num[0] == len(self.data):
                self.order = len(self.data)  # 表示出矩阵阶数
            self.r_num = len(self.data)
            self.c_num = c_num[0]
            self.output_data(self.data,'您输入的矩阵为:')
        else:
            print("输入错误请重新输入")
            self.data.clear()
            self.input_num()


    def revise_data(self):
        '''修改数据方法'''
        while True:
            condition = input('是否修改数据?(y/n)')
            if condition == 'n' or condition == 'N':
                break

            new_data = input('请输入\'行,列,修改后的数字\',多组数据使用\':\'隔开')
            #这里偷懒没有进行输入合法性检测
            '''使用正则表达式处理输入'''


    def transpose(self):
        '''求转置矩阵'''
        data_T = self.data[:]  #创建列表副本
        D_T = []
        for c in range(len(data_T[0])):    #避免产生index错误
            array = []
            for r in range(len(data_T)):
                array.append(data_T[r][c])
            D_T.append(array)
        return D_T


    '''矩阵的一些运算函数'''
    #暂未支持分数运算
    def exchange(self,r_num_1,r_num_2,mod='r'):
        '''行列交换'''
        r_num_1 -= 1
        r_num_2 -= 1
        '''选择模式'''
        mat = choose(self,mod)
        if mat:
            try:
                '''计算部分'''
                mat[r_num_1], mat[r_num_2] = mat[r_num_2], mat[r_num_1]

                self.data = mat

                if mod == 'c':
                    self.data = self.transpose()

                self.D_T = self.transpose()
            except IndexError:
                print(">>>IndexError")
            return 1


    def times(self,r_num,time,mod='r'):
        '''被乘函数'''
        r_num -= 1
        mat = choose(self,mod)
        if mat :
            try:
                '''计算部分'''
                for index,data in enumerate(mat[r_num][:]):
                    '''注意改变data的值不改变列表本身'''
                    data *= time
                    mat[r_num][index] = data

                self.data = mat

                if mod == 'c':
                    self.data = self.transpose()

                self.D_T = self.transpose()
            except IndexError:
                print(">>>IndexError")
            return 1


    def k_r(self,r_num_1,r_num_2,times,mod='r'):
        '''倍加行变换'''
        r_num_1 -= 1
        r_num_2 -= 1
        mat = choose(self,mod)
        if mat :
            try:
                '''计算部分'''
                if mod == 'r':
                    x = self.c_num
                else:
                    x = self.r_num
                for index in range(0,x):
                    mat[r_num_1][index] += times*mat[r_num_2][index]

                if mod == 'c':
                    self.data = self.transpose()

                self.D_T = self.transpose()
            except IndexError:
                print(">>>IndexError")
            return 1