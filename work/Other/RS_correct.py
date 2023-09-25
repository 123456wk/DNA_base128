import cv2

import generalizedreedsolo
import random
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
def main():
    show__example()


def cut(obj, sec):  # 按一定长度划分
    return [obj[i:i + sec] for i in range(0, len(obj), sec)]


def two_baseconversion(bitlist):  # 2进制转10进制
    tenbaseconversion = []
    for str_1 in bitlist:
        tenbaseconversion.append(int(str_1, 2))
    return tenbaseconversion


def to_bin(value, num):  # 十进制数据转8位2进制
    bin_chars = ""
    temp = value
    for i in range(num):
        bin_char = bin(temp % 2)[-1]
        temp = temp // 2
        bin_chars = bin_char + bin_chars
    return bin_chars.upper()  # 输出指定位宽的二进制字符串


#  调用函数
def reed_solomon_model(symbol_size, message_length):
    return generalizedreedsolo.Generalized_Reed_Solomon(symbol_size,  # 伽罗华域的指数
                                                        message_length,  # 加入校验位后的长度
                                                        field_size=2,  # 伽罗华域的底数
                                                        payload_length=36,  # 原始消息长度
                                                        p_factor=1)  # 加速因子


def disruption_model_1(length, error_rate, listvalue):  # 加入干扰
    disruptionnumber = length * error_rate  # 错误数量
    # print(listvalue)
    for i in range(int(disruptionnumber * 0.95)):
        strand = random.randint(0, len(listvalue) - 1)  # 序列随机
        location = random.randint(0, len(listvalue[strand]) - 1)  # 错误位置随机
        number = random.randint(0, 3)  # 碱基随机
        if number == 0:
            listvalue[strand][location] = 'A'  # 替换错误
        elif number == 1:
            listvalue[strand][location] = 'T'
        elif number == 2:
            listvalue[strand][location] = 'C'
        elif number == 3:
            listvalue[strand][location] = 'G'
    for j in range(int(disruptionnumber * 0.05)):
        strand = random.randint(0, len(listvalue) - 1)  # 序列随机
        location = random.randint(0, len(listvalue[strand]) - 1)  # 错误位置随机
        number_1 = random.randint(0, 3)  # 数字随机
        errortype = random.randint(1, 2)  # 错误类型随机
        if errortype == 1:  # 插入错误
            if number_1 == 0:
                listvalue[strand].insert(location, 'A')
            elif number_1 == 1:
                listvalue[strand].insert(location, 'T')
            elif number_1 == 2:
                listvalue[strand].insert(location, 'C')
            elif number_1 == 3:
                listvalue[strand].insert(location, 'G')
        elif errortype == 2:  # 删除错误
            del listvalue[strand][location]
    return listvalue


def read_txt_file(filename):
    with open(filename, "r") as file:
        content = file.read()
    return content

#   将  包含rs转化好的编码序列   和   数据直接转化的编码序列 传递过来
def calculate_histogram_similarity(img1, img2, bins):
    pass


