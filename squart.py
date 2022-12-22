""""关于根式的类"""
import math
import re
from fraction import Fraction
from fraction import multiply


def factorization(num):
    """分解质因数"""
    num_seq = [1]
    while num != 1:
        k = 2
        while k<=num:
            if num%k == 0:
                num_seq.append(k)
                num/=k
                break
            k+=1
    return num_seq


class Sqrt:
    def __init__(self,num,virtual = False):
        self.virtual = virtual
        if num < 0:
            num = -num
            self.virtual = True
        self.num = int(num) # 只支持输入整形变量
        self.factor = 1
        self.str = f"{self.factor}sqrt({self.num})"
        self.value = self.factor*math.sqrt(self.num)
        self.simplify()


    def simplify(self):
        """化简"""
        num_seq = factorization(self.num)
        num_set = set(num_seq)
        for num in num_set:
            count = num_seq.count(num)
            if count >= 2:
                divide = count//2
                self.num /= math.pow(num,count-count%2)
                self.factor *= math.pow(num,divide)
        self.update()


    def update(self):
        self.factor = int(self.factor)
        self.num = int(self.num)
        if self.factor == 1:
            self.str = f"sqrt({self.num})"
        else:
            self.str = f"{self.factor}sqrt({self.num})"
        if self.num == 1:
            self.str = self.str.replace("sqrt(1)","")  # 注意 replace 是暂时性操作
        if self.virtual:
            self.str += 'i'
        self.value = self.factor * math.sqrt(self.num)


def plus(sqrt1,sqrt2,mod = 1):
    if sqrt1.virtual != sqrt2.virtual or sqrt1.num != sqrt2.num:
        return None     #这种情况下不能约简，返回none
    else:
        sqrt =Sqrt((sqrt1.factor+mod*sqrt2.factor) ** 2 * sqrt1.num,sqrt1.virtual)
        return sqrt


def mul_sqrt(sqrt1,sqrt2):
    num = sqrt1.num * sqrt2.num
    factor = sqrt1.factor * sqrt2.factor
    sqrt = Sqrt(factor**2*num)
    return sqrt



class SqrtFraction:
    """关于带有根式的分数"""
    # 懒得重构Fraction和使用子类了
    def __init__(self,factor,sqrt):
        self.factor = factor
        self.sqrt = sqrt
        self.str = self.factor.str + ' ' + self.sqrt.str
        self.value = self.factor.value * self.sqrt.value


    def rec(self):
        """求倒数"""
        self.factor.numerator,self.factor.denominator = self.factor.denominator,self.factor.numerator
        self.factor.update()
        self.factor = multiply(self.factor,Fraction(1,self.sqrt.num))
        self.str = self.factor.str + ' ' + self.sqrt.str
        self.value = self.factor.value * self.sqrt.value


    def mul(self,SF):
        """与另一个相乘"""
        factor = multiply(self.factor,SF.factor)
        sqrt = mul_sqrt(self.sqrt,SF.sqrt)
        return SqrtFraction(factor,sqrt)


def sqrt_fraction(frac):
    """对分数进行开方运算"""
    numerator = Sqrt(frac.numerator*frac.denominator)
    factor = Fraction(numerator.factor,frac.denominator)
    sqrt = Sqrt(numerator.num)
    return SqrtFraction(factor,sqrt)