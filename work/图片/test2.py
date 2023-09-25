def Insert_correct(Insert_String_Group ,dictionary):

    #dictionary = confirm_Seven_Pro_Ten_list('lena_data.txt')

    Insert_Group = ""
    Index_Correct = 0
    Index_000_Correct = list()
    String_Group_Cache_list = []

    Insert_Group = Insert_String_Group
    Correct_Group = []
    Index_Correct = []
    """
    开始  针对插入1的情况
    case 1：出现连续四个1的情况
    case 2：出现三个连续0的情况000
    case 3：任意情况
    """
    if Insert_Group.count("0") == 5:
        #  情况1， 出现连续四个的情况  1111
        for i in range(len(Insert_Group) - 3):
            if Insert_Group[i: i + 4] == "1111":
                # 三种情况判断
                w = 0
                for w in range(4):
                    if i == 0:
                        Correct_Group.append(Insert_Group[1: 11])
                        Index_Correct.append(i)
                    elif i == 7:
                        Correct_Group.append(Insert_Group[0: 10])
                        Index_Correct.append(i + w)
                    else:
                        Correct_Group.append(Insert_Group[0: i + w] + Insert_Group[i + w + 1: len(Insert_Group)])
                        Index_Correct.append(i + w)

                for j in range(len(Correct_Group)):
                    for q in range(len(dictionary)):
                        if int(Correct_Group[j]) == int(dictionary[q][2]) and dictionary[q][1] > 0:
                            String_Group_Cache_list.append([Index_Correct[j], Correct_Group[j], dictionary[q][1]])
                String_Group_Cache_list.sort(key=lambda x: x[2], reverse=True)
                #return String_Group_Cache_list[0][0], String_Group_Cache_list[0][1]
                if len(String_Group_Cache_list) != 0:
                    return String_Group_Cache_list[0][0], String_Group_Cache_list[0][1]
                if len(String_Group_Cache_list) == 0:
                    data_part = "1001100101"
                    data_MinIndex = 3
                    return data_MinIndex, data_part



        #  情况2    出现三个连续相等的0情况
        #  1. 判断有几个000情况   如何记住索引   2. 去除掉这些不合适的索引   3进一步排除，不满足概率和表格的   4  选取概率最大的输出
        #  Insert_Cache_list  储存所有1 索引的列表
        Insert_Cache_list = list()
        for i in range(len(Insert_Group)):
            if Insert_Group[i] == "1":
                Insert_Cache_list.append(i)
        for i in range(len(Insert_Group) - 2):
            if Insert_Group[i: i + 3] == "000":
                if i == 0 or i == 8:
                    Index_000_Correct.append(i)
                else:
                    Index_000_Correct.append(i - 1)
                    Index_000_Correct.append(i + 3)
        #   去去除掉不满足约束的索引
        #        for i in range(len(Index_000_Correct)):
        #            Insert_Cache_list.remove(Index_000_Correct[i])
        #     将所有可能正确的字符串赋值到String_Group_Cache_list
        #     Index_String_list   索引和字符串组成的列表
        Index_String_list = list()
        t = []
        for i in range(len(Insert_Cache_list)):
            t.append(Insert_Cache_list[i])
            if t[i] == 0:
                String_Group_Cache_list.append(Insert_Group[1: 11])
            elif t[i] == 10:
                String_Group_Cache_list.append(Insert_Group[0: 10])
            else:
                String_Group_Cache_list.append(Insert_Group[0: t[i]] + Insert_Group[t[i] + 1: 11])
            Index_String_list.append([int(t[i]), String_Group_Cache_list[i]])
        #  进一步去除不满足概率 和 表格的字符串
        Pop = []
        for i in range(len(Index_String_list)):
            for j in range(len(Index_000_Correct)):
                if int(Index_String_list[i][0]) == int(Index_000_Correct[j]):
                    Pop.append(i)
        if len(Pop) == 1:
            Index_String_list.pop(Pop[0])
        if len(Pop) == 2:
            Index_String_list.pop(Pop[0])
            Index_String_list.pop(Pop[1] - 1)
        #  last_Index_String_Pro_List      最后包含索引  概率最大的数据   概率
        last_Index_String_Pro_List = list()
        #  进一步去除不满足概率 和 表格的字符串, 最后筛选，
        Prob = []
        ac = 0
        for i in range(len(Index_String_list)):
            for j in range(len(dictionary)):
                if int(Index_String_list[i][1]) == int(dictionary[j][2]) and dictionary[j][1] > 0:
                    Prob.append(dictionary[j][1])
                    last_Index_String_Pro_List.append([Index_String_list[i][0], Index_String_list[i][1], Prob[ac]])
                    ac = ac + 1
        print(last_Index_String_Pro_List , "last_Index_String_Pro_List")

        #  根据概率的高低，选出最合适的，，并且输出删除位置的索引
        last_Index_String_Pro_List.sort(key=lambda x: x[2], reverse=True)
        Correct_Group = last_Index_String_Pro_List[0][1]
        Index_Correct = last_Index_String_Pro_List[0][0]
        #return Index_Correct, Correct_Group
        if len(last_Index_String_Pro_List) != 0:
            return last_Index_String_Pro_List[0][0], last_Index_String_Pro_List[0][1]
        if len(last_Index_String_Pro_List) == 0:
            data_part = "1001100101"
            data_MinIndex = 3
            return data_MinIndex, data_part

    elif Insert_Group.count("0") == 5:
        #  情况1， 出现连续四个的情况
        for i in range(len(Insert_Group) - 3):
            if Insert_Group[i: i + 4] == "0000":
                # 三种情况判断
                w = 0
                for w in range(4):
                    if i == 0:
                        Correct_Group.append(Insert_Group[1: 11])
                        Index_Correct.append(i)
                    elif i == 7:
                        Correct_Group.append(Insert_Group[0: 10])
                        Index_Correct.append(i + w)
                    else:
                        Correct_Group.append(Insert_Group[0: i + w] + Insert_Group[i + w + 1: len(Insert_Group)])
                        Index_Correct.append(i + w)

                for j in range(len(Correct_Group)):
                    for q in range(len(dictionary)):
                        if int(Correct_Group[j]) == int(dictionary[q][2]) and dictionary[q][1] > 0:
                            String_Group_Cache_list.append([Index_Correct[j], Correct_Group[j], dictionary[q][1]])
                String_Group_Cache_list.sort(key=lambda x: x[2], reverse=True)
                # return String_Group_Cache_list[0][0], String_Group_Cache_list[0][1]
                if len(String_Group_Cache_list) != 0:
                    return String_Group_Cache_list[0][0], String_Group_Cache_list[0][1]
                if len(String_Group_Cache_list) == 0:
                    data_part = "1001100101"
                    data_MinIndex = 3
                    return data_MinIndex, data_part
        #  情况2    出现三个连续相等的0情况
        #  1. 判断有几个000情况   如何记住索引   2. 去除掉这些不合适的索引   3进一步排除，不满足概率和表格的   4  选取概率最大的输出
        #  Insert_Cache_list  储存所有1 索引的列表
        Insert_Cache_list = list()
        for i in range(len(Insert_Group)):
            if Insert_Group[i] == "0":
                Insert_Cache_list.append(i)
        for i in range(len(Insert_Group) - 2):
            if Insert_Group[i: i + 3] == "111":
                if i == 0 or i == 8:
                    Index_000_Correct.append(i)
                else:
                    Index_000_Correct.append(i - 1)
                    Index_000_Correct.append(i + 3)
        #   去去除掉不满足约束的索引
        #        for i in range(len(Index_000_Correct)):
        #            Insert_Cache_list.remove(Index_000_Correct[i])
        #     将所有可能正确的字符串赋值到String_Group_Cache_list
        #     Index_String_list   索引和字符串组成的列表
        Index_String_list = list()
        t = []
        for i in range(len(Insert_Cache_list)):
            t.append(Insert_Cache_list[i])
            if t[i] == 0:
                String_Group_Cache_list.append(Insert_Group[1: 11])
            elif t[i] == 10:
                String_Group_Cache_list.append(Insert_Group[0: 10])
            else:
                Slipe = Insert_Group[0: t[i]] + Insert_Group[t[i] + 1: 11]
                String_Group_Cache_list.append(Slipe)
            Index_String_list.append([int(t[i]), String_Group_Cache_list[i]])
        #  进一步去除不满足概率 和 表格的字符串
        Index_String_list1 = Index_String_list
        Pop = []
        for i in range(len(Index_String_list)):
            for j in range(len(Index_000_Correct)):
                if int(Index_String_list[i][0]) == int(Index_000_Correct[j]):
                    Pop.append(i)
        if len(Pop) == 1:
            Index_String_list.pop(Pop[0])
        if len(Pop) == 2:
            Index_String_list.pop(Pop[0])
            Index_String_list.pop(Pop[1] - 1)
        """
        for i in range(len(Index_String_list)):
            for j in range(Pop):
                Index_String_list.pop(Pop[j])
        """
        #  last_Index_String_Pro_List      最后包含索引  概率最大的数据   概率
        last_Index_String_Pro_List = list()
        #  进一步去除不满足概率 和 表格的字符串, 最后筛选，
        Prob = []
        ac = 0
        for i in range(len(Index_String_list)):
            for j in range(len(dictionary)):

                #   修改
                # if int(Index_String_list[i][1]) == int(dictionary[j][2]) and dictionary[j][1] > 0:
                if dictionary[j][1] > 0:
                    Prob.append(dictionary[j][1])
                    last_Index_String_Pro_List.append([Index_String_list[i][0], Index_String_list[i][1], Prob[ac]])
                    ac = ac + 1
        #  根据概率的高低，选出最合适的，，并且输出删除位置的索引
        last_Index_String_Pro_List.sort(key=lambda x: x[2], reverse=True)
        Correct_Group = last_Index_String_Pro_List[0][1]
        Index_Correct = last_Index_String_Pro_List[0][0]
        # return Index_Correct, Correct_Group
        if len(last_Index_String_Pro_List) != 0:
            # return last_Index_String_Pro_List[0][1], last_Index_String_Pro_List[0][0]
            return last_Index_String_Pro_List[0][0] , last_Index_String_Pro_List[0][1]
        if len(last_Index_String_Pro_List) == 0:
            data_part = "1001100101"
            data_MinIndex = 3
            return data_MinIndex, data_part

    else:
        Index_Correct = 3
        Correct_Group = "0011001011"
        return Index_Correct, Correct_Group