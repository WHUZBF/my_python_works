'''这里存放分数数据及其处理方法'''
#注意update可能有bug
#为什么要在isinstante后面加上float判断,因为计算中可能出现float
import math


class Fraction:
    '''分数数据类'''
    def __init__(self,numerator,denominator):
        self.numerator = numerator
        self.denominator = denominator
        self.str = str(self.numerator) + '/' + str(self.denominator)
        self.simplify() #测试中
        self.update()  #更新一遍数据


    def update(self):
        '''更新数据'''
        self.str = str(int(self.numerator)) + '/' + str(int(self.denominator))  #使用int除去意外的小数因为整数相除就算是整除也会产生小数位数，这里不必考虑过多
        if self.denominator == 1:
            self.str = str(int(self.numerator))
        elif self.denominator == -1:
            self.str = str(-int(self.numerator))
        elif self.numerator == 0:
            self.str = '0'


    def gcd(self):
        '''寻找分子分母的最大公约数'''
        '''辗转相除法'''
        num_1=self.numerator
        num_2=self.denominator
        if num_1<num_2:
            num_1,num_2=num_2,num_1
        return work(num_1,num_2)     #调用函数


    def simplify(self):
        '''分数化简方法'''
        if self.denominator == self.numerator :
            self.denominator = 1
            self.numerator = 1
            self.update()
            return self
        else:
            if self.gcd() == 1 :
                self.update()
                return self
            else:
                gcd = self.gcd()   #自动传入参数self注意调用方法是要使用句点表示法,加上self,实例名
                self.numerator = int(self.numerator / gcd)
                self.denominator = int(self.denominator / gcd)
                self.update()
                return self



def multiply(frac_1,frac_2):
    '''分数乘法'''

    if isinstance(frac_1,(int,float)):
        frac_1 = Fraction(frac_1,1)
    if isinstance(frac_2,(int,float)):
        frac_2 = Fraction(frac_2,1)

    numerator = frac_1.numerator * frac_2.numerator
    denominator = frac_1.denominator * frac_2.denominator
    frac=Fraction(numerator,denominator)
    frac.simplify()
    frac.update()
    return frac


def work(p, q):
    '''计算最大公约数p>q'''
    if q == 0:
        return p
    r = p % q
    return work(q, r)


def plus_minus(frac_1,frac_2,mod=1):
    '''分数之间的加减法'''

    if isinstance(frac_1,(int,float)):
        frac_1 = Fraction(int(frac_1),1)
    elif isinstance(frac_2,(int,float)):
        frac_2 = Fraction(int(frac_2),1)

    num_1 = frac_1.denominator
    num_2 = frac_2.denominator
    if num_1 < num_2:
        num_1,num_2 = num_2,num_1
    lcm = num_1*num_2/work(num_1,num_2)
    nume = frac_1.numerator*lcm/frac_1.denominator + mod*frac_2.numerator*lcm/frac_2.denominator
    frac_3 = Fraction(nume,lcm)
    frac_3.simplify()  # 化简
    frac_3.update() #更新一下它的string值
    if frac_3.numerator == 0:   #返回零这个数
        frac_3 = 0
    return frac_3


def reciprocal(frac):
    '''求倒数'''
    if isinstance(frac,(int,float)):
        rec = Fraction(1,int(frac))
    else:
        rec = Fraction(frac.denominator,frac.numerator)
    return rec