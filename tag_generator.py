#!/usr/bin/env python

'''
tag_generator.py
This script creates tags for your Jekyll blog hosted by Github page.
No plugins required.
'''

import glob
import os

post_dir = 'pinned/_posts/'
archive_post_dir = 'archive/_posts/'
tag_dir = 'tag/'

filenames = glob.glob(post_dir + '*markdown')
filenames.extend(glob.glob(archive_post_dir + '*markdown'))

total_tags = []
for filename in filenames:
    f = open(filename, 'r')
    crawl = False
    for line in f:
        if crawl:
            current_tags = line.strip().split()
            if current_tags[0] == 'tags:':
                total_tags.extend(current_tags[1:])
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_tags = set(total_tags)

old_tags = glob.glob(tag_dir + '*.markdown')
for tag in old_tags:
    os.remove(tag)
    
if not os.path.exists(tag_dir):
    os.makedirs(tag_dir)

for tag in total_tags:
    tag_filename = tag_dir + tag + '.markdown'
    f = open(tag_filename, 'a')
    write_str = '---\nlayout: tag_layout\ntitle: \"Tag: ' + tag + '\"\ntag: ' + tag + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()
print("Tags generated, total current", total_tags.__len__())