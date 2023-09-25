import math
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
import random_error_add
import RS_correct
from Other.image_encode import calculate_histogram_similarity, psnr, cosine_similarity

def dic_base64(num):
    dic = []
    files = []
    with open("base64_01.txt", 'r') as file:
        a = file.readlines()
    for i in range(len(a)):
        files.append(a[i])
    for i in range(len(files)):
        files[i] = files[i][:8]
    for i in range(len(a)):
        dic.append([i , files[i]])
    return dic[num][1]

def decode_dic_base64(str):
    dic = []
    files = []
    t = 0
    with open("base64_01.txt", 'r') as file:
        a = file.readlines()
    for i in range(len(a)):
        files.append(a[i])
    for i in range(len(files)):
        files[i] = files[i][:8]
    for i in range(len(a)):
        dic.append([i , files[i]])
    for i in range(64):
        if dic[i][1]  == str:
            t = i
    return t
# 编码功能函数
def functionstoten(num):
    demical_num = int(num , 2)
    bit_num = dic_base64(demical_num)
    bit_num = bit_num.zfill(8)
    # print(bit_num , "均衡码")
    return bit_num

# 解码功能函数
def decode_functionstoten(str):
    # print(str , "str")
    bit_num = bin(decode_dic_base64(str))[2:]
    bit_num = bit_num.zfill(6)
    return bit_num

    # 00-A  10-C  01-T  11-G
def confirm_dna_seq_value(input_data):
    if input_data == '00':
        return 'A'
    elif input_data == '10':
        return 'C'
    elif input_data == '01':
        return 'T'
    elif input_data == '11':
        return 'G'
    else:
        ValueError('please input correct value!')

    #  A  00  C 10  T  01  G  11
def confirm_value_seq_dna(input_data):
    if input_data == 'A':
        return '00'
    elif input_data == 'C':
        return '10'
    elif input_data == 'T':
        return '01'
    elif input_data == 'G':
        return '11'
    else:
        ValueError('please input correct value!')
"""
step 2: 1. 将数据分割成六个一组
           将第七组数据分成三段，分别放在1 3 5末尾
           2 4 6映射成均衡码
           将数据合并在一块，通过映射规则转为碱基序列 
"""
def core_method(data):
    # 读取txt数据，切分42为1组
    #将所有数据分割成42个元素一组
    sub_group = []
    # 42组打印
    for i in range(0, len(data), 42):
        split_sub_group = data[i:i + 42]
        arr = list(split_sub_group)
        sub_group.append(arr)
    # 最后一组如果不为42个，则从倒数第二个组获取，结合最后的数据
    # print(sub_group)
    end_arr = []
    if len(sub_group[-1]) % 42 > 0:
        end_sec_arr_list = sub_group[-2]
        end_sec_arr_data = end_sec_arr_list[len(sub_group[-1]):42]
        for i in range(len(sub_group[-1])):
            index = i
            end_sec_arr_data.append(sub_group[-1][index])
        end_arr = end_sec_arr_data
    sub_group[-1] = end_arr
# 将所有的42组 序列进行编码
    final_String = ""
    for i in range(len(sub_group)):
        dataString = "".join(sub_group[i])
        # print(dataString , "dataString ")
        sub_Mingroup = []
        for j in range(0, 42, 6):
            split_sub_Mingroup = dataString[j:j + 6]
            arr = list(split_sub_Mingroup)
            sub_Mingroup.append(arr)
        sub_Mingroup[0] = sub_Mingroup[0] + sub_Mingroup[6][0:2]
        sub_Mingroup[2] = sub_Mingroup[2] + sub_Mingroup[6][2:4]
        sub_Mingroup[4] = sub_Mingroup[4] + sub_Mingroup[6][4:6]
        # 将2 4 6映射成均衡码
        sub_Mingroup[1] = list(functionstoten("".join(sub_Mingroup[1])))
        sub_Mingroup[3] = list(functionstoten("".join(sub_Mingroup[3])))
        sub_Mingroup[5] = list(functionstoten("".join(sub_Mingroup[5])))

        # 合并所有数据
        final1 = ""
        Odd = "".join(sub_Mingroup[1])  + "".join(sub_Mingroup[3])  + "".join(sub_Mingroup[5])
        Mate = "".join(sub_Mingroup[0])  + "".join(sub_Mingroup[2])  + "".join(sub_Mingroup[4])
        for i in range(len(Odd)):
            final1 = final1 + Odd[i] + Mate[i]
        for i in range(len(Odd)):
            final_String = final_String + Odd[i] + Mate[i]
    return final_String
