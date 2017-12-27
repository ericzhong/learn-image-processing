#!/usr/bin/env python3

import os


def get_segment_name(val):
    name = {'0xd8': 'SOI',
            '0xdb': 'DQT',
            '0xc0': 'SOF0',
            '0xc4': 'DHT',
            '0xda': 'SOS',
            '0xd9': 'EOI'}
    if 0 == val:
        return 'compressed'
    elif 0xe0 <= val <= 0xef:
        return 'APP%s' % int(val-0xe0)
    key = hex(val)
    if key in name:
        return name[key]
    else:
        return key


def get_header(f):
    f.seek(0, 0)
    return f.read(2)


def get_trailer(f):
    f.seek(-2, os.SEEK_END)
    return f.read(2)


def get_segments(f):
    segments = []
    f.seek(-2, os.SEEK_END)
    end = f.tell() 
    f.seek(2, 0)
    while True:
        if f.tell() >= end:
            break

        # skip all 0xff between segments
        while True:
            if f.read(1)[0] != 0xff:
                f.seek(-1, os.SEEK_CUR)
                break
        
        header = f.read(3)
        type = header[0]
        size = int.from_bytes(header[1:], byteorder='big')
        data = f.read(size-2)   # minus 2-bytes for size
        segments.append({'type':type, 'size':size, 'data': data})
    return segments


# Within SOF0 segment (0xc0)
def get_image_size(seg_data):
    height = int.from_bytes(seg_data[1:3], byteorder='big')
    width = int.from_bytes(seg_data[3:5], byteorder='big')
    return height,width


# Within SOF0 segment (0xc0)
def get_data_precision(seg_data):
    return int.from_bytes(seg_data[0:1], byteorder='big')


def find_first_segment_data(segments, type):
    for s in segments:
        if s['type'] == type:
            return s['data']
    return None


if __name__ == "__main__":
    with open('dog.jpg','rb') as f:
        print("Header: %s\n" % get_header(f))

        segments = get_segments(f)
        for s in segments:
            print("Segment %s" % get_segment_name(s['type']))
            print("  Size: %s\n" % s['size'])
    
        print("Trailer: %s\n" % get_trailer(f))

        sof0_data = find_first_segment_data(segments, 0xc0)
        h, w = get_image_size(sof0_data)
        print("Image size: %sx%s" % (w, h))
        dp = get_data_precision(sof0_data)
        print("Data precision: %s" % dp)

    print("\nDone.")

