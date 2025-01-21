import demo01weather


# def insert_list():

def insert_list(city):
    list1 = []
    list1 = demo01weather.query_weather(city)

    # print(tuple1)




    def insert_text_list1():
        return list1[0:5]
    def insert_text_list2():
        # tuple1 = ()
        # tuple1 = demo01weather.query_weather('太原')
        # print(tuple1[0])
        # print(tuple1[1])
        # print(tuple1[2])
        # print(tuple1[3])
        # print(tuple1[4])
        # print(tuple1[5])
        # print(tuple1[:5])
        list2 = []
        for i in range(len(list1[6])):

            list2.append(list1[6][i].text)
            list2.append(list1[7][i].text)

        # list3 = []
        # for i in range(len(list1[7])):
        #     list3.append(list1[7][i].text)

            # print(f"{tuple1[6][i].text}{tuple1[7][i].text}")
        return list2


    def insert_sum_list():
        return insert_text_list1() + insert_text_list2()
    # print(len(list1[6]))

    # print(insert_text_list2())
    # print(insert_sum_list())
    # print(insert_text_list1())
    return insert_sum_list()
    # print(list1[6][1].text)


# print(insert_list(city='太原'))
