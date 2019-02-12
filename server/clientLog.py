import logging, logging.handlers

global rootLogger

rootLogger = logging.getLogger('raspi')

def startLog(ip):
    rootLogger.setLevel(logging.DEBUG)
    socketHandler = logging.handlers.SocketHandler(ip,logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    rootLogger.addHandler(socketHandler)
    logging.info('start log')
