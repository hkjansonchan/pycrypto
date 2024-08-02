crypto = "BTC"
interval = "15m"

match crypto:
    case 'BTC':
        start = "2018-01-01 00:00:00"
        # BTC/USDT discord webhook
        webhook_url = "https://discordapp.com/api/webhooks/1260121431115563028/r2Fh9u2g9ZPY_sUpmJ58c6eA0wm3Qr2B1QCSeRbwN2BaZqjjiop3mWJKhiIK58H_0mUP"

        # ohlcv data of BTC/USDT
        raw_data_15m = rf"pycrypto/{crypto}{interval}.csv"

        # Analyzed data of BTC/USDT
        analysis_15m = rf"pycrypto/analysis_{crypto}{interval}.csv"
    case 'PEPE':
        start = "2023-05-06 00:00:00"
        # PEPE/USDT discord webhook
        webhook_url = "https://discordapp.com/api/webhooks/1268794823909838869/gNjlnJp6y8Arvm6sjpsYqch6OtId6T_5_EU029xlMgHYru-rQaHCkBkOjl4ljgKRmyG8"

        # ohlcv data of PEPE/USDT
        raw_data_15m = rf"pycrypto/{crypto}{interval}.csv"

        # Analyzed data of PEPE/USDT
        analysis_15m = rf"pycrypto/analysis_{crypto}{interval}.csv"





