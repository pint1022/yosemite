import argparse

import plotly.graph_objects as go
import pandas_ta as ta
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode
from plotly.io import write_image
import yahoo_fin.stock_info as si

import os
from pytz import timezone
import pytz

datadir = '/home/steven/dev/yosemite_jupyter/dataset'

def export_chart(ticker='tsla', startdate=datetime.now(), period='30d', interval='15m'):
    startdate = startdate.astimezone(timezone('US/Pacific'))
    intervaldir =os.path.join(datadir, 'interval-'+period+'-'+interval)
    start = (startdate - timedelta(days=5)).strftime('%Y-%m-%d')
    end = startdate.strftime('%Y-%m-%d')

    if not os.path.exists(intervaldir):
        os.makedirs(intervaldir)
        
    stockdir = os.path.join(intervaldir, ticker)
    if not os.path.exists(stockdir):
        os.makedirs(stockdir)
    filename=os.path.join(stockdir, 'chart-'+end+'.jpg')
    
    if os.path.exists(filename):
        return 
    tick= yf.Ticker(ticker)
    fig = make_subplots(rows=1, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    subplot_titles=(ticker,),
    row_heights = [1000])
    fig.layout.xaxis.type = 'category'

#     data = yfinance.Ticker(ticker).history(period, interval=interval)

    # %d-%m-%Y %H:%M:%S

    data = tick.history(start=start, end=end, interval=interval)
#     data.ta.willr(append=True)
    data.ta.sma(length=7, append=True)
    data.ta.sma(length=20, append=True)
#     data = data[data['Volume']>0]
    fig.add_trace(go.Candlestick(x=data.loc[start:end].index,
    open=data.loc[start:end]['Open'],
    high=data.loc[start:end]['High'],
    low=data.loc[start:end]['Low'],
    close=data.loc[start:end]['Close'],
    name=ticker),
    row=1,col=1)

    # fig.add_trace(go.Bar(x=data.loc[start:end].index,
    # y=data.loc[start:end]['Volume'],
    # showlegend=False),
    # row=2, col=1)
    key_to_lookup = 'SMA_7'
    if key_to_lookup in data.loc[start:end]:
        sma7 = go.Scatter(x=data.loc[start:end].index,
        y=data.loc[start:end]['SMA_7'],
        mode='lines',
        name='SMA 7')
        fig.add_trace(sma7, row=1, col=1)

    key_to_lookup = 'SMA_20'
    if key_to_lookup in data.loc[start:end]:
        sma20 = go.Scatter(x=data.loc[start:end].index,
        y=data.loc[start:end]['SMA_20'],
        mode='lines',
        name='SMA 20')
        fig.add_trace(sma20, row=1, col=1)
    fig.update_layout(xaxis={'type': 'category'},xaxis_rangeslider_visible=False, width=1000, height=800)
    intervaldir =os.path.join(datadir, 'interval-'+period+'-'+interval)
    fig.write_image(filename)

def option_date(ticker='tsla', period=2):
    start_day = datetime.now().astimezone(timezone('US/Pacific'))
    while start_day.weekday() > 4:
        start_day=start_day - timedelta(days=1)
        
    op_wk = int(start_day.strftime("%V"))
    tick= yf.Ticker(ticker)
    selected_ops = [d for index, d in enumerate(tick.options, start=0) if index < period]
    return start_day.strftime("%Y-%m-%d"),selected_ops

def export_option_chain(ticker='tsla', period=2):
    optiondir =os.path.join(datadir, 'option-chain')
    
    if not os.path.exists(optiondir):
        os.makedirs(optiondir)
        
    stockdir = os.path.join(optiondir, ticker)
    
    if not os.path.exists(stockdir):
        os.makedirs(stockdir)

        
    tick= yf.Ticker(ticker)
    recorddate, optiondates = option_date(ticker, period)
    recorddat_dir=os.path.join(stockdir, 'option-'+recorddate)
    calldir = os.path.join(recorddat_dir, 'calls')
    putdir = os.path.join(recorddat_dir, 'puts')   

    if not os.path.exists(recorddat_dir):
        os.makedirs(recorddat_dir)
        os.makedirs(calldir)
        os.makedirs(putdir)
    else:
        optfiles = os.listdir(calldir)
        if len(optfiles) > 0:
            return
    for d in optiondates:
        try:
            opt = tick.option_chain(d)
        except ValueError:
            print(ticker, 'has no option on ', d)
            continue
        callfilename=os.path.join(calldir, 'call-'+d+'.pkl')
        putfilename=os.path.join(putdir, 'put-'+d+'.pkl')        
        opt.calls.to_pickle(callfilename)
        opt.puts.to_pickle(putfilename)

