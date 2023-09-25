import math
from PIL import Image
import numpy as np
import random
from scipy.fftpack import dct, idct
from skimage.metrics import structural_similarity as ssim
import cv2
import random_error_add
import RS_correct


# 映射规则 参数：下两位二进制数据   上一位碱基   编码规则
from Other.image_encode import calculate_histogram_similarity, cosine_similarity, psnr

def encode(bit_segments):
    carbon_options = [["A", "C"], ["G", "T"]]
    dna_sequences = []

    for segment_index, bit_segment in enumerate(bit_segments):
        dna_sequence = []
        for bit in bit_segment:
            options, window = carbon_options[int(bit)], dna_sequence[-3:]
            if len(window) == 3 and len(set(window)) == 1:
                for option in options:
                    if option != window[0]:
                        dna_sequence.append(option)
                        break
            else:
                dna_sequence.append(random.choice(options))
        dna_sequences.append(dna_sequence)
    return dna_sequences
def merge_data(final_data1):
    final_data_last = []
    sum1 = len(final_data1[-2])*2
    final_data = ""
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
def decode(dna_sequences):
    bit_segments = []
    carbon_options = [["A", "C"], ["G", "T"]]
    for sequence_index, dna_sequence in enumerate(dna_sequences):
        bit_segment = []
        for nucleotide in dna_sequence:
            for option_index, carbon_option in enumerate(carbon_options):
                if nucleotide in carbon_option:
                    bit_segment.append(option_index)

        bit_segments.append(bit_segment)
    return bit_segments
def Reconstruct_Image(image, error_rate):
    # 核心编码代码
    img = Image.open(image).convert('L')
    # img = Image.open('lena.bmp').convert('L')
    # 转换为Numpy数组
    img_np = np.array(img)
    # 转换为一维数组
    quantized_coef_1d = img_np.flatten()
    # 一维数组转换为二进制数据
    compressed_data = ''.join([format(int(x), '08b') for x in quantized_coef_1d])
    data = compressed_data
    # 将字符串数据转为 列表类型["01010101" , "10101010" ,"00101011"]
    bit_segments = []
    for i in range(0, len(data), 8):
        bit_segments.append(data[i: i + 8])
    #  编码模块
    Dna_data = encode(bit_segments)
    Dna_data_str = ''.join([''.join(sublist) for sublist in Dna_data])
    #  随机错误加入
    final_data1 = random_error_add.error_add(Dna_data_str, error_rate)
    final_data_last = merge_data(final_data1)
    Dna_data_list = [list(final_data_last[i:i + 8]) for i in range(0, len(final_data_last), 8)]
    bit_data = decode(Dna_data_list)
    #  将 list类型转为字符串类型
    # string_data = ''.join([''.join(sublist) for sublist in bit_data])
    string_data = ''.join([str(item) for sublist in bit_data for item in sublist])
    # print(string_data)  # 输出: "010101011010101000101011"
    # 错误矫正
    last_bit = RS_correct.show__example(compressed_data, string_data)
    last_bit_data = last_bit[: len(data)]
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
    img1 = np.array(Image.open(image))
    img2 = np.array(quantized_coef)
    quantized_coef = Image.fromarray(quantized_coef)
    quantized_coef.save("church_0.0025.jpg")
    mse = np.mean((img1 - img2) ** 2)
    print(mse, "mse")
    print(ssim(img1, img2, multichannel=True), "ssim")
    print(calculate_histogram_similarity(img1, img2, bins=256), "直方图")
    print('余弦相似度:', cosine_similarity(img1, img2))
    print(psnr(img1, img2), "psnr")
if __name__ == '__main__':
    Reconstruct_Image('lena.bmp', 0.004)
