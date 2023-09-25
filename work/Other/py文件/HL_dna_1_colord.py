import math
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
import random_error_add
from Other.image_encode import calculate_histogram_similarity, cosine_similarity, psnr
from colored import image_to_bit,bit_to_image

# 映射规则 参数：下两位二进制数据   上一位碱基   编码规则
def encode_map_rule(split_sub , pre_single_dna , rule):
    if rule == 0 or rule == 1:
        if pre_single_dna == "A":
            if split_sub == "00":
                pre_single_dna1 = "C"
            elif split_sub == "01":
                pre_single_dna1 = "G"
            else:
                pre_single_dna1 = "T"
            return pre_single_dna1

        if pre_single_dna == "T":
            if split_sub == "00":
                pre_single_dna1 = "A"
            elif split_sub == "01":
                pre_single_dna1 = "C"
            else:
                pre_single_dna1 = "G"
            return pre_single_dna1

        if pre_single_dna == "G":
            if split_sub == "00":
                pre_single_dna1 = "T"
            elif split_sub == "01":
                pre_single_dna1 = "A"
            else:
                pre_single_dna1 = "C"
            return pre_single_dna1

        if pre_single_dna == "C":
            if split_sub == "00":
                pre_single_dna1 = "G"
            elif split_sub == "01":
                pre_single_dna1 = "T"
            else:
                pre_single_dna1 = "A"
            return pre_single_dna1

    if rule == 2 or rule == 3:
        if pre_single_dna == "A":
            if split_sub == "10":
                pre_single_dna1 = "C"
            elif split_sub == "11":
                pre_single_dna1 = "G"
            else:
                pre_single_dna1 = "T"
            return pre_single_dna1

        if pre_single_dna == "T":
            if split_sub == "10":
                pre_single_dna1 = "A"
            elif split_sub == "11":
                pre_single_dna1 = "C"
            else:
                pre_single_dna1 = "G"
            return pre_single_dna1

        if pre_single_dna == "G":
            if split_sub == "10":
                pre_single_dna1 = "T"
            elif split_sub == "11":
                pre_single_dna1 = "A"
            else:
                pre_single_dna1 = "C"
            return pre_single_dna1

        if pre_single_dna == "C":
            if split_sub == "10":
                pre_single_dna1 = "G"
            elif split_sub == "11":
                pre_single_dna1 = "T"
            else:
                pre_single_dna1 = "A"
            return pre_single_dna1


# 解码规则
def decode_map_rule(split_sub , pre_single_dna , rule):
    if rule == 0 or rule == 1:
        if pre_single_dna == "A":
            if split_sub == "C":
                pre_single_dna1 = "00"
            elif split_sub == "G":
                pre_single_dna1 = "01"
            else:
                if rule == 0:
                    pre_single_dna1 = "10"
                if rule == 1:
                    pre_single_dna1 = "11"
            return pre_single_dna1

        if pre_single_dna == "T":
            if split_sub == "A":
                pre_single_dna1 = "00"
            elif split_sub == "C":
                pre_single_dna1 = "01"
            else:
                if rule == 0:
                    pre_single_dna1 = "10"
                if rule == 1:
                    pre_single_dna1 = "11"
            return pre_single_dna1

        if pre_single_dna == "G":
            if split_sub == "T":
                pre_single_dna1 = "00"
            elif split_sub == "A":
                pre_single_dna1 = "01"
            else:
                if rule == 0:
                    pre_single_dna1 = "10"
                if rule == 1:
                    pre_single_dna1 = "11"
            return pre_single_dna1

        if pre_single_dna == "C":
            if split_sub == "G":
                pre_single_dna1 = "00"
            elif split_sub == "T":
                pre_single_dna1 = "01"
            else:
                if rule == 0:
                    pre_single_dna1 = "10"
                if rule == 1:
                    pre_single_dna1 = "11"
            return pre_single_dna1

    if rule == 2 or rule == 3:
        if pre_single_dna == "A":
            if split_sub == "C":
                pre_single_dna1 = "10"
            elif split_sub == "G":
                pre_single_dna1 = "11"
            else:
                if rule == 2:
                    pre_single_dna1 = "00"
                if rule == 3:
                    pre_single_dna1 = "01"
            return pre_single_dna1

        if pre_single_dna == "T":
            if split_sub == "A":
                pre_single_dna1 = "10"
            elif split_sub == "C":
                pre_single_dna1 = "11"
            else:
                if rule == 2:
                    pre_single_dna1 = "00"
                if rule == 3:
                    pre_single_dna1 = "01"
            return pre_single_dna1

        if pre_single_dna == "G":
            if split_sub == "T":
                pre_single_dna1 = "10"
            elif split_sub == "A":
                pre_single_dna1 = "11"
            else:
                if rule == 2:
                    pre_single_dna1 = "00"
                if rule == 3:
                    pre_single_dna1 = "01"
            return pre_single_dna1

        if pre_single_dna == "C":
            if split_sub == "G":
                pre_single_dna1 = "10"
            elif split_sub == "T":
                pre_single_dna1 = "11"
            else:
                if rule == 2:
                    pre_single_dna1 = "00"
                if rule == 3:
                    pre_single_dna1 = "01"
            return pre_single_dna1



