"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""

import math
def viterbi_1(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    #create dictionaries for Pe, Ps, Pt

    #Pe: P(wi | ti) = P(witi) / P(ti)
    emission, start, transition = {}, {}, {} #dict of dict like baseline
    #emission: key = tag, value = dict, key = word, value = freq
    #start: key = tag, val = freq, only tracks when at start
    #transition: key = (tag_k, tag_k-1), val = freq
    emission_n = {} #key: tag, value: # of words of the tag
    #emission: k = tag, v = dict --> dict: k = word, v = freq
    #so P(wi | ti) = emission[tag][word] / 
    for s in train: 
        for i in range(len(s)):
            word, tag = s[i][0], s[i][1]
            if i == 0: #start
                if start.get(tag, None) == None:
                    start[tag] = 1
                else:
                    start[tag] += 1
                start = False

            if emission_n.get(tag, None) == None: #emission
                emission_n[tag] = 1
            else:
                emission_n[tag] += 1
            tag_dict = emission.get(tag, None)
            if tag_dict == None:
                tag_dict[tag] = {word: 1}
            else:
                tag_dict[tag] += 1

            if i == 0: continue #skip transition for first one
            prev_tag = s[i - 1][1] 
            if transition.get((tag, prev_tag), None) == None:
                transition[(tag, prev_tag)] = 1
            else:
                transition[(tag, prev_tag)] += 1

    #decoding
    ans = []
    for s in test:
        v, b = [], []
        for k in range(len(s)):
            tags = list(start.keys())
            v_curr, b_curr = [], []
            word = s[k][0]

            max_v = 0, best_t = tags[0]
            for tB in range(len(tags)):  
                tag = tags[tB]
                if k == 0:
                    v_curr.append(math.log(start[tag]) + math.log(emission[tag][word]))
                    b_curr.append(tag)
                else:
                    for tA in range(len(tags)):
                        curr_v  = math.log(v[k - 1][tA]) 
                        curr_v += math.log(transition[(tag, tags[tA])])
                        curr_v += math.log(emission[tag][word])

                        if curr_v > max_v:
                            max_v = curr_v
                            best_t = tags[tB]

                    v_curr.append(max_v)
                    b_curr.append(best_t)

            v.append(v_curr)
            b.append(b_curr)
        
        #find best one in last row
        best_idx = 0, best_odds = v[len(s) - 1][0]
        for t in range(1, len(tags)):
            if v[len(s) - 1][t] > best_odds:
                best_odds = v[len(s) - 1][t]
                best_idx  = t

        best_end_tag = tags[best_idx]
        #backtrack 
        
        
    return ans