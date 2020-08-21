import uuid
import struct
from collections import namedtuple

def display(file_path):

    block_head_format = struct.Struct('@20s d 16s I 11s I')
    block_head = namedtuple('Block_Head', 'hash timestamp case_id item_id state length')
    block_data = namedtuple('Block_Data', 'data')

    fp = open(file_path, 'rb')

    while True:

        try:
            head_content = fp.read(block_head_format.size)
            curr_block_head = block_head._make(
                block_head_format.unpack(head_content))
            block_data_format = struct.Struct(str(curr_block_head.length)+'s')
            data_content = fp.read(curr_block_head.length)
            curr_block_data = block_data._make(
                block_data_format.unpack(data_content))
            print(curr_block_head)
            print(curr_block_data)
        except:
            break

    fp.close()
