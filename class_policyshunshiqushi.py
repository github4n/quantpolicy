# @Time : 2020/4/2 1:21 
# @Author : bufeetu
# @File : class_policyma.py 
import time, datetime
import os
import requests
import json
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from class_policymodel import Policymodel
#注释完毕


class Policyshunshiqushi(Policymodel):
    def __init__(self):
        pass
    def get_zhangshu(self,isduo=True):
        zhangshu_duo = 0
        zhangshu_kong = 0
        for i in range(len(self.list_wg)):
            wg = self.list_wg[i]
            if wg['status'] == 'kong_ok':
                zhangshu_kong += wg['zhangshu_wg']
            if wg['status'] == 'duo_ok':
                zhangshu_duo += wg['zhangshu_wg']
        if isduo==True:
            return zhangshu_duo
        else:
            return zhangshu_kong
    def log_paramlist(self,content):
        content = str(content)+ '\n'
        url=os.getcwd() + '/logparamlist.txt'
        f = open(url, mode='a+')
        f.write(str(content))
        # f.write(str(content)+'        '+str(self.get_date_now()))
        f.close()
        print(content)
    def zongjie(self):
        # 资产 净利润 手续费  年化率 最大回撤 胜率 盈亏比
        # 持仓率 最低保证金率 连续盈利 连续亏损  结单次数 平均每次结单收益
        # 张数 间隔 止盈 止损
        fund=str(round(float(self.dict_acc['quanyi'])*float(self.dict_data['close']),2))
        money=str(self.dict_acc['money'])
        fee=str(self.dict_jilu['fee_sum'])
        rate_nianhua = str(self.get_nianhua(self.dict_jilu['list_rate_shouyi_fund'][-1], self.date_totimechuo('2018-09-15'), self.dict_param['timechuo_end']))
        huiche_max=str(self.dict_jilu['huiche_max'])
        res = self.get_shenglv_yingkui(self.dict_jilu['list_rate_shouyi_close'])
        rate_shenglv=str(res[0])
        rate_yingkui = str(res[1])
        rate_chicang=str(max(self.dict_jilu['list_rate_chicang']))
        rate_margin_min=str(min(self.dict_jilu['list_rate_margin']))
        res=self.get_num_lianxuyingkui(self.dict_jilu['list_rate_shouyi_close'])
        num_lianxuying=str(res[0])
        num_lianxukui=str(res[1])
        num_shouyi=str(len(self.dict_jilu['list_rate_shouyi_close']))
        aver_shouyi=str(sum(self.dict_jilu['list_rate_shouyi_close'])/len(self.dict_jilu['list_rate_shouyi_close']))
        m1=self.coinname+'|'+fund+'|'+money+'|'+fee+'|'+rate_nianhua+'|'+huiche_max+'|'+rate_shenglv+'|'+rate_yingkui
        m2='|'+rate_chicang+'|'+rate_margin_min+'|'+num_lianxuying+'|'+num_lianxukui+'|'+num_shouyi+'|'+aver_shouyi
        m3='|' + str(self.dict_param['jiange']) + '|' + str(self.dict_param['zhangshu_shun'])+ '|' + str(self.dict_param['zhangshu_ni']) + '|' + str(self.dict_param['zhiying']) + '|' + str(self.dict_param['zhisun'])+ '|' + str(self.dict_param['sleep_day'])
        m3= '|' + str(self.dict_param['zhangshu_shun'])+ '|' + str(self.dict_param['zhiying']) + '|' + str(self.dict_param['zhisun'])+ '|' + str(self.dict_param['sleep_day'])
        self.log_paramlist(m1+m2+m3)
        self.log_paramlist(self.dict_jilu['list_rate_shouyi_close'])
        self.chart_2(self.coinname+'年化'+str(rate_nianhua)+'回撤'+str(huiche_max), self.dict_jilu['list_rate_jizhun'], self.dict_jilu['list_rate_shouyi_fund'])

        # m1 = self.coinname + '资产' + fund + '利润' + money + '手续费' + fee + '年化' + rate_nianhua + '回撤' + huiche_max + '胜率' + rate_shenglv + '盈亏' + rate_yingkui
        # m2 = '持仓率' + rate_chicang + '最低保证金' + rate_margin_min + '连续盈利' + num_lianxuying + '连续亏损' + num_lianxukui + '收益次数' + num_shouyi + '平均收益' + aver_shouyi
        # m3 = '间隔' + str(self.dict_param['jiange']) + '顺势' + str(self.dict_param['zhangshu_shun']) + '逆势' + str(self.dict_param['zhangshu_ni'])  + '止盈' + str(self.dict_param['zhiying']) + '止损' + str(self.dict_param['zhisun'])+ '休眠' + str(self.dict_param['sleep_day'])
        # self.log_paramlist(m1)
        # self.log_paramlist(m2)
        # self.log_paramlist(m3)
    def wg_tocsv(self,title):
        return
        name = ['id', 'price_wg', 'zhangshu_wg','status','shouyi','rate_shouyi','rate_shouyi_max','timechuo','date']
        test = pd.DataFrame(columns=name, data=self.list_wg)  # 数据有三列，列名分别为one,two,three
        print(test)
        datem = self.timechuo_todate(self.dict_data['timechuo'])
        zhangshu_duo = self.get_zhangshu(True)
        zhangshu_kong = self.get_zhangshu(False)
        price = self.dict_data['close']
        m = '价格' + str(price) + '回撤' + str(self.dict_jilu['huiche_max']) + 'duo' + str(zhangshu_duo) + 'kong' + str(zhangshu_kong) + '本轮收益率' + str(self.dict_acc['lun_rate_shouyi'])
        test.to_csv(os.getcwd() + '/' + datem + m + title + '.csv', encoding='gbk')
    def log(self,content):
        return
        content = str(content)+'                  price='+str(self.dict_data['open'])+'    '+str(self.dict_data['date'])  + '\n'
        print(content)
        url=os.getcwd() + '/log'+self.coinname+'.txt'
        f = open(url, mode='a+')
        f.write(str(content))
        f.close()
    def log_del(self):
        url = os.getcwd() + '/log' + self.coinname + '.txt'
        if (os.path.exists(url)):
            os.remove(url)
    def close(self,price,mianzhi):
        #获取数据
        zhiying = self.dict_param['zhiying']
        huiche = self.dict_param['huiche']
        lun_direction=self.dict_acc['lun_direction']
        lun_rate_shouyi = self.dict_acc['lun_rate_shouyi']
        lun_rate_shouyi_max = self.dict_acc['lun_rate_shouyi_max']
        fee_close=self.get_fee(price,self.dict_acc['lun_zhangshu_sum'], mianzhi)
        todo=''
        if lun_rate_shouyi_max>zhiying and lun_rate_shouyi<=lun_rate_shouyi_max*(1-huiche*0.01):
            todo = '止盈'
        if lun_direction=='kong' and lun_rate_shouyi<0-abs(self.dict_param['zhisun']):
            todo = '止损空'
        if lun_direction=='duo' and  lun_rate_shouyi<0-abs(self.dict_param['zhisun']):
            todo = '止损多'
        if lun_direction=='sleep' and self.dict_data['direction']!='sleep':
            todo = '解冻'
        if todo == '止盈' or todo == '止损空' or todo == '止损多' or todo == '解冻':
            if todo == '止损空' or todo == '止损多':
                self.dict_acc['timechuo_sleep'] = int(self.dict_data['timechuo']) + 86400 * self.dict_param['sleep_day']
            self.log('整体'+todo+',收益率' + str(lun_rate_shouyi)+'初始价格'+str(self.dict_acc['lun_price_start'])+'初始资产'+str(self.dict_acc['lun_fund_start']))
            self.dict_jilu['fee_sum'] += 2 * fee_close
            self.wg_tocsv(self.coinname+todo + str(lun_rate_shouyi))
            self.list_wg.clear()
            if abs(lun_rate_shouyi)>1:
                self.dict_jilu['list_rate_shouyi_close'].append(lun_rate_shouyi)
            self.log('扣手续费之前权益'+str(self.dict_acc['quanyi']))
            self.dict_acc['quanyi']-=2*fee_close
            self.log('扣手续费之后权益'+str(self.dict_acc['quanyi']))
            # 开始卖币换钱
            if self.dict_acc['quanyi'] * price > 10000:
                num_sell = self.dict_acc['quanyi'] - (10000 / price)
                self.dict_acc['quanyi'] = round(10000 / price, 8)
                num_money = num_sell * price * 0.998
                self.dict_acc['money'] += num_money
                self.log('卖币成功,卖出数量' + str(num_sell) + '得到钱' + str(num_money) + '当前净利润' + str(self.dict_acc['money']))
        return
    def uprecord(self,price,mianzhi):
        #更新本轮收益率 本轮最大收益率 本轮最高最低价 记录
        fund = round(price * self.dict_acc['quanyi'],4)
        self.dict_jilu['fund_max'] = max(self.dict_jilu['fund_max'], fund)
        self.dict_jilu['fund_min'] = min(self.dict_jilu['fund_min'], fund)
        lun_rate_shouyi = round(fund / self.dict_acc['lun_fund_start'] * 100 - 100, 2)
        self.dict_acc['lun_rate_shouyi'] = lun_rate_shouyi
        if lun_rate_shouyi > self.dict_acc['lun_rate_shouyi_max']:
            self.dict_acc['lun_rate_shouyi_max'] = lun_rate_shouyi
            self.log('恭喜,本轮收益率达到' + str(lun_rate_shouyi))
        rate_chicang = round(self.dict_acc['lun_zhangshu_sum'] / (fund / mianzhi), 2)
        self.dict_jilu['rate_chicang_max'] = max(self.dict_jilu['rate_chicang_max'], rate_chicang)
        self.dict_acc['lun_price_high'] = max(self.dict_acc['lun_price_high'],price)
        self.dict_acc['lun_price_low'] = min(self.dict_acc['lun_price_low'],price)
        if self.dict_data['timechuo']>self.dict_jilu['timechuo_record']:
            self.dict_jilu['huiche_max'] = max(self.dict_jilu['huiche_max'],round((10000-fund) / (10000) * 100,2))
            self.dict_jilu['timechuo_record']=int(self.dict_data['timechuo'])+3600*4
            #资金收益率 币数收益率 基准率 手续费
            money=self.dict_acc['money']
            rate_shouyi_fund = round((fund+money) / self.dict_jilu['fund_start'] * 100 - 100, 2)
            rate_shouyi_coin = round((fund+money)/price / self.dict_jilu['quanyi_start'] * 100 - 100, 2)
            rate_jizhun = round(price / float(self.dict_jilu['price_start']) * 100 - 100, 2)
            rate_margin = self.get_rate_margin(price,self.dict_acc['lun_zhangshu_sum'], self.dict_acc['quanyi'], mianzhi)
            self.dict_jilu['list_rate_shouyi_fund'].append(rate_shouyi_fund)
            self.dict_jilu['list_rate_shouyi_coin'].append(rate_shouyi_coin)
            self.dict_jilu['list_rate_jizhun'].append(rate_jizhun)
            self.dict_jilu['list_rate_chicang'].append(rate_chicang)
            self.dict_jilu['list_rate_margin'].append(rate_margin)
            m1='本轮'+str(self.dict_acc['lun_direction'])+'张数'+str(self.dict_acc['lun_zhangshu_sum'])+'本轮收益率'+str(lun_rate_shouyi)+'本轮最大收益率'+str(self.dict_acc['lun_rate_shouyi_max'])
            m2 = '权益' + str(self.dict_acc['quanyi']) + '资产' + str(fund) + '净利润' + str(self.dict_acc['money']) + '手续费' + str(self.dict_jilu['fee_sum']) + '收益率' + str(rate_shouyi_fund) + '基准率' + str(rate_jizhun)
            m3 = '最大回撤' + str(self.dict_jilu['huiche_max']) + '最大持仓率' + str(max(self.dict_jilu['list_rate_chicang'])) + '最低保证金率' + str(min(self.dict_jilu['list_rate_margin']))
            m4 = '交易最低资金' + str(self.dict_jilu['fund_min']) + '最高资金' + str(self.dict_jilu['fund_max'])
            self.log(m1)
            self.log(m2)
            self.log(m3)
            self.log(m4)
    def ok(self,price,mianzhi):
        #遍历网格,更新单个收益,累计总收益,更新权益
        shouyi_sum = 0
        zhangshu_sum=0
        for i in range(len(self.list_wg)):
            wg = self.list_wg[i]
            price_wg = wg['price_wg']
            zhangshu_wg = wg['zhangshu_wg']
            status = wg['status']
            if status == 'duo_ok' or status == 'kong_ok' or status == 'chong_ok':
                if status == 'duo_ok':
                    shouyi= self.get_unsettled(price_wg, price, zhangshu_wg, mianzhi, True)
                    rate_shouyi = price / price_wg * 100 - 100
                else:
                    shouyi= self.get_unsettled(price_wg, price, zhangshu_wg, mianzhi, False)
                    rate_shouyi = 0-(price / price_wg * 100 - 100)
                self.list_wg[i]['shouyi'] = round(shouyi,2)
                self.list_wg[i]['rate_shouyi'] = round(rate_shouyi,2)
                self.list_wg[i]['rate_shouyi_max'] = max(self.list_wg[i]['rate_shouyi_max'],rate_shouyi)
                shouyi_sum += shouyi
                zhangshu_sum += zhangshu_wg
        # 更新权益
        self.dict_acc['quanyi'] = round(self.dict_acc['lun_quanyi_start'] + shouyi_sum, 8)
        self.dict_acc['lun_zhangshu_sum']=zhangshu_sum
        return
    def ing(self,high,low,mianzhi,price):
        # 遍历网格,如果duo_ing  价格跌破就成交   waitkong 涨破就成交
        for i in range(len(self.list_wg)):
            wg = self.list_wg[i]
            if wg['status'] == 'duo_ing' and low < wg['price_wg']:
                self.list_wg[i]['status'] = 'duo_ok'
                self.list_wg[i]['date'] = self.dict_data['date']
                self.log('开多成交,成交价' + str(wg['price_wg']) + '成交张数' + str(wg['zhangshu_wg']))
            if wg['status'] == 'kong_ing' and high > wg['price_wg']:
                self.list_wg[i]['status'] = 'kong_ok'
                self.list_wg[i]['date'] = self.dict_data['date']
                self.log('开空成交,成交价' + str(wg['price_wg']) + '成交张数' + str(wg['zhangshu_wg']))
        return
    def wait(self,high,low):
        #遍历网格,如果waitduo  价格超过,就委托   waitkong 跌破就委托
        for i in range(len(self.list_wg)):
            wg = self.list_wg[i]
            if wg['status']=='duo_wait' and high>wg['price_wg']:
                self.list_wg[i]['status']='duo_ing'
                # self.log('委托开多,委托价'+str(wg['price_wg'])+'委托张数'+str(wg['zhangshu_wg']))
            if wg['status']=='kong_wait' and low<wg['price_wg']:
                self.list_wg[i]['status'] = 'kong_ing'
                # self.log('委托开空,委托价'+str(wg['price_wg'])+'委托张数'+str(wg['zhangshu_wg']))
        return
    def creat(self,price,atr,mianzhi):
        self.list_wg = []
        fund=round(self.dict_acc['quanyi']*price,4)
        zhangshu_chong=int(fund/mianzhi)
        zhangshu_shun = max(round(self.dict_param['zhangshu_shun']*zhangshu_chong,2),1)
        zhangshu_ni = max(round(self.dict_param['zhangshu_ni']*zhangshu_chong,2),1)
        jiange_wg = atr * self.dict_param['jiange']
        direction=self.dict_data['direction']
        status = ''
        zhangshu_wg=0
        geshu = self.dict_param['geshu']
        for i in range(geshu * 2 + 1):
            id = i + 1
            price_wg = price + (geshu - i) * jiange_wg
            if direction == 'duo':
                status='duo_wait'
                if price_wg>price:
                    zhangshu_wg=zhangshu_shun
                else:
                    zhangshu_wg=zhangshu_ni
            elif direction == 'kong':
                status = 'kong_wait'
                if price_wg<price:
                    zhangshu_wg=zhangshu_shun
                else:
                    zhangshu_wg=zhangshu_ni
            dict_wg = {
                'id': id,
                'price_wg': round(price_wg, 3),
                'zhangshu_wg': zhangshu_wg,
                'status': status,
                'shouyi': 0,
                'rate_shouyi': 0,
                'rate_shouyi_max': 0,
                'timechuo': self.dict_data['timechuo'],
                'date': self.dict_data['date'],
            }
            #加入列表
            if i == geshu:
                dict_wg['zhangshu_wg'] = zhangshu_chong
                dict_wg['status'] = 'chong_ok'
            if (direction!='sleep' or i==geshu) and price_wg>0:
                self.list_wg.append(dict_wg)
        self.dict_acc['lun_direction'] = direction
        self.dict_acc['lun_price_start'] = price
        self.dict_acc['lun_quanyi_start'] = self.dict_acc['quanyi']
        self.dict_acc['lun_fund_start'] = self.dict_acc['quanyi'] * price
        self.dict_acc['lun_rate_shouyi'] = 0
        self.dict_acc['lun_rate_shouyi_max'] = 0
        self.dict_acc['lun_zhangshu_sum'] =0
        self.dict_acc['lun_price_high']=price
        self.dict_acc['lun_price_low']=price
        self.log('账户='+str(self.dict_acc))
        self.log('创建网格完成,总格数'+str(len(self.list_wg))+'间隔'+str(jiange_wg)+'方向'+str(direction)+'初始资产'+str(fund))
    def buy(self,price):
        quanyi = round(self.dict_jilu['fund_start'] / price, 8)
        self.dict_acc['quanyi'] = quanyi
        self.dict_jilu['price_start'] = price
        self.dict_jilu['quanyi_start'] = quanyi
        self.log('系统:购买成功.得到权益' + str(quanyi)+'初始价格'+str(self.dict_jilu['price_start'])+'初始权益'+str(self.dict_jilu['quanyi_start']))
    def run(self,open,high,low,close,atr):
        if self.dict_acc['quanyi'] == 0:
            self.buy(close)
            return
        else:
            mianzhi = self.dict_param['mianzhi']
            if self.list_wg==[]:
                self.creat(close,atr, mianzhi)
                self.log('创建网格成功')
            else:
                if len(self.list_wg)>1:
                    self.ing(high,low,mianzhi,close)
                    self.wait(high,low)
                self.ok(close,mianzhi)
                self.uprecord(close,mianzhi)
                self.close(close,mianzhi)
    def start(self,coinname,jici,param={}):
        self.coinname=str(coinname).lower()
        # 整理参数
        self.dict_param=param
        self.dict_param['jingdu']=self.get_jingdu(coinname)
        self.dict_param['mianzhi']=self.get_mianzhi(coinname)
        # 创建记录容器
        self.dict_jilu = {
            'price_start': 0,
            'quanyi_start': 0,
            'fund_start': 10000,
            'timechuo_record': 0,
            'fee_sum': 0,
            'rate_chicang_max': 0,
            'huiche_max': 0,
            'fund_max': 10000,
            'fund_min': 10000,
            'list_rate_shouyi_close': [],
            'list_rate_shouyi_fund': [],
            'list_rate_shouyi_coin': [],
            'list_rate_jizhun': [],
            'list_rate_chicang': [0],
            'list_rate_margin': [],
            'list_ma': [],
        }
        self.dict_data = {
            'date': 0,
            'timechuo': 0,
            'open': 0,
            'high': 0,
            'low': 0,
            'close': 0,
            'ma': 0,
            'atr': 0,
            'direction':'sleep'
        }
        self.dict_acc = {
            'quanyi': 0,
            'lun_direction':'',
            'lun_price_start': 0,
            'lun_quanyi_start': 0,
            'lun_fund_start': 0,
            'lun_price_high': 0,
            'lun_price_low': 0,
            'lun_rate_shouyi': 0,
            'lun_rate_shouyi_max': 0,
            'lun_zhangshu_sum': 0,
            'money': 0,
            'timechuo_sleep':0,
        }
        self.list_wg = []
        self.log_del()
        # 遍历数据
        df = pd.read_csv('../kline/1m_' + coinname + 'usdt.csv')
        print('./kline/1m_' + coinname + 'usdt.csv')
        for idx, row in df.iterrows():
            #记录ma列表
            if len(self.dict_jilu['list_ma'])==0:
                self.dict_jilu['list_ma'].append(float(row['ma91']))
            if self.dict_jilu['list_ma'][-1]!=float(row['ma91']):
                self.dict_jilu['list_ma'].append(float(row['ma91']))
            self.dict_data = {
                'date': str(row['date']),
                'timechuo': int(row['timechuo']),
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'ma': float(row['ma91']),
                'atr': float(row['atr']),
                'direction':self.get_direction_qushi(float(row['close']),float(row['ma91']),self.dict_jilu['list_ma'])
            }
            if int(row['timechuo'])<self.dict_acc['timechuo_sleep']:
                self.dict_data['direction']='sleep'
            if int(row['timechuo']) > self.date_totimechuo('2019-01-01') and self.dict_jilu['list_rate_shouyi_fund'][-1]<5:
                self.log_paramlist(str(jici)+'失败!收益'+str(self.dict_jilu['list_rate_shouyi_fund'][-1])+'过低'+str(self.dict_param))
                return
            if self.dict_jilu['huiche_max']>35:
                self.log_paramlist(str(jici)+'失败!回撤'+str(self.dict_jilu['huiche_max'])+'过大' + str(self.dict_param))
                return
            if max(self.dict_jilu['list_rate_chicang'])>4.5:
                self.log_paramlist(str(jici)+'失败!持仓率'+str(max(self.dict_jilu['list_rate_chicang']))+'过大' + str(self.dict_param))
                return
            if int(row['timechuo']) > self.dict_param['timechuo_end']:
                print(str(jici)+'到达结束时间'+str(self.get_date_now()))
                self.zongjie()
                return
            else:
                self.run(float(row['open']),float(row['high']),float(row['low']),float(row['close']),float(row['atr']))





