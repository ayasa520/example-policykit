#!/usr/bin/env python3

import dbus

if __name__ == '__main__':
    interface = dbus.Interface(dbus.SystemBus().get_object(
        "com.example.HelloWorld", "/HelloWorld"), "com.example.HelloWorldInterface")
    result = interface.SayHello("This is client")
    print(result)
