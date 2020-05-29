#coding:utf8

import frida, sys,os,json,codecs
import subprocess
import time
import ctypes

if (len(sys.argv) == 3):
    jsfile = str(sys.argv[1].strip())
    package_name = str(sys.argv[2]).strip()
else:

  print "Usage: python frida_attach.py [hook.js] [package_name] "

  sys.exit(1)

def print_result(message):
    print ("[!] Received: [%s]" %(message))

def stringFromArray(data):

    ret = ''
    for i in data:
        value = ctypes.c_uint8(i).value

        if value == 0:

            continue

        if value <=127:

            ret += chr(value)
        else:

            ret += '\\x' + hex(value)[2:]

    return ret


def hex_stringFromArray(data):

    ret = '['
    for i in data:
        value = ctypes.c_uint8(i).value

        ret += hex(value) + ","

    return ret + "]"

def on_message(message, data):
    print(data)
    if 'payload' in message:
        data = message['payload']

        if type(data) is list:

            print stringFromArray(data)

        else:
            print data
       
    else:
        if message['type'] == 'error':
            print (message['stack'])
        else:
            print message

def main():

    with codecs.open(jsfile, 'r', encoding='utf8') as f:
         jscode  = f.read()

    process = frida.get_device_manager().enumerate_devices()[-1].attach(package_name)
    script = process.create_script(jscode)
    script.on('message', on_message)
    script.load()
    sys.stdin.read()

if __name__ == '__main__':
    main()
