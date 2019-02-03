import imgServer  as img
import carControl as control
import clientLog  as log


log.startLog('172.16.10.223')
rootLogger = log.rootLogger

img.startImgSever(("172.16.10.227", 12345))
control.startMoveSever(('172.16.10.227',12347),rootLogger)