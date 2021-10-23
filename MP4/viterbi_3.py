"""
Part 4: Here should be your best version of viterbi, 
with enhancements such as dealing with suffixes/prefixes separately
"""


#takes a word and guesses a suitable tag
def tag_guesser(word, curr_tag):
    if word.endswith('ing'):
        return 'VERB'
    # elif word.endswith('ly') and hapax.get('ADV', None) != None:
    #     return 'ADV'
    # elif word.startswith('$') and hapax.get('NOUN', None) != None:
    #     return 'NOUN'
    else:
        return curr_tag

import math
def viterbi_3(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    #create dictionaries for Pe, Ps, Pt
    #Pe: P(wi | ti) = P(witi) / P(ti)
    emission, transition = {}, {} #dict of dict like baseline
    #emission: key = tag, value = dict, key = word, value = freq
    #transition: key = prev tag, value = dict, key = tag, value = freq
    emission_n, transition_n = {}, {} #key: tag, value: # of words of the tag
    #emission: k = tag, v = dict --> dict: k = word, v = freq
    #so P(wi | ti) = emission[tag][word] 

    total_words = 0 #used for START & END for laplace smoothing
    for s in train: 
        for i in range(len(s)):
            total_words += 1

            word, tag = s[i][0], s[i][1]
            if emission_n.get(tag, None) == None: #total counts in emission for each tag
                emission_n[tag] = 1
            else:
                emission_n[tag] += 1

            tag_dict = emission.get(tag, None)
            if tag_dict == None:
                emission[tag] = {word: 1}
            else:
                if tag_dict.get(word, None) == None:
                    emission[tag][word] = 1
                else:
                    emission[tag][word] += 1

            if i == 0: continue #skip transition for first one
            prev_tag = s[i - 1][1] 

            if transition_n.get(prev_tag, None) == None: #total transitions for each prev tag
                transition_n[prev_tag] = 1
            else:
                transition_n[prev_tag] += 1

            trans_dict = transition.get(prev_tag, None)
            if trans_dict == None:
                transition[prev_tag] = {tag: 1}
            else:
                if trans_dict.get(tag, None) == None:
                    transition[prev_tag][tag] = 1
                else:
                    transition[prev_tag][tag] += 1

    #map hapax words to X-WORDS
    tags = list(emission_n.keys())
    hapax = {}
    hapax_n = 0
    #prob of a hapax word given a tag = hapax[tag] / hapax_n
    # print(tags)

    f = open("hapax_dump.txt", "w") #dump hapax values
    for tag in tags:
        for word in emission[tag]:
            if emission[tag][word] != 1: continue 

            if hapax.get(tag, None) == None:
                hapax[tag] = 1
            else:
                hapax[tag] += 1

            f.write(str(word) + "=" + str(tag) + "\n")
            hapax_n += 1

    f.close()
    print("hapax dump complete")

    #decoding
    ans = []
    e_alpha = 0.01  #smoothing constant for emission
    # s_alpha = 1.0   #smoothing constant for start
    t_alpha = 0.001 #smoothing constant for transition
    h_alpha = 0.00001 #smoothing for hapax

    for s in test:
        v, b = [], []
        for k in range(len(s)):
            # print(tags)
            v_curr, b_curr = [], []
            word = s[k]

            for tagB in tags:  
                #values for emission smoothing
                #only 1 start/end for each document
                scaled_e_alpha = len(s) / total_words #only 1 start/end for each document
                if hapax.get(tagB, None) != None: #tag = START or END, never in hapax
                    scaled_e_alpha = e_alpha * (hapax[tagB] / hapax_n)

                e_V = len(emission[tagB].keys())
                e_denom = emission_n[tagB] + scaled_e_alpha * (e_V + 1)
                
                if k == 0:
                    #start
                    if emission[tagB].get('START', None) == None:
                        curr_v = math.log(scaled_e_alpha / e_denom)
                    else:
                        curr_v = math.log((scaled_e_alpha + emission[tagB]['START']) / e_denom)
                        
                    if emission[tagB].get(word, None) == None: #smoothing for emission
                        guessed_tag = tag_guesser(word, tagB)
                        if hapax.get(guessed_tag, None) == None:
                            scaled_e_alpha *= h_alpha
                        else:
                            scaled_e_alpha *= (hapax[guessed_tag] / hapax_n)
                        curr_v += math.log(scaled_e_alpha / e_denom)
                    else:
                        curr_v += math.log((scaled_e_alpha + emission[tagB][word]) / e_denom)

                    v_curr.append(curr_v)
                    b_curr.append(-1)
                    
                else:
                    max_v, best_t = float('-inf'), 0
                    #emission probs don't depend on tagA

                    for tA in range(len(tags)):
                        tagA = tags[tA]
                        curr_v = v[k - 1][tA]
                        if transition.get(tagA, None) == None: #tagA = END usually
                            curr_v += math.log(0.0001) #set to some tiny value
                        else:
                            t_V = len(transition[tagA].keys())
                            t_denom = transition_n[tagA] + t_alpha * (t_V + 1) 
                            if transition[tagA].get(tagB, None) == None:
                                curr_v += math.log(t_alpha / t_denom)
                            else:
                                curr_v += math.log((t_alpha + transition[tagA][tagB]) / t_denom)

                        if curr_v > max_v:
                            max_v = curr_v
                            best_t = tA

                    if emission[tagB].get(word, None) == None: #unseen word given the tag
                        guessed_tag = tag_guesser(word, tagB)
                        if hapax.get(guessed_tag, None) == None:
                            scaled_e_alpha *= h_alpha
                        else:
                            scaled_e_alpha *= (hapax[guessed_tag] / hapax_n)
                        max_v += math.log(scaled_e_alpha / e_denom)
                    else:
                        max_v += math.log((scaled_e_alpha + emission[tagB][word]) / e_denom)

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

        curr_idx = best_idx
        curr_s_tags = [tags[curr_idx]]

        for i in range(len(s) - 1, 0, -1):
            curr_idx = b[i][curr_idx]
            curr_s_tags.append(tags[curr_idx])

        curr_s_tags.reverse()

        curr_ans = []
        for i in range(len(s)):
            curr_ans.append((s[i], curr_s_tags[i]))
        ans.append(curr_ans)
    return ans