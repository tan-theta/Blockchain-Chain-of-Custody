import os
import sys
import struct
import argparse
from error import *
from datetime import datetime
from collections import namedtuple

def initiate(file_path):

    
    block_head_format = struct.Struct('20s d 16s I 11s I')
    block_head = namedtuple('Block_Head', 'hash timestamp case_id item_id state length')
    block_data = namedtuple('Block_Data', 'data')

    
    try:
        fp = open(file_path, 'rb')
        fp.close()
    except:

        now = datetime.now()
        timestamp = datetime.timestamp(now)
        head_values = (str.encode(""), timestamp, str.encode(
            ""), 0, str.encode("INITIAL"), 14)
        data_value = (str.encode("Initial block"))
        block_data_format = struct.Struct('14s')
        packed_head_values = block_head_format.pack(*head_values)
        packed_data_values = block_data_format.pack(data_value)
        curr_block_head = block_head._make(
            block_head_format.unpack(packed_head_values))
        curr_block_data = block_data._make(
            block_data_format.unpack(packed_data_values))

        # print(curr_block_head)
        # print(curr_block_data)

        fp = open(file_path, 'wb')
        fp.write(packed_head_values)
        fp.write(packed_data_values)
        fp.close()

    fp = open(file_path, 'rb')

    try:
        head_content = fp.read(block_head_format.size)
        curr_block_head = block_head._make(block_head_format.unpack(head_content))
        block_data_format = struct.Struct(str(curr_block_head.length)+'s')
        data_content = fp.read(curr_block_head.length)
        curr_block_data = block_data._make(block_data_format.unpack(data_content))
    except:
        print("Blockchain file not found.")
        Initial_Block_Error()

    fp.close()

    if "INITIAL" in (curr_block_head.state).decode('utf-8').upper():
        return False
    else:
        return True
