#!/bin/python
import socket
from sys import argv, stderr

if __name__ == '__main__':
    addr = ('localhost', 12345)
    if len(argv) == 3:
        addr = (*argv[1:2], )
    elif len(argv) > 1:
        print(f"Usage: {argv[0]} hostname port", file=stderr)
        exit(1)
    print(addr)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        buf = input()
        s.sendto(buf.encode(), addr)