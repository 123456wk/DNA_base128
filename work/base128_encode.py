from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
from Other.image_encode import calculate_histogram_similarity, cosine_similarity, psnr
import base128_decode
import correct_error_add
import self_correct
def write_list_to_txt(data, filename):
    with open(filename, "w") as file:
        for item in data:
            file.write(str(item) + "\n")


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

# 整理结果数据
def collating_final_code(f_list):
    final_arr = []
    for idx in range(len(f_list)):
        final_code = f_list[idx]
        f_c_arr = []
        for idy in range(len(final_code)):
            f_c = str(final_code[idy])
            f_c_arr.append(f_c)
            code_s = "".join(f_c_arr)
        final_arr.append(code_s)
    return final_arr

# 字典构建
def confirm_Seven_Pro_Ten_list(input_data):
    #  文件传过来数据   字符串类型
    data  = input_data
    i = 0
    sumSep = 0

    # 将十进制转为7位二进制
    seq_Sev = []
    for x in range(0, 128):
        a = x
        a = bin(x)  # 将数据转化为二进制的函数
        a = a[2:]  # 从第三位开始取数据
        seq_Sev.append(a.zfill(7))
    #    print(seq_Sev[x])
    a = [0] * 128
    while i <= len(data):
        for t in range(128):
            if seq_Sev[t] == str(data[i + 10: i + 17]):
                a[t] = int(a[t]) + 1
        i = i + 17
    #  上面数据 生成七位的二进制数据和出现在数据集中的概率
    # 将生成的两位列表，按照概率的高的进行排序
    dictionary = list()
    for i in range(len(seq_Sev)):
        dictionary.append([int(seq_Sev[i]), int(a[i])])
    dictionary.sort(key=lambda x: x[1], reverse=True)
    # 读取含有约束的均衡码
    with open("01Blance.txt", "r") as file:
        data = file.readlines()
    # 将01均衡码纳入列表中
    data1 = list()
    for i in range(len(data)):
        if i % 2 != 0:
            data1.append(data[i][:10])
    for i in range(len(dictionary)):
        dictionary[i].append(data1[i])
    return dictionary

#   七进制映射成十进制函数
def functions_to_ten(num, dictionary):
    string1 = ""
    for i in range(len(dictionary)):
        if int(num) == dictionary[i][0]:
            string1 = str(dictionary[i][2]).zfill(10)
            return string1
'''
step 2
（1）将数据分割成17个一组,%17≠0，
（2）后7个通过映射函数映射为十进制均衡码
（3）均衡码与前10个数据异或，获得离散数据
（4）均衡码与离散数据合成最终数据  交叉
'''
def core_method(text, dictionary):
    # 读取txt数据，切分17为1组
    data = text
    sub_group = []
    # 17组打印
    for i in range(0, len(data), 17):
        split_sub_group = data[i:i + 17]
        arr = list(split_sub_group)
        sub_group.append(arr)
    end_arr = []
    if len(sub_group[-1]) % 17 > 0:
        end_sec_arr_list = sub_group[-2]
        end_sec_arr_data = end_sec_arr_list[len(sub_group[-1]):17]
        for i in range(len(sub_group[-1])):
            index = i
            end_sec_arr_data.append(sub_group[-1][index])
        end_arr = end_sec_arr_data
    sub_group[-1] = end_arr
    # 每个组，后7个数据通过映射函数映射为十进制均衡码
    equilibrium_arr = []
    for idx in range(len(sub_group)):
        sub_data = sub_group[idx]
        back_seven_data = sub_data[-7:]
        str_back_seven_data = "".join(back_seven_data)
        #  调用函数将七位数据映射成十进制数据
        equilibrium_code = functions_to_ten(str_back_seven_data, dictionary)
        equilibrium_arr.append(equilibrium_code)
    # 每个组，前10个数据与后7个生成的均衡码进行异或操作
    discrete_arr = []
    for idx in range(len(sub_group)):
        # 均衡码
        eq_code = equilibrium_arr[idx]
        # 获取每组前10数据
        sub_data = sub_group[idx]
        sub_for_ten_data = sub_data[:10]
        discrete_arr.append(sub_for_ten_data)
        str_for_ten_data = "".join(sub_for_ten_data)
    # 均衡码与离散数据合成最终数据
    final_list = []
    for idx in range(len(equilibrium_arr)):
        d_code = equilibrium_arr[idx]
        e_code = discrete_arr[idx]
        final_code = []
        for idy in range(len(e_code)):
            e = d_code[idy]
            final_code.append(int(e))
            d = e_code[idy]
            final_code.append(d)
        final_list.append(final_code)
    # print(final_list)
    return final_list
'''
step 3
00-A  10-C  01-T  11-G
'''
def convert_data_to_dna_sequence(code):  # 11 01 11 01 11 10 00 01 00 10
    dna_seq = []
    for i in range(len(code) // 2):
        a = code[i * 2:i * 2 + 2]
        value = confirm_dna_seq_value(a)
        dna_seq.append(value)
    dna_seq_str = "".join(dna_seq)
    return dna_seq_str

def Reconstruct_Image(image, error_rate):
    # step 1 : 图像转为二进制数据
    img = Image.open(image).convert('L')
    # 转换为Numpy数组
    img_np = np.array(img)
    # 转换为一维数组
    quantized_coef_1d = img_np.flatten()
    # 一维数组转换为二进制数据
    compressed_data = ''.join([format(int(x), '08b') for x in quantized_coef_1d])
    # step 2 :字典构建     将或得的数据compressed_data   加入到函数中
    dictionary = confirm_Seven_Pro_Ten_list(compressed_data)
    # step 3 ：核心编码
    final_list = core_method(compressed_data, dictionary)
    # 整理结果
    result = collating_final_code(final_list)
    # 还原为最终DNA序列
    get_dna_seq = ""
    for idx in range(len(result)):
        res = result[idx]
        get_dna_seq = str(get_dna_seq) + str(convert_data_to_dna_sequence(res))
    data = correct_error_add.error_add(get_dna_seq, error_rate)
    data = self_correct.drift_correct(data, dictionary)
    shuju = base128_decode.decode_core_method(data, dictionary)
    shuju1 = ""
    for i in range(len(shuju)):
        shuju1 = shuju1 + "".join(shuju[i])
    # 图像重建部分
    binary_bit_data = shuju1[:len(compressed_data)]
    last_bit_data = binary_bit_data
    # 图像重构  将二进制数据转为一维数组
    quantized_coef_1d = np.array([int(last_bit_data[i:i + 8], 2) for i in range(0, len(last_bit_data), 8)])
    quantized_coef = np.reshape(quantized_coef_1d, img_np.shape)
    quantized_coef = quantized_coef.astype(np.uint8)
    # 显示图像
    cv2.imshow('Reconstructed Image', quantized_coef)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img1 = np.array(Image.open('lena.bmp'))
    img2 = np.array(quantized_coef)
    quantized_coef = Image.fromarray(quantized_coef)
    quantized_coef.save("base128_ex_0.0025.jpg")
    #    img2 = np.array(Image.open('lena.bmp'))
    mse = np.mean((img1 - img2) ** 2)
    print(mse, "mse")
    print(ssim(img1, img2, multichannel=True), "ssim")
    print(calculate_histogram_similarity(img1, img2, bins=256), "直方图")
    print(psnr(img1, img2), "psnr")
if __name__ == '__main__':
    Reconstruct_Image('lena.bmp', 0.004)












