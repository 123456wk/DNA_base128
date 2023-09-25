import math
import random
import random_error_add
import RS_correct
from colored import image_to_bit,bit_to_image
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
    final_data = ""
    sum1 = len(final_data1[-2]) * 5
    #   step1 ： 将获得的数组重新分组
    for i in range(math.ceil(len(final_data1) / 5)):
        final_data_five = ""
        remainder = len(final_data1) % 5
        devider = math.floor(len(final_data1) / 5)
        if i <= devider - 1:
            for j in range(5):
                final_data_five = final_data_five + "".join(final_data1[i * 5 + j])
        if i == math.ceil(len(final_data1) / 5) - 1 and remainder > 0:
            for j in range(remainder):
                final_data_five = final_data_five + "".join(final_data1[i * 5 + j])
        if len(final_data_five) != sum1:
            print(final_data_five, len(final_data_five), "*******")
        if len(final_data_five) > sum1:
            final_data_five = final_data_five[: sum1]
        if len(final_data_five) < sum1:
            length = sum1 - len(final_data_five)
            for t in range(length):
                final_data_five = final_data_five + "A"
        final_data = final_data + final_data_five
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

def  Reconstruct_image(image, error_rate):
    # 彩色图像  step1： 彩色图像转为三通道二进制数据
    compressed_data, compressed_data1, compressed_data2 = image_to_bit(image)
    # step 2 :在图像中随机加入错误
    colord_bit = []
    colord_bit.append(compressed_data)
    colord_bit.append(compressed_data1)
    colord_bit.append(compressed_data2)
    colord_channel = []
    for three_passage in range(len(colord_bit)):
        compressed_data = colord_bit[three_passage]
        data = compressed_data
        bit_segments = []
        for i in range(0, len(data), 8):
            bit_segments.append(data[i: i + 8])
        #  编码模块
        Dna_data = encode(bit_segments)
        Dna_data_str = ''.join([''.join(sublist) for sublist in Dna_data])
        final_data1 = random_error_add.error_add(Dna_data_str, error_rate)
        final_data = ""
        #   解码
        final_data = merge_data(final_data1)
        Dna_data_list = [list(final_data[i:i + 8]) for i in range(0, len(final_data), 8)]
        bit_data = decode(Dna_data_list)
        string_data = ''.join([str(item) for sublist in bit_data for item in sublist])
        # print(string_data)  # 输出: "010101011010101000101011"
        # 错误矫正
        last_bit = RS_correct.show__example(compressed_data, string_data)
        last_bit_data = last_bit[: len(compressed_data)]
        colord_channel.append(last_bit_data)
        # 将三通道二进制数据进行重建
    bit_to_image(image, colord_channel[0], colord_channel[1], colord_channel[2])
if __name__ == '__main__':
    Reconstruct_image("4.1.01.tiff", 0.0025)




