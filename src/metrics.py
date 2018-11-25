import numpy as np

# constants for strategies
SELL = 0
BUY = 1

# annual average market return (expected)
RISK_FREE_RATE = 0.07

####################################
#           Strategies             #
####################################

# Contract:
# each strategy function must produce a
# tuple of buys and sells

def getMomentum(prices, ma1, ma2):
    """
    Momentum strategies assume price is trending when a
    short term moving average crosses a long term moving
    average.
    """
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

def getMeanReversion(prices, ma1, ma2):
    """
    Mean reversion strategies assume a security
    is trending **abnormally** when a short term
    moving average crosses a long term moving average
    """
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
            if short[i - 1] > long[i - 1] and short[i] <= long[i]:  # buy signal
                buys.append(prices[i])
                side = SELL

        else:  # side == SELL
            if short[i - 1] <= long[i - 1] and short[i] > long[i]:  # sell signal
                sells.append(prices[i])
                side = BUY

    # if last sell signal was not generated,
    # sell on last period
    if len(buys) > len(sells):
        sells.append(prices[len(prices) - 1])

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
    cumProfit = (cumProfit - 1) / 100

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

def getSharpeRatio(buys, sells):
    if len(buys) != len(sells):
        raise ValueError("Incompatible dimensions")

    cumProfit = 1
    returns = []

    # we could use cumulative profit function, but we would
    # still need to retrieve the every asset returns
    for buyPrice, sellPrice in zip(buys, sells):
        cumProfit *= sellPrice / buyPrice
        returns.append(sellPrice / buyPrice)

    # if cumProfit is '1', we really made no profit
    cumProfit -= 1

    if len(returns) == 1:
        return (cumProfit - RISK_FREE_RATE) / 1
    else:
        return (cumProfit - RISK_FREE_RATE) / np.std(returns)


def getSortinoRatio(buys, sells):
    if len(buys) != len(sells):
        raise ValueError("Incompatible dimensions")

    cumProfit = 1
    negReturns = []

    # we could use cumulative profit function, but we would
    # still need to retrieve the negative asset returns
    for buyPrice, sellPrice in zip(buys, sells):
        cumProfit *= sellPrice / buyPrice

        if buyPrice > sellPrice:
            negReturns.append(sellPrice / buyPrice)

    # if cumProfit is '1', we really made no profit
    cumProfit -= 1

    if len(negReturns) <= 1:
        return (cumProfit - RISK_FREE_RATE) / 1
    else:
        return (cumProfit - RISK_FREE_RATE) / np.std(negReturns)

def getSterlingRatio(buys, sells):
    if len(buys) != len(sells):
        raise ValueError("Incompatible dimensions")

    cumProfit = 1
    drawdowns = []

    # we could use cumulative profit function, but we would
    # still need to retrieve the drawdowns
    for buyPrice, sellPrice in zip(buys, sells):
        cumProfit *= sellPrice / buyPrice

        if buyPrice > sellPrice:
            drawdowns.append(sellPrice - buyPrice)

    # if cumProfit is '1', we really made no profit
    cumProfit -= 1

    if len(drawdowns) <= 1:
        return (cumProfit - RISK_FREE_RATE) / 1
    else:
        return (cumProfit - RISK_FREE_RATE) / np.std(drawdowns)

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