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

            if emission_n.get(tag, None) == None: #emission
                emission_n[tag] = 1
            else:
                emission_n[tag] += 1
            tag_dict = emission.get(tag, None)
            if tag_dict == None:
                temp = {word: 1}
                emission[tag] = temp
            else:
                if tag_dict.get(word, None) == None:
                    tag_dict[word] = 1
                else:
                    tag_dict[word] += 1

            if i == 0: continue #skip transition for first one
            prev_tag = s[i - 1][1] 
            if transition.get((tag, prev_tag), None) == None:
                transition[(tag, prev_tag)] = 1
            else:
                transition[(tag, prev_tag)] += 1

    #decoding
    ans = []
    e_alpha = 1.0   #smoothing constant for emission
    s_alpha = 1.0   #smoothing constant for start
    t_alpha = 1.0   #smoothing constant for transition

    for s in test:
        v, b = [], []
        curr_ans = []
        for k in range(len(s)):
            tags = list(emission_n.keys())
            v_curr, b_curr = [], []
            word = s[k][0]

            max_v, best_t = 0, 0
            for tB in range(len(tags)):  
                tag = tags[tB]
                #values for emission smoothing
                e_V, s_V = len(emission[tag].keys()), len(start.keys())
                e_denom, s_denom = emission_n[tag] + e_alpha * (e_V + 1), len(s) + s_alpha * (s_V + 1)

                if k == 0:
                    curr_v = 0
                    if start.get(tag, None) == None:
                        curr_v = math.log(s_alpha / s_denom)
                    else:
                        curr_v = math.log((s_alpha + start[tag]) / s_denom) #each sentence has one starting word
                        
                    if emission[tag].get(word, None) == None: #smoothing for emission
                        curr_v += math.log(e_alpha / e_denom)
                    else:
                        curr_v += math.log((e_alpha + emission[tag][word]) / e_denom)

                    v_curr.append(curr_v)
                    b_curr.append(tag)
                else:
                    t_V = len(transition.keys())
                    t_denom = len(s) - 1 + t_alpha * (t_V + 1) #total num of transitions is len(s) - 1

                    for tA in range(len(tags)):
                        curr_v  = v[k - 1][tA]

                        if transition.get((tag, tags[tA]), None) == None:
                            curr_v += math.log(t_alpha / t_denom)
                        else:
                            curr_v += math.log(transition[(tag, tags[tA])] / t_denom)

                        if emission[tag].get(word, None) == None:
                            curr_v += math.log(e_alpha / e_denom)
                        else:
                            curr_v += math.log((e_alpha + emission[tag][word]) / e_denom)

                        if curr_v > max_v:
                            max_v = curr_v
                            best_t = tB

                    v_curr.append(max_v)
                    b_curr.append(best_t)

            v.append(v_curr)
            b.append(b_curr)
        
        #find best one in last row
        best_idx, best_odds = 0, v[len(s) - 1][0]
        for t in range(1, len(tags)):
            if v[len(s) - 1][t] > best_odds:
                best_odds = v[len(s) - 1][t]
                best_idx  = t
        
        #backtrack 
        tags = list(emission_n.keys())
        curr_idx = best_idx
        curr_s_tags = []
        for i in range(len(s) - 2, -2, -1):
            curr_s_tags.append(tags[curr_idx])
            curr_idx = b[i][curr_idx]

        curr_s_tags.reverse()
        
        for i in range(len(s)):
            curr_ans.append((s[i][0], curr_s_tags[i]))
        
        ans.append(curr_ans)
    return ans