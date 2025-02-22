from tradingview_ta import TA_Handler, Interval, Exchange
# use for environment variables
import os
# use if needed to pass args to external modules
import sys
# used for directory handling
import glob

import time

from helpers.parameters import (
    parse_args, load_config
)
# Load arguments then parse settings
args = parse_args()
#get config file
DEFAULT_CONFIG_FILE = 'config.yml'
config_file = args.config if args.config else DEFAULT_CONFIG_FILE
parsed_config = load_config(config_file)

MY_EXCHANGE = 'BINANCE'
MY_SCREENER = 'CRYPTO'
MY_FIRST_INTERVAL = Interval.INTERVAL_1_MINUTE
MY_SECOND_INTERVAL = Interval.INTERVAL_5_MINUTES
MY_THIRD_INTERVAL = Interval.INTERVAL_15_MINUTES
TA_BUY_THRESHOLD = 13 # How many of the 26 indicators to indicate a buy
PAIR_WITH = parsed_config['trading_options']['PAIR_WITH']
TICKERS = parsed_config['trading_options']['TICKERS_LIST']
TIME_TO_WAIT = 1 # Minutes to wait between analysis
FULL_LOG = False # List anylysis result to console

def analyze(pairs):
    taMax = 0
    taMaxCoin = 'none'
    signal_coins = {}
    first_analysis = {}
    second_analysis = {}
    third_analysis = {}
    first_handler = {}
    second_handler = {}
    third_handler = {}

    if os.path.exists('signals/signalsample.exs'):
        os.remove('signals/signalsample.exs')

    if os.path.exists('signals/signalsample.sell'):
        os.remove('signals/signalsample.sell')

    for pair in pairs:
        first_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_FIRST_INTERVAL,
            timeout= 10
        )
        second_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_SECOND_INTERVAL,
            timeout= 10
        )
        third_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_THIRD_INTERVAL,
            timeout= 10
        )

    for pair in pairs:

        try:
            first_analysis = first_handler[pair].get_analysis()
            second_analysis = second_handler[pair].get_analysis()
            third_analysis = third_handler[pair].get_analysis()
        except Exception as e:
                    print("buysellcustsignal:")
                    print("Exception:")
                    print(e)
                    print (f'Coin: {pair}')
                    print (f'First handler: {first_handler[pair]}')
                    print (f'Second handler: {second_handler[pair]}')
                    print (f'Second handler: {third_handler[pair]}')
                    tacheckS = 0

        first_tacheck = first_analysis.summary['BUY']
        first_recommendation = first_analysis.summary['RECOMMENDATION']
        first_RSI = float(first_analysis.indicators['RSI'])

        second_tacheck = second_analysis.summary['BUY']
        second_recommendation = second_analysis.summary['RECOMMENDATION']
        second_RSI = float(second_analysis.indicators['RSI'])

        third_tacheck = third_analysis.summary['BUY']
        third_recommendation = third_analysis.summary['RECOMMENDATION']
        third_RSI = float(third_analysis.indicators['RSI'])

        if FULL_LOG:
            print(f'buysellcustsignal:{pair} First {first_tacheck} Second {second_tacheck} Third {third_tacheck}')
            print(f'buysellcustsignal:{pair} First {first_recommendation} Second {second_recommendation} Third {third_recommendation}')
        #else:
            #print(".", end = '')

        if first_tacheck > taMax:
                taMax = first_tacheck
                taMaxCoin = pair

        if (first_recommendation == "BUY" or first_recommendation == "STRONG_BUY") and (second_recommendation == "BUY" or second_recommendation == "STRONG_BUY") and \
            (third_recommendation == "BUY" or third_recommendation == "STRONG_BUY"):
                if first_RSI <= 67 and second_RSI <= 67 and third_RSI <= 67:
                    signal_coins[pair] = pair
#                    print(f'buysellcustsignal: Buy Signal detected on {pair}')
                    with open('signals/signalsample.exs','a+') as f:
                        f.write(pair + '\n')

        if (first_recommendation == "SELL" or first_recommendation == "STRONG_SELL") and (second_recommendation == "SELL" or second_recommendation == "STRONG_SELL") and \
            (third_recommendation == "SELL" or third_recommendation == "STRONG_SELL"):
                #signal_coins[pair] = pair
#                print(f'buysellcustsignal: Sell Signal detected on {pair}')
                with open('signals/signalsample.sell','a+') as f:
                    f.write(pair + '\n')

    #print(f'buysellcustsignal: Max signal by {taMaxCoin} at {taMax} on shortest timeframe')

    return signal_coins

#if __name__ == '__main__':
def do_work():
    signal_coins = {}
    pairs = {}

    pairs=[line.strip() for line in open(TICKERS)]
    for line in open(TICKERS):
        pairs=[line.strip() + PAIR_WITH for line in open(TICKERS)]

    while True:
#        print(f'buysellcustsignal: Analyzing {len(pairs)} coins')
        signal_coins = analyze(pairs)
#        if len(signal_coins) == 0:
#            print(f'buysellcustsignal: No coins above {TA_BUY_THRESHOLD} threshold on three timeframes. Waiting {TIME_TO_WAIT} minutes for next analysis')
#        else:
#            print(f'buysellcustsignal: {len(signal_coins)} coins above {TA_BUY_THRESHOLD} treshold on three timeframes. Waiting {TIME_TO_WAIT} minutes for next analysis')

        time.sleep((TIME_TO_WAIT*60))
