import socket
import struct
import time

localIP     = "0.0.0.0"
localPort   = 11111
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")


blend_shapes = [
  'idk0',
  'idk1',
  'idk2',
  'idk3',
  'EyeBlinkLeft',
  'EyeLookDownLeft',
  'EyeLookInLeft',
  'EyeLookOutLeft',
  'EyeLookUpLeft',
  'EyeSquintLeft',
  'EyeWideLeft',
  'EyeBlinkRight',
  'EyeLookDownRight',
  'EyeLookInRight',
  'EyeLookOutRight',
  'EyeLookUpRight',
  'EyeSquintRight',
  'EyeWideRight',
  'JawForward',
  'JawRight',
  'JawLeft',
  'JawOpen',
  'MouthClose',
  'MouthFunnel',
  'MouthPucker',
  'MouthRight',
  'MouthLeft',
  'MouthSmileLeft',
  'MouthSmileRight',
  'MouthFrownLeft',
  'MouthFrownRight',
  'MouthDimpleLeft',
  'MouthDimpleRight',
  'MouthStretchLeft',
  'MouthStretchRight',
  'MouthRollLower',
  'MouthRollUpper',
  'MouthShrugLower',
  'MouthShrugUpper',
  'MouthPressLeft',
  'MouthPressRight',
  'MouthLowerDownLeft',
  'MouthLowerDownRight',
  'MouthUpperUpLeft',
  'MouthUpperUpRight',
  'BrowDownLeft',
  'BrowDownRight',
  'BrowInnerUp',
  'BrowOuterUpLeft',
  'BrowOuterUpRight',
  'CheekPuff',
  'CheekSquintLeft',
  'CheekSquintRight',
  'NoseSneerLeft',
  'NoseSneerRight',
  'TongueOut',
  'HeadYaw',
  'HeadPitch',
  'HeadRoll',
  'LeftEyeYaw',
  'LeftEyePitch',
  'LeftEyeRoll',
  'RightEyeYaw',
  'RightEyePitch',
  'RightEyeRoll'
]

class Unpacker:
  def __init__(self, data):
    self.data = data
    self.index = 0
    #self.items = []
    
  def unpack(self, fmt):
    size = struct.calcsize(fmt)
    item = struct.unpack(fmt, self.data[self.index:self.index + size])
    if len(item) == 0:
        item = None
    elif len(item) == 1:
        item = item[0]
    #self.items.append(item)
    self.index += size
    return item

  def unpack_cstr1(self):
    size = self.unpack('B')
    item = self.data[self.index:self.index + size]#.decode()
    #self.items.append(item)
    self.index += size
    return item

def parse_message(data):
  u = Unpacker(data)
  version = u.unpack('I')
  guid = u.unpack_cstr1()
  idk123 = u.unpack('BBB')
  device = u.unpack_cstr1()
  idk4 = u.unpack('B')
  remaining = (len(data) - u.index) // 4
  weights = u.unpack('>' + 'f' * remaining)
  return weights

# Listen for incoming datagrms
while True:
    data, src = UDPServerSocket.recvfrom(bufferSize)
    #if len(data) != 312:
    #  print(len(data))
    weights = parse_message(data)

    if time.time() % 1 < 0.1:
      for i in range(len(weights)):
        if i % 10 == 0:
          print('')
        print('%s=%.2f' % (blend_shapes[i], weights[i]), end='   ')
      
      print('\n\n')
    