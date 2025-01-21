import csv
from bs4 import BeautifulSoup  # html解析
import requests
from lxml import etree
from xpinyin import Pinyin


def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='yuBaoTable')
    if table is None:
        print("未找到历史天气")
        return
    tbody = table.find('tbody')
    if tbody is None:
        print("未找到<tbody>标签")
        return
    data = tbody.find_all('tr')
    for tr in data:
        tds = tr.find_all('td')
        if len(tds) < 7:  # 跳过不完整的行
            continue  # 提取关键标签内容

        td_2 = tds[2].text.strip() if tds[2].text else ""
        td_3 = tds[3].text.strip() if tds[3].text else ""
        ulist.append([tds[0].string.strip(), tds[1].find('a').string.strip(),
                      td_2, td_3, tds[4].string.strip()])


def printUnivList(ulist, num):
    file_name = "历史天气记录.csv"
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)  # 对查询的城市的历史天气进行保存
        writer.writerow(["日期时间", "气温", "天气情况", "风向", "风力", "日出", "日落"])
        for i in range(num):
            u = ulist[i]
            writer.writerow(u)
            print(f"日期时间：{u[0]}\t气温：{u[1]}\t天气情况：{u[2]}\t风向：{u[3]}\t风力：{u[4]}\t日出：{u[5]}\t日落：{u[6]}")


def query_weather(str):
    print(str)
    p = Pinyin()
    result1 = p.get_pinyin(str)
    # print (result1)
    city = result1.replace('-', '')

    url = f'https://www.tianqishi.com/{city}.html'  # 到“天气史”这个网站查询天气历史
    # f12网络页面，刷新页面，请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    res_data = requests.get(url=url, headers=headers)
    # print(res_data)
    tree = etree.HTML(res_data.text)
    # print(tree)
    city = tree.xpath('//h3[@class="city-title ico"]')[0].text
    date = tree.xpath('//h3[@class="city-title ico"]//span')[0].text
    ot = tree.xpath('//div[@class="ltlTemperature"]//b')[0].text  # 室外温度
    st = tree.xpath('//div[@class="ltlTemperature"]//span')[0].text  # 体感温度
    t_type = tree.xpath('(//div[@class="box pcity"])[3]//li//a[@target="_blank"]')[0].text.split('：')[1].split('，')[0]
    all_day_t = tree.xpath('(//div[@class="box pcity"])[3]//li//a[@target="_blank"]')[0].text.split('：')[1].split('，')[
        1]
    datas = tree.xpath('//ul[@class="mt"]//li')
    values = tree.xpath('//ul[@class="mt"]//li//span')
    he = tree.xpath('(//div[@class="air-quality pd0"])[1]//font')
    suggest = tree.xpath('(//div[@class="air-quality pd0"])[2]//font')
    tianqijianbao = tree.xpath('//div[@class="jdjianjie"]//p')[0]
    history_weather(str)
    def create_list():
        list1 = [city, date, ot, st, t_type, all_day_t, datas, values, he, suggest, tianqijianbao]
        return list1

    # return create_tuple()
    print(f"【城市】{city}\n【日期】{date}\n【室外温度】{ot}\n【体感温度】{st}\n【天气情况】{t_type}\n"
          f"【全天气温】{all_day_t}")

    for i in range(len(datas)):
        print(f"【{datas[i].text}】{values[i].text}")

    print(f"【健康影响】{he[0].text}\n【建议措施】{suggest[0].text}")

    print(f"【天气简报】{tianqijianbao.text}")
    return create_list()


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
        return html
    except:
        print("爬取失败")
        return None


def history_weather(str):
    p = Pinyin()
    result1 = p.get_pinyin(str)
    # print (result1)
    city = result1.replace('-', '')
    ulist = []
    url = f'https://www.tianqishi.com/lishi/{city}.html'
    html = getHTMLText(url)
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='yuBaoTable')
    if table is None:
        print("未找到该城市历史天气")
        return
    # print(table)
    # tbody = table.find('tbody')
    # if tbody is None:
    #     print("未找到<tbody>标签")
    data = table.find_all('tr')
    # print(data)
    for tr in data:
        tds = tr.find_all('td')
        # print(len(tds))
        if len(tds) < 7:  # 跳过不完整的行
            continue

        # print(tds[3])
        td_0 = tds[0].text.strip() if tds[0].text else ""
        # print(td_0) # 天气温度
        td_1 = tds[1].text.strip() if tds[1].text else ""
        # print(td_1) # 天气温度
        td_2 = tds[2].text.strip() if tds[2].text else ""
        # print(td_2) # 天气情况 晴天
        td_3 = tds[3].text.strip() if tds[3].text else ""
        # print(td_3)
        td_4 = tds[4].text.strip() if tds[4].text else ""
        # print(td_4)
        td_5 = tds[5].text.strip() if tds[5].text else ""
        # print(td_5)
        td_6 = tds[6].text.strip() if tds[6].text else ""
        # print(td_6)

        ulist.append([td_0, td_1, td_2, td_3, td_4, td_5, td_6])
    # print(ulist)
    # 天气历史文件的保存
    file_name = "历史天气记录.csv"
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["日期时间", "气温", "天气情况", "风向", "风力", "日出", "日落"])
        for i in range(30):
            u = ulist[i]
            writer.writerow(u)
            print(f"日期时间：{u[0]}\t气温：{u[1]}\t天气情况：{u[2]}\t风向：{u[3]}\t风力：{u[4]}\t日出：{u[5]}\t日落：{u[6]}")

        # def  print_save(text,feilname):


#     print（text）
#     with open(filename,'a')as file
#         file.write(text+'/n')
#
#
# def query_weathersave(str):
#         open()
#
# def save_to_csv(ulist,num):
#     filename = '当前天气。csv'
#     with open(filename, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)  # 对查询的城市的当前天气进行保存
#         writer.writerow(["日期时间", "气温", "天气情况", "风向", "风力", "日出", "日落"])
#         for i in range(num):
#             u = ulist[i]
#             writer.writerow(u)
#             print(f"日期时间：{u[0]}\t气温：{u[1]}\t天气情况：{u[2]}\t风向：{u[3]}\t风力：{u[4]}\t日出：{u[5]}\t日落：{u[6]}")

def xunhuan():
    while True:  # 采用循环持续运行程序
        Number = int(input(
            "输入1查询当前实时天气展示\n输入2进行自定义查询\n输入3查看历史天气\n输入4退出程序\n"))  # 输入城市名称来改变所要查询的城市

        if Number == 1:
            str = ("太原")
            print("查询中...")
            query_weather(str)
            # save_to_csv(str)
            history_weather(str)
        elif Number == 2:
            str = input("请输入所要查询的城市名称：")
            print("查询中...")
            query_weather(str)
            history_weather(str)
            # save_to_csv(str)
        elif Number == 3:  # 查看天气历史
            str = input("输入所要查看城市历史天气（30天内）：")
            print("查询中...")
            history_weather(str)
        elif Number == 4:
            break  # 退出循环
        else:
            print('请按要求输入')
            continue
# xunhuan()
