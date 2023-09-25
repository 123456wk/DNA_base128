

import math
from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct
from skimage.metrics import structural_similarity as ssim
import cv2
import random_error_add


# 映射规则 参数：下两位二进制数据   上一位碱基   编码规则
from Other.image_encode import calculate_histogram_similarity, cosine_similarity, psnr


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
    remainder = len(dna_data)%27
    devider = int(len(dna_data)/27)

    for i in range(0 , math.ceil(len(dna_data)/27)):
        if remainder > 0 and devider == i:
            dna_data_split = dna_data[i * 27: len(dna_data)] + "AAA"
            dna_data_last = dna_data_last + dna_data_split
        else:
            dna_data_split = dna_data[i*27 : (i+1)*27] +  "AAA"
            dna_data_last =  dna_data_last + dna_data_split
    # print(dna_data_last , "dna_data_last")
    return dna_data_last , remainder , devider

#  将DNA序列转为二进制数据
def correct(DNA_data_error ):
    DNA_data_err1 = []
    for i in range(0 , len(DNA_data_error)):
        for j in range(5):
            t = 0
            if remainder > 0 and devider == i:
                binary_dna = binary_dna + DNA_data_error[t: t + remainder]
                # print(binary_data[t: t + remainder] , "binary_dna[t: t + remainder]")
            else:
                #   有效载荷发生替换错误
                if DNA_data_error[i][t + 27: t + 30] == "AAA":
                    #  注释
                    s = 1
                    binary_dna = binary_dna + DNA_data_error[i][t: t + 27]
                    t = t + 30
                    continue
                #   有效载荷发生插入错误
                if DNA_data_error[i][t + 28: t + 31]:
                    binary_dna = binary_dna + DNA_data_error[i][t: 27]
                    t = t + 31
                    continue
                #   有效载荷发生删除错误
                if binary_dna[t + 26: t + 29]:
                    binary_dna = binary_dna + DNA_data_error[i][t: 26] + "A"
                    t = t + 29
                    continue
                # "AAA"出现替换错误
                if DNA_data_error[i][t + 27: t + 30].count("A") == 2 and DNA_data_error[i][t + 57: t + 60].count("A") == 3:
                    binary_dna = binary_dna + DNA_data_error[i][t:t + 27]
                    t = t + 30
                    continue
                # "AAA"出现插入错误
                if DNA_data_error[i][t + 27: t + 31].count("A") == 3 and DNA_data_error[i][t + 58: t + 61].count("A") == 3:
                    binary_dna = binary_dna + DNA_data_error[i][t:t + 27]
                    t = t + 31
                    continue
                    #   如何记录下一个索引位置  向下易一位
                # "AAA"出现删除错误
                if DNA_data_error[i][t + 27: t + 29].count("A") == 2 and DNA_data_error[i][t + 58: t + 61].count("A") == 3:
                    binary_dna = binary_dna + DNA_data_error[i][t:t + 27]
                    t = t + 29
                    continue



