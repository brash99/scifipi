import sys
import binascii

def get_bits(limit_status):
    status = limit_status.decode()
    hexcode = binascii.hexlify(status.encode('utf-8','surrogatepass'))
    inthexcode = int(hexcode,16)
    binarycode = bin(inthexcode)
    bits = binarycode[2:]
    bitsz = bits.zfill(4*((len(bits)+3)//4))

    #print ('Hexcode = ',hexcode,'  Int(hexcode) = ',inthexcode,' Binary rep = ',binarycode,'  Bits = ',bits,' BitsZ = ',bitsz)
    return bitsz

limit_status1 = b'\x00'

print ('Original serial bytecode = ',limit_status1)
print ('Bits = ',get_bits(limit_status1))