def model_1(length, msg, binarylen, ori_base_msg, img_np=None):
    # 加入干扰 计算纠错率    base ： 包含纠错码的碱基序列    binarylen： 转化长度    ori_base_msg：原始碱基序列
    for error_rate in range(1, 2, 1):
        # dis_msg = disruption_model_1(length, error_rate * 0.01, msg)    #  错误加入
        dis_msg = msg
        # *****************纠错****************
        finalfile = []
        for dis_i in range(len(dis_msg)):
            sup_msg = ''
            for dis_j in dis_msg[dis_i]:
                if dis_j == 'A':
                    sup_msg = sup_msg + '00'
                elif dis_j == 'T':
                    sup_msg = sup_msg + '01'
                elif dis_j == 'C':
                    sup_msg = sup_msg + '10'
                elif dis_j == 'G':
                    sup_msg = sup_msg + '11'
            finalfile.append(sup_msg)
        # print(finalfile, "测试", len(finalfile))
        finalfile_ten = []
        for dis_l in finalfile:
            tempbitmsg = cut(dis_l, binarylen)
            finalfile_ten.append(two_baseconversion(tempbitmsg))
        #  print(finalfile_ten  , "finalfile_ten")
        correct = []

        #  改动地方2 ： 直接在用这块进行纠错
        for dis_m in finalfile_ten:
            model = reed_solomon_model(binarylen, len(dis_m))
            # noinspection PyBroadException
            try:
                correct.append(model.decode(dis_m))
            except Exception:
                correct.append(([]))
                # print("纠错失败的序列号:", finalfile_ten.index(dis_m))
        last_data = []
        bit_data = ""
        #  使用to_bin 将十进制数据转为二进制数据
        #for i in range(len(correct)):
            #print(correct[i], i, len(correct[i]), "--------")

        for i in range(len(correct)):
            if len(correct[i]) == 36:
                for j in range(len(correct[i])):
                    bit_data = bit_data + "".join(to_bin(correct[i][j], binarylen))
            else:
                t = 288 - len(correct[i])
                for z in range(t):
                    bit_data = bit_data + "0"
        # print(len(bit_data), "to_bin(value_1, binarylen)")
        # print(bit_data)

        # 图像重建及比对
        last_bit_data = bit_data[: 524288]
        return last_bit_data



def mapp_base(data):
    data_base = []
    for split_num in range(len(data)):
        data_base.append([])
        for i in range(0, len(data[split_num]), 2):
            if data[split_num][i:i + 2] == '00':
                data_base[split_num].append('A')
            elif data[split_num][i:i + 2] == '01':
                data_base[split_num].append('T')
            elif data[split_num][i:i + 2] == '10':
                data_base[split_num].append('C')
            elif data[split_num][i:i + 2] == '11':
                data_base[split_num].append('G')
    # print(len(data_base))
    return data_base


def error_correction_rate(error_rate, binarylen, listvalue, msg):
    base_orimsg = msg  # 原始碱基序列
    length = 0
    for base_split in base_orimsg:
        length = length + len(base_split)

    file_3 = open('temp.txt', 'a')
    file_3.seek(0)
    file_3.truncate()
    for temp_split in listvalue:
        if len(temp_split) != 0:
            for temp_value in temp_split:
                file_3.write(to_bin(temp_value, binarylen))
            file_3.write('\n')
        else:
            file_3.write('' + '\n')
    file_3.close()

    file_3 = open('temp.txt', 'r')
    data_decode = [line.strip('\n') for line in file_3.readlines()]  # 按行读取
    file_3.close()
    # print(data_decode)

    base_decode = []
    for temp_split_1 in data_decode:
        if len(temp_split_1) != 0:
            temp_list = []
            for i in range(0, len(temp_split_1), 2):
                if temp_split_1[i:i + 2] == '00':  # 映射成碱基
                    temp_list.append('A')
                elif temp_split_1[i:i + 2] == '01':
                    temp_list.append('T')
                elif temp_split_1[i:i + 2] == '10':
                    temp_list.append('C')
                elif temp_split_1[i:i + 2] == '11':
                    temp_list.append('G')
            base_decode.append(temp_list)
            # print(mapp_base(temp_split_1))
        else:
            base_decode.append([])
    # print(base_decode)

    right_num = 0
    for i in range(len(base_orimsg)):
        if len(base_orimsg[i]) >= len(base_decode[i]) and len(base_decode[i]) != 0:
            for j in range(len(base_decode[i])):
                if base_decode[i][j] == base_orimsg[i][j]:
                    right_num = right_num + 1
        elif len(base_orimsg[i]) < len(base_decode[i]):
            for k in range(len(base_orimsg[i])):
                if base_decode[i][k] == base_orimsg[i][k]:
                    right_num = right_num + 1
    c = np.abs(right_num / length)
    print('错误率:{:.1%}'.format(error_rate * 0.01), '纠错率:{:.4%}'.format(c))

    #  修改逻辑
    #  1. 将图像转为二进制数据和加入错误的数据写入TXT
    #  2. 将正确的校正码加入到错误的数据中
    #  3. 测试图像重建率


