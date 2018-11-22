import numpy as np

# constants for strategies
SELL = 0
BUY = 1

####################################
#           Strategies             #
####################################

# Contract:
# each strategy function must produce a
# tuple of buys and sells

def getMACrossover(prices, ma1, ma2):
    short = long = None
    if len(ma1) < len(ma2):
        short = ma2
        long = ma1
    else:
        short = ma1
        long = ma2

    # truncate all 3 series to same length
    trunc = len(long)
    prices = prices[len(prices) - trunc:]
    short = short[len(short) - trunc:]

    buys, sells = [], []
    side = BUY

    # Long only - find first buy signal
    for i in range(1, len(prices)):

        if side == BUY:
            if short[i-1] <= long[i-1] and short[i] > long[i]:  # buy signal
                buys.append(prices[i])
                side = SELL

        else:  # side == SELL
            if short[i-1] > long[i-1] and short[i] <= long[i]:  # sell signal
                sells.append(prices[i])
                side = BUY

    # if last sell signal was not generated,
    # sell on last period
    if len(buys) > len(sells):
        sells.append(prices[len(prices)-1])


    return buys, sells


def getBuyAndHold(prices):
    """
    CONTROL STRATEGY
    The Buy and Hold strategy assumes purchase on first price and
    sell on last price
    :param prices: NP Array of asset prices
    """

    buys = [prices[0]]
    sells = [prices[len(prices)-1]]
    return buys, sells


####################################
#      Performance Metrics         #
####################################

# Contract:
# Each performance metric must
# take a list of buy and sell prices

def getCumulativeProfit(buys, sells):
    if len(buys) != len(sells):
        raise ValueError("Incompatible dimensions")

    cumProfit = 1

    for buyPrice, sellPrice in zip(buys, sells):
        cumProfit *= sellPrice / buyPrice

    # if cumProfit is '1', we really made no profit
    cumProfit -= 1

    return cumProfit

def getAverageProfitPerTrade(buys, sells):
    if len(buys) != len(sells):
        raise ValueError("Incompatible dimensions")

    # accumulator
    averageProfit = 0

    for buyPrice, sellPrice in zip(buys, sells):
        averageProfit += sellPrice - buyPrice

    # divided by number of trades
    averageProfit /= len(buys)

    return averageProfit


# testing code
if __name__ == "__main__":
    prices = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
    ma2 = np.array([0.841470985,0.909297427,0.141120008,-0.756802495,-0.958924275,-0.279415498,0.656986599,0.989358247,0.412118485,-0.544021111,-0.999990207,-0.536572918,0.420167037,0.990607356,0.65028784,-0.287903317,-0.961397492])
    ma1 = np.array([0.479425539,0.841470985,0.997494987,0.909297427,0.598472144,0.141120008,-0.350783228,-0.756802495,-0.977530118,-0.958924275,-0.705540326,-0.279415498,0.215119988,0.656986599,0.937999977,0.989358247])

    buys, sells = getMACrossover(prices, ma1, ma2)
    cumProfit = getCumulativeProfit(buys, sells)
    average = getAverageProfitPerTrade(buys, sells)

    buys, sells = getBuyAndHold(prices)
    cumProfit = getCumulativeProfit(buys, sells)
    average = getAverageProfitPerTrade(buys, sells)