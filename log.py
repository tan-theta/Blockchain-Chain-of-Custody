import os
import struct
import hashlib
import uuid
from error import *
from datetime import datetime
from collections import namedtuple


def log(reverse, number, case_id, item_id, file_path):
    # if(reverse):
    #     print(reverse)
    # if(number):
    #     print(number)
    # if(case_id):
    #     print(case_id)
    # if(item_id):
    #     print(item_id)
    # exit(0)
    # state = ''
    # prev_hash = b''
    # case_id = ''


    block_head_format = struct.Struct('20s d 16s I 11s I')
    block_head = namedtuple('Block_Head', 'hash timestamp case_id item_id state length')
    block_data = namedtuple('Block_Data', 'data')
    blocks=[]
    fp = open(file_path, 'rb')

    while True:

        try:
            head_content = fp.read(block_head_format.size)
            curr_block_head = block_head._make(block_head_format.unpack(head_content))
            block_data_format = struct.Struct(str(curr_block_head.length) + 's')
            data_content = fp.read(curr_block_head.length)
            curr_block_data = block_data._make(block_data_format.unpack(data_content))
            # prev_hash = hashlib.sha1(head_content + data_content).digest()
            blocks.append((curr_block_head,curr_block_data))

        except:
            # print("Last Block Recorded")
            break

    fp.close()

    # print(case_id)
    if(reverse):
        # blocks_to_be_displayed = blocks[:]
        # blocks_to_be_displayed.reverse()
        blocks.reverse()
    if(case_id):
        i=0
        while(i<len(blocks)):

            caseid = b""
            rev_case_id = blocks[i][0].case_id
            for j in range(0, len(rev_case_id)):
                caseid = bytes([rev_case_id[j]]) + caseid
            case = str(uuid.UUID(bytes=caseid))

            if(case != case_id):
                blocks.pop(i)
            else:
                i+=1
    if(item_id):
        i=0
        while(i<len(blocks)):
            if(str(blocks[i][0].item_id) not in item_id):
                blocks.pop(i)
            else:
                i+=1
    if(number):
        i=int(number)
        while(i<len(blocks)):
            blocks.pop(i)


    # ctr=0
    for block in blocks:
        # print("Block Head")
        # for j in i[0]:
        #     print(j)
        # print("Block Data")
        # for j in i[1]:
        #     print(j)
        # print()
        # print()
        caseid=b""
        rev_case_id = block[0].case_id
        for i in range(0,len(rev_case_id)):
            caseid=bytes([rev_case_id[i]]) + caseid

        
        print("Case:",uuid.UUID(bytes=caseid))
        print("Item:",block[0].item_id)
        action = ""
        for i in block[0].state.decode():
            if(i.isalpha()):
                action+=i
        print("Action:",action)
        date = str(datetime.fromtimestamp(block[0].timestamp)).split()[0]
        time = str(datetime.fromtimestamp(block[0].timestamp)).split()[1]
        date_time = date+"T"+time+"Z"

        print("Time:",date_time)
        print()
