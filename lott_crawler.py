import csv
import datetime
import itertools
import re
from urllib.error import URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

# from getlog import Logger

# 每次抓取数据周期
BALL_SCOPE = 4


class BallIndex(object):

    """find bicolor and let fore and back index"""

    def __init__(self, ftotal, btotal, flen, blen, opt):
        self.ftotal = ftotal
        self.btotal = btotal
        self.flen = flen
        self.blen = blen
        self.fore = opt[:self.flen]
        self.back = opt[-self.blen:]

    def foreIndex(self, ftotal, fore, flen):
        # 生成所有可能
        def foreAll(ftotal, flen):
            t = list(range(1, ftotal + 1))
            foreSet = list(itertools.combinations(t, flen))
            return foreSet
        foreBall = tuple(sorted(int(fore) for fore in fore))
        foreSet = foreAll(ftotal, flen)
        ind = foreSet.index(foreBall) + 1
        return ind

    def fbIndex(self):
        return self.foreIndex(self.ftotal, self.fore, self.flen), self.foreIndex(self.btotal, self.back, self.blen)


class LottBiColor(object):

    """A class that analysis lottery."""

    def __init__(self, kind, words, fname, label1, label2, label3, ftotal, btotal, flen, blen, width):
        self.kind = kind
        self.words = words
        self.fname = fname
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3
        self.ftotal = ftotal
        self.btotal = btotal
        self.flen = flen
        self.blen = blen
        self.width = width

    def foreIndex(self, ftotal, fore, flen):
        # 生成所有可能
        def foreAll(ftotal, flen):
            t = list(range(1, ftotal + 1))
            foreSet = list(itertools.combinations(t, flen))
            return foreSet
        foreBall = tuple(sorted(int(fore) for fore in fore))
        foreSet = foreAll(ftotal, flen)
        ind = foreSet.index(foreBall) + 1
        return ind

    def fbIndex(self, opt):
        fore, back = opt[:self.flen], opt[-self.blen:]
        return self.foreIndex(self.ftotal, fore, self.flen), self.foreIndex(self.btotal, back, self.blen)

    # 内部页面处理
    def get_info(self, key_word, soup):
        info_head = soup.find(text=re.compile(key_word))
        if info_head is not None:
            info_temp = info_head.parent.find_next('td')
            if info_temp is not None:
                info0 = ''.join(info_temp.text.strip())
            else:
                info0 = 'None'
            info_temp1 = info_temp.find_next('td')
            if info_temp1 is not None:
                info1 = ''.join(info_temp1.text.strip())
            else:
                info1 = 'None'
            info = [info0, info1]
        else:
            info = ['None', 'None']
        return info

    # 输出txt
    def info_set(self, output_list, txtfile, soup):
        for word in self.words:
            output = self.get_info(word, soup)
            output_list.extend(output)
        out = '\t'.join(output_list) + '\n'
        out = out.replace(',', '')
        txtfile.write(out)
        print(out[:-1])

    def get_id(self, idLast):

        # 新年如果出现系统故障时使用
        # today= datetime.datetime.strptime('20190102', '%Y%m%d').date()
        today = datetime.datetime.now().date()
        # if yesterday is new year's day, set id to xxxx001
        if today.month == 1 and today.day == 2:
            print('Happy New Year! Welcome to {}'.format(today.year))
            cop_in = [today.year * 1000 + 1]
        # else, set id to lastest 3
        else:
            print('Lastid is {}\nToday is {}'.format(idLast, today))
            cop_in = list(range(idLast + 1, idLast + BALL_SCOPE))
        return cop_in

    # snatch at data
    def parse_page(self):
        with open(self.fname, 'r+') as txtfile:
            tm = txtfile.readlines()
            idLast = int(tm[-1].split('\t')[0])
            cop_in = self.get_id(idLast)
            for cop in cop_in:
                name = str(cop)[-self.width:]
                link = "http://www.17500.cn/" + \
                    self.kind + "/details.php?issue=" + name
                output_list = [name]
                req = Request(link)
                try:
                    response = urlopen(req)
                except URLError as e:
                    if hasattr(e, 'reason'):
                        print('We failed to reach a server.')
                        print(('Reason: ', e.reason))
                    elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.')
                        print(('Error code: ', e.code))
                else:
                    # everything is fine
                    page = urlopen(link)
                    soup = BeautifulSoup(page.read().decode('gb2312'), "lxml")
                    # print soup.text
                    if '抱歉' in soup.text:
                        break
                    retemp = '20\\d\\d-\\d{2}-\\d{2}(?=' + '开奖' + ')'
                    l_date = soup.find('td', text=re.compile(retemp)).text[:-2]
                    info_ball = soup.find('td', text=self.label1)
                    if info_ball is None:
                        continue
                    else:
                        ball = info_ball.find_next('tr').text.split()
                        findex, bindex = self.fbIndex(ball)  # 产生前后球序号
                    total = soup.find(text=re.compile(self.label2))
                    if total:
                        push_in_total = total.split('：')[1][:-1]
                    else:
                        push_in_total = '0'
                    total = soup.find(text=re.compile(self.label3))
                    if total:
                        net_in_total = total.split('：')[1][:-1]
                    else:
                        net_in_total = '0'
                    output_list.append(l_date)
                    output_list.extend(ball)  # 本期球
                    output_list.extend([str(findex), str(bindex)])
                    output_list.append(push_in_total)  # 本期销售总金额
                    output_list.append(net_in_total)  # 本期奖池总金额
                    self.info_set(output_list, txtfile, soup)

    # 转换出csv
    def foutput(self):
        with open(self.fname, 'r') as txtfile:
            with open(self.fname.split('.')[0] + '.csv', 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(
                    [x[:-1].split('\t') for x in txtfile.readlines()])


def getNow():
    words = ['一等奖', '二等奖', '三等奖', '四等奖', '五等奖', '六等奖']
    kind = 'let'
    label1 = '后区号码'
    label2 = '本期销售额'
    label3 = '滚入下期奖金'
    fname = 'lett.txt'
    ftotal = 35
    btotal = 12
    flen = 5
    blen = 2
    width = 5
    lettiman = LottBiColor(kind, words, fname, label1, label2,
                           label3, ftotal, btotal, flen, blen, width)
    lettiman.parse_page()
    lettiman.foutput()
    print("Lett, that's all!")
    kind = 'ssq'
    label1 = '蓝色球'
    label2 = '投注总额为'
    label3 = '奖池金额为'
    fname = 'lott.txt'
    ftotal = 33
    btotal = 16
    flen = 6
    blen = 1
    width = 7
    lottiman = LottBiColor(kind, words, fname, label1, label2,
                           label3, ftotal, btotal, flen, blen, width)
    lottiman.parse_page()
    lottiman.foutput()
    print("Lott, that's all!")


# def makelogs():
#     # redirection
#     r_obj = Logger()
#     sys.stdout = r_obj
    
#     # redirect to console
#     r_obj.to_console()
#     # redirect to file
#     r_obj.to_file('Default.log')
#     # flush buffer
#     r_obj.flush()
#     # reset
#     r_obj.reset()


if __name__ == '__main__':
    getNow()
