"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""


# import heapq
def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    tag_freqs = {}  #dict of dict, key = word, value = (freqs, most_common), 
                    #freqs is dict of key = tag for the word, value = frequency
                    #most_common is the most common tag
    overall_most_common =  ("", 0) #used for unseens later
    overall_tag_freqs = {} #dict where keys = all tags, value = freq

    for s in train:
        for word in s:
            curr_word, curr_tag = word[0], word[1]
            curr_word_pair = tag_freqs.get(curr_word, None)
            if overall_tag_freqs.get(curr_tag, None) == None:
                overall_tag_freqs[curr_tag] = 1
            else:
                overall_tag_freqs[curr_tag] += 1
            if overall_most_common[1] < overall_tag_freqs[curr_tag]:
                overall_most_common = (curr_tag, overall_tag_freqs[curr_tag])

            if curr_word_pair == None: #check if word exists in dict
                curr_word_tags = {}
                curr_word_tags[curr_tag] = 1
                tag_freqs[curr_word] = (curr_word_tags, curr_tag)
            else: 
                curr_word_tags = curr_word_pair[0]
                most_common    = curr_word_pair[1]
                if curr_word_tags.get(curr_tag, None) == None: #check if tag exists in word
                    curr_word_tags[curr_tag] = 1
                else:
                    curr_word_tags[curr_tag] += 1

                #update most common
                if curr_word_tags[most_common] < curr_word_tags[curr_tag]:
                    tag_freqs[curr_word] = (curr_word_tags, curr_tag)

    # for key in tag_freqs:
    #     print(key, tag_freqs[key])


    ans = []

    for s in test:
        curr = []
        for word in s:
            if tag_freqs.get(word, None) == None:
                curr.append((word, overall_most_common[0]))
            else:
                curr.append((word, tag_freqs[word][1]))
        ans.append(curr)

    return ans