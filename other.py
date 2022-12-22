def string_distance(str1, str2):
    """这个方法用递归贼慢"""
    i = len(str1)
    j = len(str2)
    if j == 0:
        return i
    elif i == 0:
        return j
    else:
        if str1[-1] != str2[-1]:
            flag = 1
        else:
            flag = 0
            # flag会在函数结束后被释放吗?
            # 根本不用像C一样提前声明变量
            # 注意python和C中索引都是[]matlab使用()
            # 千万注意切片操作左闭右开
        return min(string_distance(str1[:], str2[:-1])+1,
                   string_distance(str1[:-1], str2[:])+1,
                   string_distance(str1[:-1], str2[:-1])+flag,
                   )  # 一维数组切片后是深拷贝


def string_distance_dp(str1,str2):
    """下面是dp循环版本，对比上面的递归效率更高"""
    len1 = len(str1)
    len2 = len(str2)
    dp = [[0]*(len2+1) for _ in range(len1+1)]
    for i in range(1, len1+1):
        dp[i][0] = i
    for j in range(1, len2 + 1):
        dp[0][j] = j
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1], min(dp[i][j - 1], dp[i - 1][j])) + 1
    return dp[len1][len2]


class Doc:
    """
    专门存放文档注释的类
    """
    def flag(self):
        """
        使用exit命令可以退出程序"
        """
        ...

    def matrixs(self):
        """
        使用view_all可以查看所有的矩阵名称,使用view可以查看某个矩阵的信息,使用view_f可以查看某个数值矩阵的信息,格式为'view 矩阵名'
        输出时,会在矩阵名后使用括号标识出矩阵类型比如 A(FloatMatrix),B(BoolMatrix) 未标明即为普通矩阵
        """
        ...

    def format_len(self):
        """
        通过format命令,您可以指定输出的精度,要求计算机输出到第几位小数,格式为 'format number' number是指定的输出位数
        """
        ...

    def doc(self):
        """
        使用doc来查看所有支持的命令的详细使用方法,语法为 'doc cmd' cmd是你要查找的命令名称
        """
        ...

    def help(self):
        """
        直接在提示符中输入help,系统会自动打印使用文档到屏幕上,前提是文档要和程序在一个根目录下,作者也觉得可以废除这个命令
        """
        ...

    def save_as(self):
        """
        使用save_as命令,您可以将上次的运算结果以矩阵形式保存,方便下一次计算,注意,比如像det命令的计算结果是不支持使用save_as保存为标量矩阵的
        命令的语法为 'save_as 目标矩阵名称' 您可以任意设置一个名称来保存上一次计算的结果
        """
        ...

    def value(self):
        """
        ***要使用value命令,您必须先进入calculate_mode***
        value 命令是专用于将矩阵转换为一个数值矩阵的,其中的元素以浮点数模式存储在大型运算方面有更强劲的性能
        特别注意,目前直接使用数值矩阵进行常规运算会报错,只支持使用 f^ 来计算它的n次幂
        但是您可以使用view_f来查看数值矩阵,这时它的逆矩阵、行列式等,也会一并显示出来
        """
        ...

    def calculate(self):
        """
        进入calculate_mode后您可以使用多种多样的运算符对矩阵进行标准运算
        1.'A @ B' 计算A,B矩阵乘积
        2.'A - B' 计算A-B
        3.'A + B' 计算A+B
        4.'A ^ num' 计算A的num次方  ps:在次数很高时，由于内部计算机制会导致不稳定问题，一般次数下不受影响
        5.'A , B' 横着合并矩阵
        6.'A ; B' 竖着合并矩阵
        7.'A f^ num' 对于数值矩阵A的专属计算，计算A的n次幂
        8.'A * B' 矩阵对应元素相乘
        9.'A / B' 矩阵对应元素相除
        10.'A .+ num' 矩阵所有元素加上一个数
        11.'A .- num' 矩阵所有元素减去一个数
        12.'A .^ num' 矩阵所有元素进行n次幂操作
        13.'A .* num' 矩阵所有元素乘以一个数
        除了第七个是数值矩阵的专属,其它的计算结果都可以使用save_as保留为矩阵形式
        """
        ...

    def calculate_mode(self):
        """
        直接输入calculate_mode进入计算模式
        只有进入calculate_mode后,您才可以使用计算模式下的命令,当然define等这种常规命令不受影响
        直到您输入mode_end退出计算模式,您一直可以使用计算命令进行计算
        要进入其它模式请先退出当前模式
        """
        ...

    def draft_mode(self):
        """
        直接输入draft_mode进入草稿模式
        在草稿模式下,您需要先选择一个已经定义好的矩阵,之后您便可以使用命令交互式地操作您的矩阵,您可以直接输入mode_end退出
        每一步计算器都会输出结果到屏幕上,您依然可以使用save_mat保存每一次操作后的矩阵
        要进入其它模式请先退出当前模式
        """
        ...

    def mode_end(self):
        """
        直接输入mode_end可以退出当前模式进入常规模式
        您随时可以输入calculate_mode/draft_mode重新进入您想要进入的模式
        """
        ...

    def view_op(self):
        """
        要使用view_op您需要先进入draft_mode
        在draft_mode下直接输入view_op,程序会以最为美观的方式输出您对矩阵在草稿模式下所有做过的操作
        比如: r[1]<->r[2]表示第一行和第二行换位置
             5*r[1] 表示第一行乘五倍
             r[1] + 6*r[2] 表示把第二行乘6加到第一行上去
             类似的c代表列
        """
        ...

    def mul(self):
        """
        要使用mul您需要先进入draft_mode
        模式输入r(行)或者c(列)
        'mul 行(列) 倍数 模式' 某一行(列)乘以一个非零常数
        不支持使用小数输入倍数
        """
        ...

    def times(self):
        """
        要使用times您需要先进入draft_mode
        模式输入r(行)或者c(列)
        'times 行(列) 行(列) 倍数 模式' 后面的行(列)乘以一个非零常数加到前面去
        不支持使用小数输入倍数
        """
        ...

    def exchange(self):
        """
        要使用exchange您需要先进入draft_mode
        模式输入r(行)或者c(列)
        'exchange 行(列) 行(列) 模式' 交换两行(列)
        """
        ...

    def bool_mode(self):
        """
        使用 bool_mode 来直接进入bool模式
        在bool模式中,您可以定义布尔矩阵来进行繁琐的逻辑运算,助力您在离散数学中的学习
        现在bool模式支持以下几种运算:
        not(!),and(&),or(|),xor(^),bool_product(#),bool_power(#^)
        使用doc命令来获取更多这些运算的信息
        """
        ...