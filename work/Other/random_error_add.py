import math
import  random
import numpy
from PIL import Image
import numpy as np

"""
默认数据整体是列表，列表的单个元素是string
step 1 ：计算出错误碱基数量
step 2 : 得出发生错误的序列位置（进行判断）
step 3 ：从错误序列遍历出   替换错误  插入错误和删除错误
step 4 ：进行错误插入
"""
# step 1 : 计算出错误碱基数量   data待传输的数据量
# 0.1% 的错误
def error_add(data1 , rate ):
    #  数据转为 150长度
    data = []
    for i in range(0 , len(data1) ,150):
        Mate1_MinGroup = data1[i:i + 150]
        data.append(Mate1_MinGroup)

    #count_Correct  = math.ceil(32776*0.001)
    count_Correct  = math.ceil(len(data1)*rate)
    print(count_Correct)

    #  step 2 : 发生错误的序列位置
    count_Correct_index = []
    i = 0
    # 对所有的进行遍历
    while i < count_Correct :
        count_MinGroup = 0
    #    Random_index = random.choice(len(data))
        Random_index = random.randrange(0 , len(data1) - 300)
        Random_index_left = Random_index//150
        Random_index_right = Random_index%150
        if len(count_Correct_index) == 0:
            i = i + 1
            count_Correct_index.append([Random_index, Random_index_left, Random_index_right])
        if len(count_Correct_index) != 0 and  Random_index_right != 0:
            #单个随机与列表中随机的索引进行遍历，判断出是否符合
            for j in range(len(count_Correct_index)):
                if Random_index_left != count_Correct_index[j][1]:
                    count_MinGroup = count_MinGroup + 1
                # 如果left在一行中，进行下面判断
                if Random_index_left == count_Correct_index[j][1]:
                    if Random_index_right < 70 and count_Correct_index[j][2] >= Random_index_right + 70:
                        count_MinGroup = count_MinGroup + 1
                    elif Random_index_right >= 80 and count_Correct_index[j][2] <= Random_index_right - 70:
                        count_MinGroup = count_MinGroup + 1
                    else:
                        if count_Correct_index[j][2] >= Random_index_right + 70 and count_Correct_index[j][2] <= Random_index_right - 70:
                            count_MinGroup = count_MinGroup + 1
            if len(count_Correct_index) == count_MinGroup:
                i = i + 1
                count_Correct_index.append([Random_index, Random_index_left, Random_index_right])
        count_Correct_index.sort()

    # step 3: 从错误碱基位置中遍历出替换 插入和删除的错误     替换错误占比80%  插入占比10%  删除占比10%,  其中数据都是list类型
    count_Correct_index1 = count_Correct_index
    print(len(count_Correct_index1) , "len(count_Correct_index1)")

    print(int(count_Correct * 0.1) , "int(count_Correct * 0.1)")
    count_insert_Correct = random.sample(count_Correct_index1 , int(count_Correct * 0.1))
    # 插入方面逻辑
    for i in range(len(count_insert_Correct)):
        j = 0
        t = 0
        while t == 0:
            if count_Correct_index1[j] == count_insert_Correct[i]:
                count_Correct_index1.pop(j)
                t = t + 1
            else:
                j = j + 1
    print(len(count_Correct_index1) ,"count_Correct_index1")

    # 删除方面的错误
    count_delete_Correct = random.sample(count_Correct_index1 , int(count_Correct * 0.1))
    for i in range(len(count_delete_Correct)):
        j = 0
        t = 0
        while t == 0:
            if count_Correct_index1[j] == count_delete_Correct[i]:
                count_Correct_index1.pop(j)
                t = t + 1
            else:
                j = j + 1
    print(len(count_Correct_index1) ,"count_Correct_index2  ------")
    # 替换方面的错误
    count_sub_Correct = random.sample(count_Correct_index1 , int(count_Correct * 0.8))

    #  step 4 进行错误的插入
    #  (1) 插入错误
    for i in range(len(count_insert_Correct)):
        string_list_cache = []
        #count_insert_Correct[i][1]) 行索引      count_insert_Correct[i][2]  列索引
        if count_insert_Correct[i][2] == 0:
            string_list_cache = list(data[int(count_insert_Correct[i][1]) - 1])
            string_list_cache.insert(149, random.choice(['A', 'C', 'G', 'T']))
        else:
            string_list_cache = list(data[int(count_insert_Correct[i][1])])
            string_list_cache.insert(int(count_insert_Correct[i][2] - 1), random.choice(['A', 'C', 'G', 'T']))
        data[int(count_insert_Correct[i][1])] = "".join(string_list_cache)

    # （2）删除错误
    for i in range(len(count_delete_Correct)):
        string_list_cache = []
        #count_insert_Correct[i][1]) 行索引      count_insert_Correct[i][2]  列索引
        if count_delete_Correct[i][2] == 0:
            string_list_cache = list(data[int(count_delete_Correct[i][1]) - 1])


            #   删除错误的索引
            # print(string_list_cache)
            string_list_cache.pop(len(string_list_cache) - 1 )
        else:
            string_list_cache = list(data[int(count_delete_Correct[i][1])])
            string_list_cache.pop(int(count_delete_Correct[i][2] - 1))
        data[int(count_delete_Correct[i][1])] = "".join(string_list_cache)
    # (3) 替换错误
    #  基本逻辑： 1 找出当前位置的单个序列    2 通过分析那句代码进行重新赋值就好了
    for i in range(len(count_sub_Correct)):
        string_list_cache = []
        if count_sub_Correct[i][2] == 0:
            string_list_cache = list(data[int(count_sub_Correct[i][1]) - 1])
            sub_minDNA = string_list_cache[len(string_list_cache) - 1]
            string_list_cache[len(string_list_cache) - 1] = random.choice(list(filter(lambda nucleotide: nucleotide != sub_minDNA, ['A', 'C', 'G', 'T'])))
        else:
            string_list_cache = list(data[int(count_sub_Correct[i][1])])
            sub_minDNA = string_list_cache[int(count_sub_Correct[i][2] - 1)]
            string_list_cache[int(count_sub_Correct[i][2] - 1)] = random.choice(list(filter(lambda nucleotide: nucleotide != sub_minDNA, ['A', 'C', 'G', 'T'])))
        data[int(count_sub_Correct[i][1])] = "".join(string_list_cache)

    count_insert_Correct.sort()
    count_delete_Correct.sort()
    count_sub_Correct.sort()
    return  data

























