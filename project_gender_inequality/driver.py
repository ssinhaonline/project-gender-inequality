#!/usr/bin/env python

import itertools
import urllib2
from threading import Thread
from math import ceil
import RMP_prof_info_collector as Rinfo
import RMP_link_manager as Rlink
import RMP_prof_comments_collector as Rcomment
from pdb import set_trace
#from tqdm import tqdm
from json import dumps

THREADS = 250

temp_URLS = list()
for link in Rlink.read_by_lines('../fixtures/RMP_prof_urls.txt'):
    temp_URLS.append(link)
URLS = list(set(temp_URLS))

#URLS = (
#    'www.ratemyprofessors.com/ShowRatings.jsp?tid=150122',
#    'www.ratemyprofessors.com/ShowRatings.jsp?tid=1010230'
#    )

def divide_list(full_list, N):
    """
    Takes a full list of elements and returns a list of lists with N partitions
    """
    partitioned_list = list()
    if(len(full_list) % N == 0):
        one_slice = len(full_list) / N
        for i in range(0, len(full_list), one_slice):
            partitioned_list.append(full_list[i : i + one_slice])
    else:
        one_slice = (len(full_list) - (len(full_list) % (N - 1))) / (N - 1)
        loop_last = (len(full_list) - (len(full_list) % (N - 1)))
        for i in range(0, loop_last, one_slice):
            partitioned_list.append(full_list[i : i + one_slice])
        partitioned_list.append(full_list[loop_last : len(full_list)])
    return partitioned_list

def main():
    NEW_URLS = tuple(divide_list(URLS, THREADS))
    #total = 0
    for i in range(THREADS):
       t = Agent(NEW_URLS[i])
       print 'Starting thread ' + str(i)
       t.start()
       print 'Stopping thread' + str(i)
       #print len(NEW_URLS[i])
       #total += len(NEW_URLS[i])
    #print total


class Agent(Thread):
    def __init__(self, urls): #, threadID):
        Thread.__init__(self)
        self.urls = urls
        #self.threadID = threadID

    def run(self):
        urls = self.urls #itertools.cycle(self.urls) 
        #tid = self.threadID
        #thread_data = list()
        for this_url in urls:
            #this_url = urls.next()
            #count += 1
            #print count
            f = open('../fixtures/all_jsons/prof_' + Rinfo.get_prof_id(this_url) + '.json', 'w')
            try:
                prof_soup = Rlink.scrape_prof_info(this_url)
                rpan_soup = Rlink.reduce_to_rpanel(prof_soup)
            except:
                continue
            prof_id = Rinfo.get_prof_id(this_url)
            name = Rinfo.get_prof_name(rpan_soup)
            details = Rinfo.get_prof_details(rpan_soup)
            ratings = Rinfo.get_prof_ratings(rpan_soup)
            top_tags = Rinfo.get_top_tags(rpan_soup)
            comments = Rcomment.get_prof_comments(prof_id)
            prof_dict = {   'id': prof_id,
                            'name': name,
                            'details': details,
                            'ratings':ratings,
                            'top 20 tags': top_tags,
                            'all comments': comments 
                        }
            #thread_data.append(prof_dict)
            f.write(dumps(prof_dict))
            f.close()

if __name__ == '__main__':
    set_trace()
    main()