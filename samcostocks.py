import requests
import json


def tockenHeader(u, p, y):
    loginHeaders = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    loginRequestBody = {
        "userId": u,
        "password": p,
        "yob": y
    }
    loginResponse = requests.post(
        'https://api.stocknote.com/login', data=json.dumps(loginRequestBody), headers=loginHeaders)
    a = loginResponse.json()

    tockenHeaders = {
        'Accept': 'application/json',
        'x-session-token': a['sessionToken']
    }
    return tockenHeaders
#########################################
# ORDER BOOK
# oBookResponse = requests.get('https://api.stocknote.com/order/orderBook', headers = tockenHeaders).json()
# print(oBookResponse['orderBookDetails'][0]['tradingSymbol'])

#########################################
# HOLDINGS


def holding(u, p, y):
    holdingsResponse = requests.get(
        'https://api.stocknote.com/holding/getHoldings', headers=tockenHeader(u, p, y)).json()
    holding.symbol = []
    qnty = []
    avgP = []
    ltp = []
    pnl = []
    pnlperc = []
    try:
        for stocks in holdingsResponse['holdingDetails']:
            holding.symbol.append(stocks['tradingSymbol'])
            qnty.append(int(stocks['holdingsQuantity']))
            avgP.append(float(stocks['averagePrice']))
            ltp.append(float(stocks['lastTradedPrice']))
            pnl.append(float(stocks['totalGainAndLoss']))
            pnlperc.append((((float(stocks['lastTradedPrice'])-float(stocks['averagePrice']))/float(
                stocks['holdingsQuantity']))/float(stocks['averagePrice']))*100)

        f = open('samco_holdings.html', 'w')
        head = """<html><head><title>Samco Stocks</title><meta http-equiv="refresh" content="10"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Trirong"><style>
  table {
    border-collapse: collapse;
    width: 50%;
    height: 50%;
    align:center;
    border-radius:20px;
    font-size:15px
  }
  table,h3,nav{
    font-family: "Trirong", serif;
    align:center
  }
  th, td {
    text-align: left;
    padding: 4px;
  }
  th {
    background-color: #04AA6D;
    color: white;
  }
  </style></head>"""
        body = """<body><b><table align=center><tr>
        <th>holding.symbol</th><th>Qnty</th><th>Average price</th><th>LTP</th><th>PNL</th><th>PNL %</th></tr>"""
        totalInvestment = 0
        avg_profit_perc = 0
        for i in range(len(holding.symbol)):
            totalInvestment = totalInvestment+(qnty[i]*avgP[i])

            if pnlperc[i] < 0:
                t = """<tr align=center><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td bgcolor=red>{}</td></tr>""".format(
                    holding.symbol[i], qnty[i], avgP[i], ltp[i], pnl[i], format(pnlperc[i], '.2f'))
            else:
                t = """<tr align=center><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td bgcolor=green>{}</td></tr>""".format(
                    holding.symbol[i], qnty[i], avgP[i], ltp[i], pnl[i], format(pnlperc[i], '.2f'))
                avg_profit_perc = pnlperc[i]+avg_profit_perc
            body = body+t

        # total="""<tr align=center bgcolor='green'><td>Total</td><td></td><td></td><td>{}</td><td>{}</td><td></td></tr>""".format(holdingsResponse['holdingSummary']['portfolioValue'],format(sum(pnl),'.2f'))
        webPageHeading = """<nav><h3>Portfolio value: {}&emsp;|&emsp;Investment: {}&emsp;|&emsp;Profit: {}&emsp;|&emsp;only profit percentage: {}</h3></nav>""".format(
            holdingsResponse['holdingSummary']['portfolioValue'], format(totalInvestment, '.2f'), format(sum(pnl), '.2f'), format(avg_profit_perc/len(holding.symbol), '.2f'))
        f.write(head+webPageHeading+body+'<h3>Total no. of scrips:' +
                str(len(holding.symbol))+'</h3>'+'</b></body></html>')
        f.close()
    except Exception as e:
        print(e)


u = input("enter client id:")
p = input("enter password:")
y = input("enter yob:")


holding(u, p, y)
print(holding.symbol)