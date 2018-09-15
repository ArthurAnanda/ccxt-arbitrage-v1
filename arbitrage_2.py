# 此脚本由一个确定的交易对pair找到全市场的最优搬砖路径
import ccxt
import pandas as pd
import datetime

# datetime_now = str(datetime.datetime.now())[:19]
# print(datetime_now)
# print(datetime_now<'2018-09-15 00:32:57')

def exchangeHasSymbol(exchange,symbol):
    '''
    prerequisite: ccxt
    :param exchange: str; a ccxt exchange name
    :param symbol: str; trading pairs such as 'ETH/USDT'
    :return: bool; true if exchange have such pair trading
    '''
    try:
        if symbol in getattr(ccxt,exchange)().symbols:
            return True
        else:
            return False
    except:
        return False

def fetchExchangePairBidAndAsk(exchange,pair):
    '''
    prerequisite: ccxt
    '''
    exchange_object=getattr(ccxt,exchange)()
    order_book=exchange_object.fetch_order_book(pair, 3)
    return {'bids':order_book['bids'][0][0],'asks':order_book['asks'][0][0]}

def formTradingDataframe(exchange_list,pair):
    resultDF_valid_bidsandasks=pd.DataFrame(None)
    datetime_now = str(datetime.datetime.now())[:19]
    for i in exchange_list:
        try:
            iSeries=pd.Series(fetchExchangePairBidAndAsk(i,pair),name=i)
            resultDF_valid_bidsandasks=pd.concat([resultDF_valid_bidsandasks,iSeries],axis=1,sort=False)
        except:
            pass
            # print(i,'\t',' oops ')
    resultDF_valid_bidsandasks=resultDF_valid_bidsandasks.T
    return {'resultDF':resultDF_valid_bidsandasks,'time': datetime_now}

def findBestArbitrageOpportunity(result):
    resultDF=result['resultDF']
    time=result['time']
    trade_bid = resultDF['bids'].max()
    trade_ask = resultDF['asks'].min()
    trade_bid_exchange = resultDF[resultDF['bids'] == trade_bid].index.tolist()[0]
    trade_ask_exchange = resultDF[resultDF['asks'] == trade_ask].index.tolist()[0]
    if trade_bid > trade_ask:
        print('existing trading opportunity at time:\t',time)
        print('trade_bid_exchange: ', trade_bid_exchange, '\t', 'trade_bid: ', trade_bid)
        print('trade_ask_exchange: ', trade_ask_exchange, '\t', 'trade_ask: ', trade_ask)
        print('return: ', trade_bid / trade_ask - 1)
    else:
        pass
        # print('there is not trading opportunity')

def mainFunction(pair):
    exchange_list=ccxt.exchanges
    valid_exchange_list=[]
    for i in exchange_list:
        if exchangeHasSymbol(i,pair):
            valid_exchange_list.append(i)
    print('trading pair: ',pair)
    print('valid_exchange_list',valid_exchange_list)
    i=0 # 设定循环总次数
    while True:
        datetime_now = str(datetime.datetime.now())[:19]
        if len(valid_exchange_list)==0 or datetime_now>'2018-09-19 07:31:18': # 确定跳出循环的条件
            break
        try:
            result=formTradingDataframe(valid_exchange_list,pair)
            findBestArbitrageOpportunity(result)
        except:
            continue
        i+=1
    print('all loop times: ',i)

if __name__ == '__main__':
    mainFunction(pair='ETH/BTC')