#  将二进制数据转为DNA序列
def encode_core(binary , rule):
    # 判断是否为0
    dna_data = ""
    if len(binary) % 2 != 0:
        binary = binary + "0"
    for i in range(0, len(binary), 2):
        # 判断索引是否是否为0
        if i == 0:
        # 最开始默认值是A
            pre_single_dna = "A"
            split_sub = binary[i: i + 2]
            # 对应规则
            single_dna = encode_map_rule(split_sub, pre_single_dna, rule)
            # print(type(rule),"rule  encode")
            dna_data = dna_data + single_dna
        else:
            split_sub = binary[i: i + 2]
            single_dna = encode_map_rule(split_sub, pre_single_dna, rule)
            pre_single_dna = single_dna
            dna_data = dna_data + single_dna
    dna_data_last = ""
    # 加入AAA   27碱基加入两个AAA

    remainder = len(dna_data)%297
    devider = int(len(dna_data) / 297)


    for i in range(0, math.ceil(len(dna_data) / 297)):
        if remainder > 0 and devider == i:
            dna_data_split = dna_data[i * 297: len(dna_data)] + "AAA"
            dna_data_last = dna_data_last + dna_data_split
        else:
            dna_data_split = dna_data[i*297 : (i+1)*297] +  "AAA"
            dna_data_last =  dna_data_last + dna_data_split
    # print(dna_data_last , "dna_data_last")
    return dna_data_last , remainder , devider


#   针对于50   进行矫正的
def correct1(DNA_data_error):
    # 最终输出的数据
    DNA_data_error
    remainder = len(DNA_data_error[-1])
    DNA_data_err1 = []
    for i in range(0 , len(DNA_data_error)):
        binary_dna = ""
        t = 0
        for j in range(1):
            if remainder > 0 and len(DNA_data_error) - 1 == i:
                #   需要做的就是   进行判断是否能被30整除，  remainder_term除数    remainder_re 余数
                remainder_term = math.ceil(remainder/297)
                remainder_re = remainder%297
                for w in range(remainder_term):
                    if remainder_term - 1 == w and remainder_re > 0:
                        binary_dna = binary_dna + DNA_data_error[i][t: remainder]
                    if DNA_data_error[i][t + 297: t + 300] == "AAA":
                        binary_dna = binary_dna + DNA_data_error[i][t: t + 297]
                        t = t + 300
                        continue
            else:
                #   有效载荷发生替换错误
                if DNA_data_error[i][t + 297: t + 300] == "AAA":
                    binary_dna = binary_dna + DNA_data_error[i][t: t + 297]
                    t = t + 3000
                    continue
                #   有效载荷发生插入错误
                if DNA_data_error[i][t + 298: t + 301] == "AAA":
                    binary_dna = binary_dna + DNA_data_error[i][t:t + 297]
                    t = t + 301
                    continue
                #   有效载荷发生删除错误
                if DNA_data_error[t + 296: t + 299] == "AAA":
                    binary_dna = binary_dna + DNA_data_error[i][t:t + 296] + "A"
                    t = t + 299
                    continue
                # "AAA"出现替换错误
                if DNA_data_error[t + 297: t + 300].count("A") >= 2:
                    binary_dna = binary_dna + DNA_data_error[t:t + 297]
                    t = t + 300
                    continue
                # "AAA"出现插入错误
                if DNA_data_error[t + 297: t + 301].count("A") >= 3:
                    binary_dna = binary_dna + DNA_data_error[t:t + 297]
                    t = t + 301
                    continue
                # "AAA"出现删除错误
                if DNA_data_error[t + 297: t + 299].count("A") == 2:
                    binary_dna = binary_dna + DNA_data_error[t:t + 297]
                    t = t + 299
                    continue
                else:
                    binary_dna = binary_dna + DNA_data_error[i][t:t + 297]
                    t = t + 299
                    continue
        if len(binary_dna) == 297:
            DNA_data_err1.append(binary_dna)
        elif len(binary_dna) > 297:
            DNA_data_err1.append(binary_dna[:297])
        elif 147 > len(binary_dna) > 294:
            supple = 297 - len(binary_dna)
            for i in range(supple):
                binary_dna = binary_dna + "T"
            DNA_data_err1.append(binary_dna[:297])
        else:
            DNA_data_err1.append(binary_dna)
    return DNA_data_err1

