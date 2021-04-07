import subprocess
import serial
import os
import re
import argparse

def getUSB():
    cmd = "ls /sys/class/tty/ttyUSB* -l | grep 1-8:1.0"
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    out = p.stdout.read()
    res = str(out).split('/')[-3]
    #print(str(out))
    #print(res)
    usb = os.path.join("/dev",res)
    print(usb)
    return usb

def changeRTK(usb,ip,port,mountpoint,count, password):
     # 端口：CNU； Linux上的/dev/ttyUSB0等； windows上的COM3等
    portx = usb
        
    # 波特率，标准值有：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    bps = 115200
 
    # 超时设置，None：永远等待操作；
    #         0：立即返回请求结果；
    #        其他：等待超时时间（单位为秒）
    timex = None
    
    # 打开串口，并得到串口对象
    ser = serial.Serial(portx, bps, timeout=timex)
    print("串口详情参数：", ser)
    
    print("AT+ENTERCFG")
    ser.write("AT+ENTERCFG\r".encode("utf-8"))
    getOK(ser)
    
    print(("AT+SET=1,{}\r".format(ip)).encode("utf-8"))
    res = ser.write(("AT+SET=1,{}\r".format(ip)).encode("utf-8"))
    print("res:{}".format(res))
    getOK(ser)
    
    print("AT+SET=2,{}\r".format(port))
    ser.write(("AT+SET=2,{}\r").format(port).encode("utf-8"))
    getOK(ser)

    print(("AT+SET=25,{}\r").format(mountpoint))
    ser.write(("AT+SET=25,{}\r").format(mountpoint).encode("utf-8"))
    getOK(ser)

    print(("AT+SET=22,{}\r").format(count))
    ser.write(("AT+SET=22,{}\r").format(count).encode("utf-8"))
    getOK(ser)

    print(("AT+SET=23,{}\r").format(password))
    ser.write(("AT+SET=23,{}\r").format(password).encode("utf-8"))
    getOK(ser)

    print("AT+GET=1")
    ser.write("AT+GET=1\r".encode("utf-8"))
    getOK(ser)

    print("AT+EXITCFG\r")
    ser.write("AT+EXITCFG\r".encode("utf-8"))
    
    
    ser.close()
    print("-----change success!!!-----")

def getOK(ser):
    while True:
        line = ser.readline()
        try:
            print(line.decode('utf-8'),end='')
        except:
            pass
        if ( re.search(b'OK',line)):
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--ip', type=str, default=None)
    parser.add_argument('--port', type=str, default=None)
    parser.add_argument('--mountpoint', type=str, default=None)
    parser.add_argument('--count', type=str, default=None)
    parser.add_argument('--password', type=str, default=None)

    args = parser.parse_args()
    usb = getUSB()
    changeRTK(usb,args.ip,args.port,args.mountpoint,args.count,args.password)

