#!/usr/bin/env python
import serial
import sys
import os
from time import sleep
# Initializing
HOST = str(sys.argv[1])
pres = 1
# wait for prompt procedure


def wfp(srl):
    sym = ' '
    buf = ''
    while sym != '#'.encode():
        sym = srl.read(1)
        buf += sym
    sleep(1)
    print buf
    srl.reset_input_buffer()
    return ''

# downloadinfg firmware
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.write(b'\n ' + 'admin' + '\n'+'ahKofei1oa' + '\n ')
wfp(ser)
ser.write(b'\n ' + 'reset config' + ' \n ' + 'y')
wfp(ser)
ser.write(b'config ipif System ipaddress 192.168.0.239/24' + '\n ')
wfp(ser)
ser.write(b'create iproute default 192.168.0.1' + '\n ')
wfp(ser)
ser.write(b'save' + '\n ')
wfp(ser)
ser.write(b'download firmware_fromTFTP 192.168.100.10'+
          ' s firmware/dlink/DGS300024TC/fw.had' + '\n ')
wfp(ser)
ser.write(b'\n ' + 'reboot' + ' \n ' + 'y')
# waiting for switch to reboot
sleep(5)
print 'pinging',
while pres != 0:
    pres = os.system('ping -c 1 192.168.0.239 > /dev/null')
    print '.',
    sleep(2)
print "pong"
sleep(2)
# uploading config from first parameter
ser.write(b'\n ' + 'admin' + '\n ' + 'ahKofei1oa' + '\n ')
wfp(ser)
ser.write(b'download cfg_fromTFTP 192.168.100.10 s ' +
          HOST.rstrip() + '.cfg' + '\n ')
wfp(ser)
sleep(15)
ser.reset_input_buffer()
# saving configuration
ser.write(b'save' + '\n ')
wfp(ser)
ser.write(b'logout' + '\n ')
print "Done."
ser.close()
