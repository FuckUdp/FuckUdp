#!/usr/bin/python
import argparse
import atexit
import random
import socket
import struct
import time

BAD_WORDS = [ "fuck",
  "damn",
  "shit",
]

WORD_USAGE = {x:0 for x in BAD_WORDS}

fucks = 0

parser = argparse.ArgumentParser(description="Make enemies on the network")
parser.add_argument('--interval', help="Time between each packet in seconds", default="1")
parser.add_argument('--ipv4', help="Disable ipv6... Weirdo.", action='store_true')
parser.add_argument('--nodns', help="Disable DNS lookups. Goes much faster.", action='store_true')
parser.add_argument('--quiet', help="Disable printing. Goes much faster.", action='store_true')
args = parser.parse_args()

def swear(bad_word):
  if random.getrandbits(1) and not(args.ipv4):
    ip = socket.inet_ntop(socket.AF_INET6, struct.pack('>QQ', random.randint(1, 0xffffffffffffffff), random.randint(1, 0xffffffffffffffff)))
    proto = socket.AF_INET6
  else:
    ip = socket.inet_ntop(socket.AF_INET, struct.pack('>I', random.randint(33554432, 0xffffffff)))
    proto = socket.AF_INET
  port = random.randint(1, 65535)
  sock = socket.socket(proto, socket.SOCK_DGRAM)
  host = ip
  if not args.nodns:
    try:
      host = socket.gethostbyaddr(ip)[0]
    except:
      pass
  if not args.quiet:
    print("{bw} -> {host}:{port}".format(bw=bad_word, host=host, port=port))
  sock.sendto(bad_word.encode('UTF-8'), (ip, port))

def main():
  global fucks
  while True:
    bad_word = random.choice(BAD_WORDS)
    WORD_USAGE[bad_word] += 1
    swear(bad_word)
    time.sleep(float(args.interval))

def cleanup():
  for i, j in WORD_USAGE.items():
    print("Gave {j} {i}'s".format(i=i, j=j))

atexit.register(cleanup)

main()
