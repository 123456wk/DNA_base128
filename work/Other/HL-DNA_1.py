import math
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
import random_error_add
from Other.image_encode import calculate_histogram_similarity, cosine_similarity, psnr

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
    r = 297
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
    # 加入AAA   碱基加入两个AAA
    remainder = len(dna_data)%r
    devider = int(len(dna_data) / r)
    for i in range(0, math.ceil(len(dna_data) / r)):
        if remainder > 0 and devider == i:
            dna_data_split = dna_data[i * r: len(dna_data)] + "AAA"
            dna_data_last = dna_data_last + dna_data_split
        else:
            dna_data_split = dna_data[i*r : (i+1)*r] +  "AAA"
            dna_data_last =  dna_data_last + dna_data_split
    # print(dna_data_last , "dna_data_last")
    return dna_data_last , remainder , devider
#   针对于50   进行矫正的
def correct1(DNA_data_error):
    # 最终输出的数据
    DNA_data_error
    remainder = len(DNA_data_error[-1])
    remainder1 = len(DNA_data_error[-2])
    remainder2 = remainder1 - 3
    DNA_data_err1 = []
    for i in range(0 , len(DNA_data_error)):
        binary_dna = ""
        t = 0
        for j in range(1):
            if remainder > 0 and len(DNA_data_error) - 1 == i:
                #   需要做的就是   进行判断是否能被30整除，  remainder_term除数    remainder_re 余数
                remainder_term = math.ceil(remainder/remainder2)
                remainder_re = remainder%remainder2
                for w in range(remainder_term):
                    if remainder_term - 1 == w and remainder_re > 0:
                        binary_dna = binary_dna + DNA_data_error[i][t: remainder]
                    if DNA_data_error[i][t + remainder2: t + remainder2 + 3] == "AAA":
                        binary_dna = binary_dna + DNA_data_error[i][t: t + remainder2]
                        t = t + remainder2 + 3
                        continue
            else:
                #   有效载荷发生替换错误
                # if DNA_data_error[t + 27: t + 30] == "AAA":
                if DNA_data_error[i][t + remainder2: t + remainder2 + 3] == "AAA":
                    binary_dna = binary_dna + DNA_data_error[i][t: t + remainder2]
                    t = t + remainder2 + 3
                    continue
                #   有效载荷发生插入错误
                if DNA_data_error[i][t + remainder2 + 1: t + remainder2 + 4] == "AAA":
                    binary_dna = binary_dna + DNA_data_error[i][t:t + remainder2]
                    t = t + remainder2 + 4
                    continue
                #   有效载荷发生删除错误
                if DNA_data_error[t + remainder2 - 1: t + remainder2 + 2] == "AAA":
                    binary_dna = binary_dna + DNA_data_error[i][t:t + remainder2 - 1] + "A"
                    t = t + remainder2 + 2
                    continue
                # "AAA"出现替换错误
                if DNA_data_error[t + remainder2: t + remainder2 + 3].count("A") >= 2:
                    binary_dna = binary_dna + DNA_data_error[t:t + remainder2]
                    t = t + remainder2 + 3
                    continue
                # "AAA"出现插入错误
                if DNA_data_error[t + remainder2: t + remainder2 + 4].count("A") >= 3:
                    binary_dna = binary_dna + DNA_data_error[t:t + remainder2]
                    t = t + remainder2 + 4
                    continue
                # "AAA"出现删除错误
                if DNA_data_error[t + remainder2: t + remainder2 + 2].count("A") == 2:
                    binary_dna = binary_dna + DNA_data_error[t:t + remainder2]
                    t = t + remainder2 + 2
                    continue
                else:
                    binary_dna = binary_dna + DNA_data_error[i][t:t + remainder2]
                    t = t + remainder2 + 2
                    continue
        if len(binary_dna) == remainder2:
            DNA_data_err1.append(binary_dna)
        elif len(binary_dna) > remainder2:
            DNA_data_err1.append(binary_dna[:remainder2])
        elif 147 > len(binary_dna) > remainder2 - 3:
            supple = remainder2 - len(binary_dna)
            for i in range(supple):
                binary_dna = binary_dna + "T"
            DNA_data_err1.append(binary_dna[:remainder2])
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
def Reconstruct_Image(image, error_rate):
    img = Image.open(image).convert('L')
    # 转换为Numpy数组
    img_np = np.array(img)
    # 转换为一维数组
    quantized_coef_1d = img_np.flatten()
    # 一维数组转换为二进制数据
    compressed_data = ''.join([format(int(x), '08b') for x in quantized_coef_1d])
    #  step  判断 该图像使用哪一种规则
    rule = 0
    odd_data = ""
    mate_data = ""
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
    # step 3  加入错误
    dna_data_last1 = random_error_add.error_add(dna_data_last, error_rate)

    #
    dna_data_last_3 = []
    for i in range(0 , len(dna_data_last1) ,2):
        if len(dna_data_last1) % 2 != 0 and len(dna_data_last1) == i - 1:
            dna_data_last_3.append(dna_data_last1[i - 1])
        else:
            split_1 = "".join(dna_data_last1[i]) + "".join(dna_data_last1[i+1])
            dna_data_last_3.append(split_1)
    # 错误矫正
    dna_data_last2 = correct1(dna_data_last_3)
    dna_data_last2 = "".join(dna_data_last2)
    #  解码过程
    binary_bit_data = decode_core(dna_data_last2 , rule)[: len(compressed_data)]
    last_bit_data = binary_bit_data
    # 图像重构   将二进制数据转为一维数组
    quantized_coef_1d = np.array([int(last_bit_data[i:i + 8], 2) for i in range(0, len(last_bit_data), 8)])
    # 将量化系数重构为二维数组
    quantized_coef = np.reshape(quantized_coef_1d, img_np.shape)
    quantized_coef = quantized_coef.astype(np.uint8)
    # 显示图像
    cv2.imshow('Reconstructed Image', quantized_coef)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img1 = np.array(Image.open(image))
    img2 = np.array(quantized_coef)
    mse = np.mean((img1 - img2) ** 2)
    quantized_coef = Image.fromarray(quantized_coef)
    quantized_coef.save("HL-DNA_ex_0.025.jpg")
    print(mse, "mse")
    print(ssim(img1, img2, multichannel=True), "ssim")
    print(calculate_histogram_similarity(img1, img2, bins=256), "直方图")
    print(psnr(img1, img2) ,"psnr")
if __name__ == '__main__':
    Reconstruct_Image('5.1.13.tiff', 0.004)








