"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""

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
    #emission: key = type, value = dict, key = word, value = freq
    #start: key = type, val = freq, only tracks when at start
    emission_n = {} #key: type, value: # of words of the type
    #emission: k = tag, v = dict --> dict: k = word, v = freq
    #so P(wi | ti) = emission[tag][word] / 
    for s in train: 
        for pair in s:
            word, tag = pair[0], pair[1]
            if emission_n.get(tag, None) == None:
                emission_n[tag] = 1
            else:
                emission_n[tag] += 1
            
            type_dict = emission.get(tag, None)
            if type_dict == None:
                type_dict[tag] = {word: 1}
            else:
                type_dict[tag] += 1






    return []