def decode_core(binary_dna1 , rule ):
    binary_data = binary_dna1
    binary_dna = binary_dna1
    binary_bit_data = ""
    for i in range(0, len(binary_dna)):
        if i == len(binary_dna) - 1:
            pre_single_dna = "A"
            split_two = decode_map_rule(binary_dna[len(binary_dna) - 1 - i] ,pre_single_dna , rule)
        else:
            pre_single_dna = binary_dna[len(binary_dna) - 2 - i]
            split_two = decode_map_rule(binary_dna[len(binary_dna) - 1 - i], pre_single_dna, rule)
        binary_bit_data = split_two + binary_bit_data
    return binary_bit_data

if __name__ == '__main__':


    #  step  1
    compressed_data, compressed_data1, compressed_data2 = image_to_bit("4.1.01.tiff")
    # step 2 :在图像中随机加入错误
    colord_bit = []
    colord_bit.append(compressed_data)
    colord_bit.append(compressed_data1)
    colord_bit.append(compressed_data2)
    colord_channel = []

    for three_passage in range(len(colord_bit)):
        compressed_data = colord_bit[three_passage]
        # data = compressed_data
        #  step2  判断 该图像使用哪一种规则
        rule = 0
        odd_data = ""
        mate_data = ""
        content = compressed_data
        #  Step 1 :  判断使用那种规则
        for i in range(0, len(content), 2):
            odd_data = odd_data + content[i]
        for i in range(0, len(content), 2):
            mate_data = mate_data + content[i]
        if odd_data.count("0") > len(odd_data) / 2:
            if odd_data.count("0") > len(odd_data) / 2:
                rule = 0
            else:
                rule = 1
        else:
            if odd_data.count("0") > len(odd_data) / 2:
                rule = 2
            else:
                rule = 3

        # step2 编码规则
        dna_data_last, remainder, devider = encode_core(content, rule)
        # step 3  加入错误
        #  目前是错误加入
        dna_data_last1 = random_error_add.error_add(dna_data_last, 0.01)

        #  转为三百碱基
        dna_data_last_3 = []
        for i in range(0, len(dna_data_last1), 2):
            if len(dna_data_last1) % 2 != 0 and len(dna_data_last1) == i - 1:
                dna_data_last_3.append(dna_data_last1[i - 1])
            else:
                split_300 = "".join(dna_data_last1[i]) + "".join(dna_data_last1[i + 1])
                dna_data_last_3.append(split_300)

        # 错误矫正
        dna_data_last2 = correct1(dna_data_last_3)

        for i in range(0, len(dna_data_last2)):
            # if len(dna_data_last2[i]) != 135:
            if len(dna_data_last2[i]) != 297:
                print(i, dna_data_last2[i], "chagndu ", len(dna_data_last2[i]))

        dna_data_last2 = "".join(dna_data_last2)
        # print(dna_data_last2, "z最终数据")
        print(len(dna_data_last2), "碱基的序列长度")

        #  解码过程
        binary_bit_data = decode_core(dna_data_last2, rule)[: 524288]
        colord_channel.append(binary_bit_data)
    # bit_to_image("4.1.01.tiff", colord_channel[0], colord_channel[1], colord_channel[2])