def show__example(data , data1):
    data = data[: 524288]
    data1 = data1[: 524288]
    file_1 = open('binfile1.txt', 'a')
    file_1.seek(0)
    file_1.truncate()

    # 获取文件长度
    tempbinarymsg = ''
    tempbinarymsg1 = ''
    for binstr in data:
        tempbinarymsg = tempbinarymsg + binstr
    print("2进制原始消息长度:", len(tempbinarymsg))
    # 添加部分
    for binstr1 in data1:
        tempbinarymsg1 = tempbinarymsg1 + binstr1


    # 按照八位读取
    binarylen = 0
    for i in range(2, 11):
        if len(tempbinarymsg) % i == 0 and i > binarylen:
            binarylen = i
    # 将数据分为8个一组  temp8bitmsg是列表数据类型
    temp8bitmsg = cut(tempbinarymsg, binarylen)
    temp8bitmsg1 = cut(tempbinarymsg1, binarylen)
    # print(temp8bitmsg   , "temp8bitmsg")#此处的tempbinarymsg刚好被8整除
    orimsg = two_baseconversion(temp8bitmsg)
    orimsg1 = two_baseconversion(temp8bitmsg1)
    print("10进制原始消息长度:", len(orimsg))

    temporimsg = cut(orimsg, 36)
    temporimsg1 = cut(orimsg1, 36)
    # print(temporimsg)
    test_normal_rs = reed_solomon_model(binarylen, 38)  # 生成伽罗华域模型    在本范例中，按照八位数据读取，38是一个列表的长度
    print(test_normal_rs)

    normal_msg = []
    #   normal_msg包含 rs码的十进制数据    temporimsg 不包含rs码的十进制数据
    #   通过将原始的数据文件、加入错误的文件  加入里面生成纠错码
    for templist in temporimsg:
        if len(templist) == 36:
            normal_msg.append(test_normal_rs.encode(templist))
        else:
            supplementarybit = '0' * (36 - len(templist))
            #  不够36位的补充0的个数
            templist.extend(map(int, list(supplementarybit)))
            normal_msg.append(test_normal_rs.encode(templist))  # 在这个地方加入rs后缀    test_normal_rs.encode(templist)

    #  大致逻辑  将错误的数据  加入正确的纠正码

    for i in range(len(normal_msg)):
        normal_msg[i][:36] = temporimsg1[i]

    length = 0
    for msg in normal_msg:
        length = length + len(msg)
        # 将文件加入纠错码的十进制数据转为二进制数据，并将数据写入binfile.txt
        for value_1 in msg:
            file_1.write(to_bin(value_1, binarylen))
        file_1.write('\n')
    file_1.close()

    c = np.abs((length - len(orimsg)) / length)
    # print('校验位占比:{:.4%}'.format(c))

    ori_base_msg = mapp_base(cut(tempbinarymsg, 288))  # 原始碱基序列
    # print(ori_base_msg)
    # print(len(ori_base_msg), "长度")

    file_5 = open('binfile1.txt', 'r')
    data = [line.strip('\n') for line in file_5.readlines()]  # 按行读取
    file_5.close()
    base = mapp_base(data)  # 映射成碱基
    num = 0
    for i in base:
        num = num + len(i)  # 碱基总数
    # 加入干扰 计算纠错率    base ： 包含纠错码的碱基序列    binarylen： 转化长度    ori_base_msg：原始碱基序列
    last_bit_data = model_1(num, base, binarylen, ori_base_msg)
    return last_bit_data


# if __name__ == "__main__":