def merge_data(final_data1):
    final_data_last = []
    sum1 = len(final_data1[-2])*2
    final_data = ""
    # print(sum1, "------------------------------sum")
    for i in range(math.ceil(len(final_data1)/2)):
        final_data_five = ""
        remainder = len(final_data1)%2
        devider = math.floor(len(final_data1)/2)
        if i <= devider - 1:
            for j in range(2):
                final_data_five = final_data_five + "".join(final_data1[i*2 + j])
        if i == math.ceil(len(final_data1)/5) - 1 and remainder > 0:
            for j in range(remainder):
                final_data_five = final_data_five + "".join(final_data1[i * 4 + j])
        if len(final_data_five) > sum1:
            final_data_five = final_data_five[ : sum1]
            final_data_last.append(final_data_five)
        if len(final_data_five) < sum1:
            length = sum1 - len(final_data_five)
            for t in range(length):
                final_data_five = final_data_five + "A"
            final_data_last.append(final_data_five)
        #print(final_data_five  , "final_data_five")
        final_data  = final_data + final_data_five
    return final_data

def decode_core(data):
    # 42组打印
    sub_group = []
    for i in range(0, len(data), 48):
        split_sub_group = data[i:i + 48]
        arr = list(split_sub_group)
        sub_group.append(arr)
    # 最后一组如果不为42个，则从倒数第二个组获取，结合最后的数据
    # print(sub_group)
    end_arr = []
    #    print('end arr length is: {}'.format(len(sub_group[-1])))
    if len(sub_group[-1]) % 48 > 0:
        end_sec_arr_list = sub_group[-2]
        end_sec_arr_data = end_sec_arr_list[len(sub_group[-1]):48]
        for i in range(len(sub_group[-1])):
            index = i
            end_sec_arr_data.append(sub_group[-1][index])
        end_arr = end_sec_arr_data
    sub_group[-1] = end_arr
    # 将所有的42组 序列进行编码
    final_String = ""
    for i in range(len(sub_group)):
        Odd = ""
        Mate = ""
        dataString = "".join(sub_group[i])
        # print(dataString , i ,"dataString " , len(dataString))
        for j in range(0,len(dataString) ,2):
            Odd = Odd + dataString[j]
            Mate = Mate + dataString[j + 1]
        sub_seven = Mate[6:8] + Mate[14:16] + Mate[22:24]
        str_Odd1 = decode_functionstoten(Odd[0:8])
        str_Odd2 = decode_functionstoten(Odd[8:16])
        str_Odd3 = decode_functionstoten(Odd[16:24])
        str_Mate1 = Mate[0:6]
        str_Mate2 = Mate[8:14]
        str_Mate3 = Mate[16:22]
        final_String = final_String + str_Mate1 + str_Odd1 + str_Mate2 + str_Odd2 + str_Mate3 + str_Odd3 + sub_seven
    return final_String
def write_to_txt(data, filename):
    with open(filename, "w") as file:
        file.write(data)
# 参数传递   image   错误率   以及重建后的图像名称



if __name__ == '__main__':
    # 图像读取
    img = Image.open('5.1.13.tiff').convert('L')
    #img = Image.open('lena.bmp').convert('L')
    # 转换为Numpy数组
    img_np = np.array(img)
    # 转换为一维数组
    quantized_coef_1d = img_np.flatten()
    # 一维数组转换为二进制数据
    compressed_data = ''.join([format(int(x), '08b') for x in quantized_coef_1d])
    data = compressed_data
    # step 2 :在图像中随机加入错误
    # 编码模块
    final_data = ""
    final_list = core_method(data)
    for i in range(0 ,len(final_list) - 1 ,2):
        dataTwo = final_list[i] + final_list[i+1]
        final_data = final_data + confirm_dna_seq_value(dataTwo)
        i = i + 2
    # 错误加入模块
    final_data1 =  random_error_add.error_add(final_data, 0.004)
    final_data_last = merge_data(final_data1)
    #  解码核心
    final_bit_data = ""
    final_bit_data_split = ""
    for i in range(0,len(final_data_last)):
        final_bit_data_split = confirm_value_seq_dna(final_data_last[i])
        final_bit_data = final_bit_data + final_bit_data_split
    last_bit = decode_core(final_bit_data)
    # RS错误矫正模块
    last_bit = RS_correct.show__example(compressed_data , last_bit)
    last_bit_data = last_bit[:524288]
    # write_to_txt(last_bit_data, 'D:/image/lena_0.001.txt')
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
    img1 = np.array(Image.open('5.1.13.tiff'))
    img2 = np.array(quantized_coef)
    quantized_coef = Image.fromarray(quantized_coef)
    quantized_coef.save("base640.01.jpg")
    mse = np.mean((img1 - img2) ** 2)
    print(mse, "mse")
    print(ssim(img1, img2, multichannel=True), "ssim")
    print(calculate_histogram_similarity(img1, img2, bins=256), "直方图")
    print('余弦相似度:', cosine_similarity(img1, img2))
    # print('哈希相似度:', calculate_hash_similarity(img1, img2))
    print(psnr(img1, img2), "psnr")