def correct(DNA_data_error):
    # 最终输出的数据
    DNA_data_error
    # devider = math.ceil(len(DNA_data_error)/150)
    # remainder = len(DNA_data_error)%150
    remainder = len(DNA_data_error[-1])
    DNA_data_err1 = []
    for i in range(0 , len(DNA_data_error)):
        binary_dna = ""
        t = 0
        for j in range(5):
            if remainder > 0 and len(DNA_data_error) - 1 == i:
                #   需要做的就是   进行判断是否能被30整除，  remainder_term除数    remainder_re 余数
                remainder_term = math.ceil(remainder/30)
                remainder_re = remainder%30
                for w in range(remainder_term):
                    if remainder_term - 1 == w and remainder_re > 0:
                        binary_dna = binary_dna + DNA_data_error[i][t: remainder]
                    if DNA_data_error[i][t + 27: t + 30] == "AAA":
                        binary_dna = binary_dna + DNA_data_error[i][t: t + 27]
                        t = t + 30
                        continue
            else:
                #   有效载荷发生替换错误
                # if DNA_data_error[t + 27: t + 30] == "AAA":
                if DNA_data_error[i][t + 27: t + 30] == "AAA":
                    binary_dna = binary_dna + DNA_data_error[i][t: t + 27]
                    # binary_dna = binary_dna + DNA_data_error[t: t + 27]
                    t = t + 30
                    continue
                #   有效载荷发生插入错误
                if DNA_data_error[i][t + 28: t + 31] == "AAA":
                # if DNA_data_error[i][t + 28: t + 31] == "AAA":
                    binary_dna = binary_dna + DNA_data_error[i][t:t + 27]
                    # binary_dna = binary_dna + DNA_data_error[t: 27]
                    t = t + 31
                    continue
                #   有效载荷发生删除错误
                if DNA_data_error[t + 26: t + 29] == "AAA":
                #if DNA_data_error[i][t + 26: t + 29] == "AAA":
                    # binary_dna = binary_dna + DNA_data_error[i][t: 26] + "A"
                    binary_dna = binary_dna + DNA_data_error[i][t:t + 26] + "A"
                    t = t + 29
                    continue
                # "AAA"出现替换错误
                if DNA_data_error[t + 27: t + 30].count("A") >= 2 and DNA_data_error[t + 57: t + 60].count(
                        "A") == 3:
                #if DNA_data_error[i][t + 27: t + 30].count("A") >= 2 and DNA_data_error[i][t + 57: t + 60].count("A") == 3:
                    # binary_dna = binary_dna + DNA_data_error[i][t:t + 27]
                    binary_dna = binary_dna + DNA_data_error[t:t + 27]
                    t = t + 30
                    continue
                # "AAA"出现插入错误
                if DNA_data_error[t + 27: t + 31].count("A") >= 3 and DNA_data_error[t + 58: t + 61].count(
                        "A") == 3:
                # if DNA_data_error[i][t + 27: t + 31].count("A") >= 3 and DNA_data_error[i][t + 58: t + 61].count("A") == 3:
                    # binary_dna = binary_dna + DNA_data_error[i][t:t + 27]
                    binary_dna = binary_dna + DNA_data_error[t:t + 27]
                    t = t + 31
                    continue
                # "AAA"出现删除错误
                if DNA_data_error[t + 27: t + 29].count("A") == 2 and DNA_data_error[t + 58: t + 61].count(
                        "A") == 3:
                # if DNA_data_error[i][t + 27: t + 29].count("A") == 2 and DNA_data_error[i][t + 58: t + 61].count("A") == 3:
                    # binary_dna = binary_dna + DNA_data_error[i][t:t + 27]
                    binary_dna = binary_dna + DNA_data_error[t:t + 27]
                    t = t + 29
                    continue
                else:
                    binary_dna = binary_dna + DNA_data_error[i][t:t + 27]
                    t = t + 29
                    continue

        #  print(binary_dna , "binary_dna")
        if len(binary_dna) == 135:
            DNA_data_err1.append(binary_dna)
        elif len(binary_dna) > 135:
            DNA_data_err1.append(binary_dna[:135])
        elif 135 > len(binary_dna) > 132:
            supple = 135 - len(binary_dna)
            for i in range(supple):
                binary_dna = binary_dna + "T"
            DNA_data_err1.append(binary_dna[:135])
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
    img = Image.open('lena.bmp').convert('L')
    # img.show()
    # 转换为Numpy数组
    img_np = np.array(img)
    # 转换为一维数组
    quantized_coef_1d = img_np.flatten()
    # 一维数组转换为二进制数据
    compressed_data = ''.join([format(int(x), '08b') for x in quantized_coef_1d])

    #print(compressed_data)
    print(len(compressed_data) , "compressed_data")

    #  step  判断 该图像使用哪一种规则
    rule = 0
    odd_data = ""
    mate_data = ""
#    with open('filename.txt', 'r') as f:
#        content = f.read()
    content = compressed_data
    #  Step 1 :  判断使用那种规则
    for i in range(0 , len(content) , 2):
        odd_data = odd_data + content[i]
    for i in range(0 , len(content) , 2):
        mate_data = mate_data + content[i]
    if odd_data.count("0") > len(odd_data)/2:
        if odd_data.count("0") > len(odd_data)/2:
            rule = 0
        else:
            rule = 1
    else:
        if odd_data.count("0") > len(odd_data)/2:
            rule = 2
        else:
            rule = 3

    # step2 编码规则
    dna_data_last , remainder , devider = encode_core(content , rule)
    print(len(dna_data_last) , "原始碱基   加入三碱基   长度是291274")

    """
    # step 3  加入错误
    #  目前是错误加入
    dna_data_last1 = random_error_add.error_add(dna_data_last, 0.01)
    # 错误矫正
    #  xiugai
    dna_data_last2 = correct(dna_data_last1)
    print(len(dna_data_last2) , "纠正完的数据长度-------")

    for i in range(0 ,len(dna_data_last2)):
        if len(dna_data_last2[i]) != 135:
            print(i   , dna_data_last2[i] ,"chagndu " ,len(dna_data_last2[i]))

    dna_data_last2 = "".join(dna_data_last2)
    # print(dna_data_last2, "z最终数据")
    print(len(dna_data_last2) , "碱基的序列长度")



    #  解码过程
    binary_bit_data = decode_core(dna_data_last2 , rule)[: 524288]
    # print(binary_bit_data)
    print(len(binary_bit_data),"binary_bit_data")


    last_bit_data = binary_bit_data
    # 图像重构
    # 将二进制数据转为一维数组
    quantized_coef_1d = np.array([int(last_bit_data[i:i + 8], 2) for i in range(0, len(last_bit_data), 8)])
    # 将量化系数重构为二维数组
    quantized_coef = np.reshape(quantized_coef_1d, img_np.shape)
    quantized_coef = quantized_coef.astype(np.uint8)

    # 显示图像
    cv2.imshow('Reconstructed Image', quantized_coef)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img1 = np.array(Image.open('lena.bmp'))
    img2 = np.array(quantized_coef)
    #    img2 = np.array(Image.open('lena.bmp'))
    print(ssim(img1, img2, multichannel=True), "ssim")
    print(calculate_histogram_similarity(img1, img2, bins=256), "直方图")
    print('余弦相似度:', cosine_similarity(img1, img2))
    # print('哈希相似度:', calculate_hash_similarity(img1, img2))
    print(psnr(img1, img2) ,"psnr")
    # 将图像写出
    # cv2.imwrite('D:/image/CV2_256.jpg', img_idct)
    """






