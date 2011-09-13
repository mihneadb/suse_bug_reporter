import re
import sys
from operator import itemgetter


def sortByKeywords(bug_list, keyword_list, rel_threshold):
    ''' scans the strings for the keywords and computes a relevance for each
    string by the following formula: if the keyword is matched exactly, it adds
    to the relevance the length of the keyword times two; if a keyword is
    matched partially in a word (i.e. 'crash' in 'crashes') it adds the length
    of the keyword;
    after all that is done, it sorts the string list by relevance
    
    ! it only returns the bugs with the relevance above the
    max_relevance * rel_threshold, so the latter must be a float between
    0 and 1 '''

    if keyword_list == [] or keyword_list == ():
        return bug_list

    # ignored words; len() has to be >= 3
    IGNORED = ('for',)


    # make sure the threshold makes sense
    if type(rel_threshold) != int and type(rel_threshold) != float:
        print "wrong relevance threshold! Must be int or float, between 0 and 1"
        sys.exit(1)
    elif rel_threshold < 0 or rel_threshold > 1:
        print "wrong relevance threshold! Must be int or float, between 0 and 1"
        sys.exit(1)

    toSort = list()
    max_relevance = 0

    for bug in bug_list:
        s = bug.summary.lower()
        s = re.findall(r'[\w_-]+', s)
        sum = 0
        kw_matched = 0
        for keyword in keyword_list:
            if (len(keyword) < 3) or (keyword in IGNORED):
                continue
            if keyword in s:
                # the keyword is matched exactly
                sum += len(keyword) * 2
                kw_matched += 1
                continue
            # check to see if the keyword matches partially
            for word in s:
                if keyword in word:
                    sum += len(keyword)
                    kw_matched += 1
        if sum != 0:
            sum += 5 ** kw_matched
            if max_relevance < sum:
                max_relevance = sum
            toSort.append((bug, sum))

    toSort_sorted = sorted(toSort, key=itemgetter(1), reverse=True)
    sorted_bug_list = [item[0] for item in toSort_sorted 
            if item[1] >= (max_relevance * rel_threshold)]
    return sorted_bug_list

