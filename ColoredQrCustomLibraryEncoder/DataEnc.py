import reedsolo

def pre_process(message):
    mode= '0100'
    msg_length= format(len(message), '08b')

    pre_bits= mode + msg_length
   
    ascii_vals = [ord(char) for char in message]
    #print(f"The ASCII values of '{message}' are: {ascii_vals}")

    
    binary_vals = [format(seq, '08b') for seq in ascii_vals]
    binary_vals= ''.join(binary_vals)
  
    final_msg= pre_bits + binary_vals

    pad_msg= padding(final_msg)
   
    return pad_msg



#Padding Phase
def padding(binary_string):
    
    #pad with zeros until multiple of 8
    remainder= len(binary_string)%8 
    if(remainder!= 0):
        needed_padding= 8-remainder
        binary_string += '0' *needed_padding

    #pad with 0xEC and 0x11 until length is 34 acii chars or 1088 bits as capacity increase 4x
    while (len(binary_string)<1088):
        binary_string += '11101100'  #pad with 0xEC
        if len(binary_string) < 1088:  #pad with 0x11
            binary_string += '00010001' 
    return binary_string
       


def ecc_encode(bit_stream):

    byte_strings = [int(bit_stream[n:n+8], 2) for n in range(0, len(bit_stream), 8)]
    #print(byte_strings)

    
    rs = reedsolo.RSCodec(40)
    encoded_msg = rs.encode(byte_strings)
    #print("The encode msg is " , list(encoded_msg))
    #print(len(encoded_msg))
    return list(encoded_msg)

def send_sent(sentence):
    data= pre_process(sentence)
    
    return ecc_encode(data)

if __name__ == "__main__":
    msg = "hello"
    data= pre_process(msg)

    send_sent(msg)
    

    






