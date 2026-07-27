import finnhub, os

def analyzeStock(symbol):
    finnhubClient = finnhub.Client(api_key=os.environ.get("FINNHUB_API_KEY"))

    quote = finnhubClient.quote(symbol)
    currentPrice = round(quote['c'], 2)
    percentChange = round(quote['dp'], 2)
    print("Current price: $" + str(currentPrice))
    print("Percent change: " + str(percentChange) + "%")

    data = finnhubClient.company_basic_financials(symbol, 'all')


    fiftoHigh = round(data["metric"]["52WeekHigh"], 2)
    fiftoLow = round(data["metric"]["52WeekLow"], 2)
    peRatio = round(data["metric"]["peTTM"], 2)
    roe = round(data["metric"]["roeTTM"], 2)
    revenueGrowth = round(data["metric"]["revenueGrowthTTMYoy"], 2)
    currentRatio = round(data["metric"]["currentRatioQuarterly"], 2)
    debtEquityRatio = round(data["metric"]["totalDebt/totalEquityQuarterly"], 2)

    print("52-week high: $" + str(fiftoHigh))
    print("52-week low: $" + str(fiftoLow))
    print("P/E ratio: " + str(peRatio))
    print("ROE: " + str(roe) + "%")
    print("Revenue Growth (Last 4 quarters): " + str(revenueGrowth) + "%")
    print("Current Ratio (Quarterly): " + str(currentRatio))
    print("Total Debt/Total Equity (Quarterly): " + str(debtEquityRatio))

    #position of current price in relation to 52-week high and low, 0 = low, 1 = high
    position = (currentPrice - fiftoLow) / (fiftoHigh - fiftoLow)


    #Now will give a "Buy Score" based on personal value of stock stats
    buyScore = 0
    buyScoreColor = ""

    revenueGrowthColor = "bad"
    if revenueGrowth >= 20: #total of 20 points, weight of 20%
        buyScore += 20
        revenueGrowthColor = "great"
    elif revenueGrowth >= 10:
        buyScore += 16
        revenueGrowthColor = "good"
    elif revenueGrowth >= 0:
        buyScore += 8
        revenueGrowthColor = "average"

    roeColor = "bad"
    if roe >= 20: #total of 20 points, weight of 20%
     buyScore += 20
     roeColor = "great"
    elif roe >= 15:
     buyScore += 15
     roeColor = "good"
    elif roe >= 10:
        buyScore += 10
        roeColor = "average"


    #10-25 is average healthy pe ratio range
    peRatioColor = "bad"
    if 10 <= peRatio <= 25: #total of 25 points, weight of 25%
     buyScore += 25
     peRatioColor = "great"
    elif 25 < peRatio <= 35:
        buyScore += 19
        peRatioColor = "good"
    elif 35 < peRatio <= 50 or 0 < peRatio < 10:
        buyScore += 13
        peRatioColor = "average"

    #1.5 and above is considered healthy, however more than three points
    #  to inefficiency
    currentRatioColor = "bad"
    if 1.5 <= currentRatio <= 3: #total of 10 points, weight of 10%
        buyScore += 10
        currentRatioColor = "great"
    elif 1.2 <= currentRatio < 1.5:
        buyScore += 7
        currentRatioColor = "good"
    elif 1.0 <= currentRatio <= 1.2 or currentRatio > 3:
        buyScore += 3
        currentRatioColor = "average"

    debtEquityRatioColor = "bad"
    if debtEquityRatio <= 0.5: #total of 15 points, weight of 15%
        buyScore += 15
        debtEquityRatioColor = "great"
    elif debtEquityRatio <= 1:
        buyScore += 13
        debtEquityRatioColor = "good"
    elif debtEquityRatio <= 2:
        buyScore += 5
        debtEquityRatioColor = "average"


    if position <= 0.20:#52 week position has a weight of 10%
        buyScore += 10
    elif position <= 0.40:
        buyScore += 8
    elif position <= 0.60:
        buyScore += 6
    elif position <= 0.80:
        buyScore += 4



    #Personal bonus points for negative percent change points assumin stock
    #is doing good enough to get extra points
    if  buyScore >= 60 and percentChange < 0:
        if percentChange <= -10:
            buyScore += 5
        elif percentChange <= -5:
            buyScore += 3
        elif percentChange < 0:
            buyScore += 1

    percentChangeColor = "bad"
    if percentChange > 0:
        percentChangeColor = "good"



    print() #space for break of score and recommendation

    recommendation = ""
    recommendationColor = ""

    print("Buy Score: " + str(buyScore) + "/100")
    if buyScore >= 100:
        recommendation = "No-Brainer"
        recommendationColor = "great"
        buyScoreColor = "great"
    elif buyScore > 90:
        recommendation = "Strong Buy"
        recommendationColor = "great"
        buyScoreColor = "great"
    elif buyScore >= 75:
        recommendation = "Buy"
        recommendationColor = "good"
        buyScoreColor = "good"
    elif buyScore >= 60:
        recommendation = "Weak Buy"
        recommendationColor = "average"
        buyScoreColor = "average"
    elif buyScore >= 50:
        recommendation = "Hold/Wait"
        recommendationColor = "bad"
        buyScoreColor = "bad"
    else:
        recommendation = "Avoid"
        recommendationColor = "bad"

    print("Recommendation: " + recommendation)


    # keys for for variables for html file to use easily
    print("reached return statement")


    fiftoHigh = f"{fiftoHigh: .2f}" #forces two decimal places
    fiftoLow = f"{fiftoLow: .2f}"
    return {
        
        "currentPrice": currentPrice,
        "percentChange": percentChange,
        "percentChangeColor": percentChangeColor,
        "fiftoHigh": fiftoHigh,
        "fiftoLow": fiftoLow,
        "peRatio": peRatio,
        "peRatioColor": peRatioColor,
        "roe": roe,
        "roeColor": roeColor,
        "revenueGrowth": revenueGrowth,
        "revenueGrowthColor": revenueGrowthColor,
        "currentRatio": currentRatio,
        "currentRatioColor": currentRatioColor,
        "debtEquityRatio": debtEquityRatio,
        "debtEquityRatioColor": debtEquityRatioColor,
        "position": position,
        "buyScore": buyScore,
        "recommendation": recommendation,
        "buyScoreColor": buyScoreColor,
        "recommendationColor": recommendationColor
    }





    
