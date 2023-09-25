import base128_decode
import correct_error_add
import self_correct
from colored import image_to_bit,bit_to_image

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
    data = input_data
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
    #    dictionary = confirm_Seven_Pro_Ten_list('1.txt')
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
    data = text
    sub_group = []
    # 17组打印
    for i in range(0, len(data), 17):
        split_sub_group = data[i:i + 17]
        arr = list(split_sub_group)
        sub_group.append(arr)

    # 最后一组如果不为17个，则从倒数第二个组获取，结合最后的数据
    end_arr = []
    # print('end arr length is: {}'.format(len(sub_group[-1])))
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
    return final_list
# step 3  00-A  10-C  01-T  11-G
def convert_data_to_dna_sequence(code):  # 11 01 11 01 11 10 00 01 00 10
    dna_seq = []
    for i in range(len(code) // 2):
        a = code[i * 2:i * 2 + 2]
        value = confirm_dna_seq_value(a)
        dna_seq.append(value)
    dna_seq_str = "".join(dna_seq)
    return dna_seq_str

def Reconstruction_image(image,error_rate):
    compressed_data, compressed_data1, compressed_data2 = image_to_bit(image)
    colord_bit = []
    colord_bit.append(compressed_data)
    colord_bit.append(compressed_data1)
    colord_bit.append(compressed_data2)
    colord_channel = []
    for three_passage in range(len(colord_bit)):
        compressed_data = colord_bit[three_passage]
        # step 2 :字典构建     将或得的数据compressed_data   加入到函数中
        dictionary = confirm_Seven_Pro_Ten_list(compressed_data)
        # step 3 ：核心编码
        final_list = core_method(compressed_data, dictionary)
        result = collating_final_code(final_list)
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
        shuju1 = shuju1[:len(compressed_data)]
        colord_channel.append(shuju1)
    # 将三通道二进制数据进行重建
    bit_to_image(image, colord_channel[0], colord_channel[1], colord_channel[2])


if __name__ == '__main__':
    Reconstruction_image("4.1.01.tiff", 0.005)