def isExported(datadir, period, interval):
    dataDir =os.path.join(datadir, 'interval-'+period+'-'+interval)
    return os.path.exists(intervaldir)

def isMarketOpen(datadir, period, interval):
    dataDir =os.path.join(datadir, 'interval-'+period+'-'+interval)
    return os.path.exists(intervaldir)

def export_missing_data(list=si.tickers_sp500(), startdate=datetime.now()):
    interval='15m'
    option_period=24
    sdate = startdate
    edate = datetime.now().astimezone(timezone('US/Pacific'))
    while sdate < edate:
        while sdate.weekday() > 4:
            sdate=sdate + timedelta(days=1)
        if (sdate >= edate):
            print("completed catchup from ", startdate)
            break
        print(one_date, one_date.weekday())

        for ticker in list:
            if ticker=='GEN':
                continue
            weekno = one_date.weekday()
            if weekno < 5:
                try:
                    export_chart(ticker=ticker, startdate=one_date, period='wk', interval=interval)
                except ValueError:
                    print(ticker, 'has no data ', ValueError)            
                export_option_chain(ticker=ticker, period=option_period)

def export_today_data(list=si.tickers_sp500(),  interval='15m', option_period=24, one_date=datetime.now().astimezone(timezone('US/Pacific'))):
    while one_date.weekday() > 4:
        one_date=one_date - timedelta(days=1)    
    print(one_date, one_date.weekday())

    for ticker in list:
        if ticker=='GEN':
            continue
        weekno = one_date.weekday()
        if weekno < 5:
            try:
                export_chart(ticker=ticker, startdate=one_date, period='wk', interval=interval)
            except ValueError as e:
                print(ticker, 'has no data ', e)            
            export_option_chain(ticker=ticker, period=option_period)

def mkdate(datestr):
    return datetime.strptime(datestr, '%Y-%m-%d')

def parse():
    parser = argparse.ArgumentParser(description='stock data collection')
    parser.add_argument('--missing', default=False, action='store_true')    
    parser.add_argument('--dir', '-d', metavar='DIR', default='dataset',
                        help='path(s) to dataset (if one path is provided, it is assumed\n' +
                       'to have subdirectories named "train" and "val"; alternatively,\n' +
                       'train and val paths can be specified directly by providing both paths as arguments)')
    parser.add_argument('--list', '-l', metavar='LIST', default='all',
                        help='list of stock groups: sp500, dow or all') 
    parser.add_argument('--date', '-dt', metavar='DATE', type=mkdate, default=datetime.now(),
                        help='which date is to retrieve') 
# 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo                      
    parser.add_argument('--interval', '-n', metavar='Interval', default='15m',
                        help='the interval of stock data')                       
    parser.add_argument('--option-period', '-p', default='24', type=int,
                        metavar='N', help='option period (default: 24)')
    args = parser.parse_args()
    return args

def main():
    args = parse()
    datadir = args.dir
    sgroups = {"sp500":si.tickers_sp500(),
        "dow": si.tickers_dow(),
        "custom": ['SQQQ', 'TQQQ', 'SOXL', 'BX', 'BLK', 'COIN', 'MSTR', 'LRCX', 'U', 'ASML', 'TSM', 'GS', 'NVDA', 'AMD']}
    if args.missing:
        print("export all list...\n")
        for l in sgroups:
            export_missing_data(l, one_date=args.date)
        return

    print(args.date)
    if args.list == 'all':
        print("export all list...\n")
        for l in sgroups:
            export_today_data(l, interval=args.interval, option_period=args.option_period, one_date=args.date)
    elif args.list == 'sp500':
        print("export sp500...\n")
        export_today_data(sgroups['sp500'], interval=args.interval, option_period=args.option_period, one_date=args.date)
    elif args.list == 'dow':
        print("export dow...\n")
        export_today_data(sgroups['dow'], interval=args.interval, option_period=args.option_period, one_date=args.date)
    else:
        print("export custom...\n")
        export_today_data(sgroups['custom'], interval=args.interval, option_period=args.option_period, one_date=args.date)

if __name__ == '__main__':
    main()
