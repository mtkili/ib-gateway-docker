from ib_insync import IBC, IB, Watchdog
import os
import logging
import signal
import sys

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="[%(asctime)s]%(levelname)s:%(message)s")
    logging.info('start ib gateway...')
    ib_gateway_version = int(os.listdir("/root/Jts/ibgateway")[0])
    account = os.environ['IB_ACCOUNT']
    password = os.environ['IB_PASSWORD']
    trade_mode = os.environ['TRADE_MODE']
    ibc = IBC(ib_gateway_version, gateway=True, tradingMode=trade_mode, userid=account, password=password)
    ib = IB()
    def onConnected():
        logging.info('IB gateway connected')
        logging.info(ib.accountValues())
            
    def onDisconnected():
        logging.info('IB gateway disconnected')
    ib.connectedEvent += onConnected
    ib.disconnectedEvent += onDisconnected
    watchdog = Watchdog(ibc, ib, port=os.environ['IBGW_PORT'], 
        connectTimeout=60, 
        appStartupTime=60, 
        appTimeout=59)
    watchdog.start()
    ib.run()
    logging.info('IB gateway is ready.')
    
