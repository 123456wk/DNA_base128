import math

import random_error_add
import RS_correct
from colored import image_to_bit,bit_to_image


def encode(bit_segments):
    first_3 = [[0, 0], [0, 1], [1, 0], [1, 1]]

    last_2 = {
        0: ["AA", "CC", "GG", "TT"],
        1: ["AC", "CG", "GT", "TA"],
        2: ["AG", "CT", "GA", "TC"],
        3: ["AT", "CA", "GC", "TG"],
    }
    dna_sequences = []
    index_base = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}
    # enumerate(bit_segments)   作用是啥   枚举函数  将list或者数组遍历到    segment_index , bit_segment
    # for segment_index, bit_segment in enumerate(bit_segments):
    for segment_index in range(len(bit_segments)):
        bit_segment = bit_segments[segment_index]
        dna_sequence = []
        for position in range(0, len(bit_segment), 8):
            carbon_piece, silicon_piece = [None] * 5, bit_segment[position: position + 8]
            for index, carbon_position in zip([0, 2, 4], [0, 1, 3]):
                split1 = str(silicon_piece[index: index + 2])
                segment = int(split1, 2)
                carbon_piece[carbon_position] = index_base.get(segment)
            for last_2_option in last_2.get(int(silicon_piece[6: 8], 2)):
                carbon_piece[2], carbon_piece[4] = last_2_option[0], last_2_option[1]
                if len(set(carbon_piece[:3])) > 1 and len(set(carbon_piece[3:])) > 1:
                    break
            dna_sequence += carbon_piece
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
    first_3 = [[0, 0], [0, 1], [1, 0], [1, 1]]
    last_2 = {
        str([0, 0]): ["AA", "CC", "GG", "TT"],
        str([0, 1]): ["AC", "CG", "GT", "TA"],
        str([1, 0]): ["AG", "CT", "GA", "TC"],
        str([1, 1]): ["AT", "CA", "GC", "TG"],
    }
    bit_segments = []
    base_index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    for sequence_index, dna_sequence in enumerate(dna_sequences):
        bit_segment = []
        for position in range(0, len(dna_sequence), 5):
            carbon_piece, silicon_piece = dna_sequence[position: position + 5], []
            for index in [0, 1, 3]:
                split = str(bin(base_index.get(carbon_piece[index]))[2:])
                split = split.zfill(2)
                bit_segment += split
            combination = carbon_piece[2] + carbon_piece[4]
            for value, options in last_2.items():
                if combination in options:
                    silicon_piece += [int(value[1]), int(value[4])]

            bit_segment += silicon_piece
            bit_segment = [str(item) for item in bit_segment]
        bit_segments.append(bit_segment)
    return bit_segments

def Reconstruct_image(image, error_rate):
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
        # 将字符串数据转为 列表类型["01010101" , "10101010" ,"00101011"]
        bit_segments = []
        for i in range(0, len(data), 8):
            bit_segments.append(data[i: i + 8])
        #  主函数
        # bit_segments = ["01010101" , "10101010" ,"00101011"]
        #  bit_segments  传递的是list数据类型，八个一组
        #  return    是[['C', 'C', 'G', 'C', 'T'], ['G', 'G', 'C', 'G', 'T'], ['A', 'G', 'A', 'G', 'T']]
        Dna_data = encode(bit_segments)
        Dna_data_str = ''.join([''.join(sublist) for sublist in Dna_data])
        #  随机错误加入
        final_data1 = random_error_add.error_add(Dna_data_str, error_rate)
        final_data = merge_data(final_data1)
        Dna_data_list = [list(final_data[i:i + 5]) for i in range(0, len(final_data), 5)]
        bit_data = decode(Dna_data_list)
        # print(decode(Dna_data))
        # decode    参数：[['C', 'C', 'G', 'C', 'T'], ['G', 'G', 'C', 'G', 'T'], ['A', 'G', 'A', 'G', 'T']]
        # return [['0', '1', '0', '1', '0', '1', 0, 1], ['1', '0', '1', '0', '1', '0', 1, 0], ['0', '0', '1', '0', '1', '0', 1, 1]]
        #  将 list类型转为字符串类型
        string_data = ''.join([''.join(sublist) for sublist in bit_data])
        # 加入纠错码
        last_bit = RS_correct.show__example(compressed_data, string_data)
        last_bit_data = last_bit[: len(compressed_data)]
        colord_channel.append(last_bit_data)
    # 将三通道二进制数据进行重建
    bit_to_image(image, colord_channel[0], colord_channel[1], colord_channel[2])

if __name__ == '__main__':
    Reconstruct_image("4.1.01.tiff", 0.005)






