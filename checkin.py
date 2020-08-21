import os
import uuid
import struct
import hashlib
from error import *
from initiate import initiate
from datetime import datetime
from collections import namedtuple


def checkin(item_id, file_path):

    success = True
    state = ''
    prev_hash = b''
    case_id = ''

    block_head_format = struct.Struct('20s d 16s I 11s I')
    block_head = namedtuple(
        'Block_Head', 'hash timestamp case_id item_id state length')
    block_data = namedtuple('Block_Data', 'data')

    to_initiate = initiate(file_path)
        
    fp = open(file_path, 'rb')

    while True:

        try:
            head_content = fp.read(block_head_format.size)
            curr_block_head = block_head._make(
                block_head_format.unpack(head_content))
            block_data_format = struct.Struct(
                str(curr_block_head.length)+'s')
            data_content = fp.read(curr_block_head.length)
            curr_block_data = block_data._make(
                block_data_format.unpack(data_content))

            prev_hash = hashlib.sha1(head_content+data_content).digest()

            if int(item_id[0]) == curr_block_head.item_id:
                case_id = curr_block_head.case_id
                state = curr_block_head.state
        except:
            break

    fp.close()

    try:


        if state.decode('utf-8').rstrip('\x00') == "CHECKEDOUT":

            now = datetime.now()

            timestamp = datetime.timestamp(now)
            head_values = (prev_hash, timestamp, case_id, int(
                item_id[0]), str.encode("CHECKEDIN"), 0)
            data_value = b''
            block_data_format = struct.Struct('0s')
            packed_head_values = block_head_format.pack(*head_values)
            packed_data_values = block_data_format.pack(data_value)
            curr_block_head = block_head._make(
                block_head_format.unpack(packed_head_values))
            curr_block_data = block_data._make(
                block_data_format.unpack(packed_data_values))

            # print(curr_block_head, curr_block_data)

            fp = open(file_path, 'ab')
            fp.write(packed_head_values)
            fp.write(packed_data_values)
            fp.close()

            print("Case:", str(uuid.UUID(bytes=case_id)))
            print("Checked in item:", item_id[0])
            print("\tStatus:", "CHECKEDIN")
            print("\tTime of action:", now.strftime(
                '%Y-%m-%dT%H:%M:%S.%f') + 'Z')

            success = True
        
        else:
            Incorrect_State()

    except:
        # Item ID not found
        Item_Not_Found()
        
    sys.exit(0)

