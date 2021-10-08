# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
import numpy as np
import math
from tqdm import tqdm
from collections import Counter
import reader

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


"""
  load_data calls the provided utility to load in the dataset.
  You can modify the default values for stemming and lowercase, to improve performance when
       we haven't passed in specific values for these parameters.
"""
 
def load_data(trainingdir, testdir, stemming=False, lowercase=True, silently=False):
    print(f"Stemming is {stemming}")
    print(f"Lowercase is {lowercase}")
    train_set, train_labels, dev_set, dev_labels = reader.load_dataset(trainingdir,testdir,stemming,lowercase,silently)
    return train_set, train_labels, dev_set, dev_labels


# Keep this in the provided template
def print_paramter_vals(laplace,pos_prior):
    print(f"Unigram Laplace {laplace}")
    print(f"Positive prior {pos_prior}")

#returns a dict with the frequency of all words given type
def naive_bayes_freqs(train_set, train_labels, doc_type):
    freq = {}
    n = 0       #number of words given type
    for i in range(len(train_set)):
        if train_labels[i] == doc_type:
            n += len(train_set[i])
            for word in train_set[i]:
                if freq.get(word) == None:
                    freq[word] = 1
                else:
                    freq[word] += 1
    
    return (freq, n)

def naive_probs(pos_freqs, neg_freqs, pos_n, neg_n, dev_set, laplace, pos_prior):
    pos_probs, neg_probs = [], []
    for doc in dev_set:
        pos_prob, neg_prob = math.log(pos_prior), math.log(1 - pos_prior)
        for word in doc:
            curr_pos, curr_neg = 0, 0
            if pos_freqs.get(word) == None:
                curr_pos = laplace / (pos_n + laplace * (len(pos_freqs) + 1))
            else:
                curr_pos = (pos_freqs[word] + laplace) / (pos_n + laplace * (len(pos_freqs) + 1))
            
            if neg_freqs.get(word) == None:
                curr_neg = laplace / (neg_n + laplace * (len(neg_freqs) + 1))
            else:
                curr_neg = (neg_freqs[word] + laplace) / (neg_n + laplace * (len(neg_freqs) + 1))

            pos_prob += math.log(curr_pos)
            neg_prob += math.log(curr_neg)

        pos_probs.append(pos_prob)
        neg_probs.append(neg_prob)

    return (neg_probs, pos_probs)

"""
You can modify the default values for the Laplace smoothing parameter and the prior for the positive label.
Notice that we may pass in specific values for these parameters during our testing.
"""

def naiveBayes(train_set, train_labels, dev_set, laplace=0.0015, pos_prior=0.8, silently=False):
    # Keep this in the provided template
    print_paramter_vals(laplace,pos_prior)

    pos_data = naive_bayes_freqs(train_set, train_labels, 1)
    neg_data = naive_bayes_freqs(train_set, train_labels, 0)

    pos_freqs, pos_n = pos_data[0], pos_data[1]
    neg_freqs, neg_n = neg_data[0], neg_data[1]

    probs = naive_probs(pos_freqs, neg_freqs, pos_n, neg_n, dev_set, laplace, pos_prior, silently)

    ans = []
    for i in tqdm(range(len(dev_set)),disable=silently):
        if probs[0][i] >= probs[1][i]:
            ans.append(0)
        else:
            ans.append(1)

    return ans

# Keep this in the provided template
def print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior):
    print(f"Unigram Laplace {unigram_laplace}")
    print(f"Bigram Laplace {bigram_laplace}")
    print(f"Bigram Lambda {bigram_lambda}")
    print(f"Positive prior {pos_prior}")

def bigram_freqs(train_set, train_labels, doc_type):
    freq = {}
    n = 0
    for i in range(len(train_set)):
        if train_labels[i] == doc_type:
            n += len(train_set[i]) - 1
            for j in range(len(train_set[i]) - 1):
                curr_key = (train_set[i][j], train_set[i][j + 1]) 
                if freq.get(curr_key) == None:
                    freq[curr_key] = 1
                else:
                    freq[curr_key] += 1
    
    return (freq, n)

def bigram_probs(pos_freqs, neg_freqs, pos_n, neg_n, dev_set, laplace, pos_prior):
    pos_probs, neg_probs = [], []

    for doc in dev_set:
        pos_prob, neg_prob = math.log(pos_prior), math.log(1 - pos_prior)
        for i in range(len(doc) - 1):
            curr_pos, curr_neg = 0, 0
            curr_key = (doc[i], doc[i + 1])
            if pos_freqs.get(curr_key) == None:
                curr_pos = laplace / (pos_n + laplace * (len(pos_freqs) + 1))
            else:
                curr_pos = (pos_freqs[curr_key] + laplace) / (pos_n + laplace * (len(pos_freqs) + 1))
            
            if neg_freqs.get(curr_key) == None:
                curr_neg = laplace / (neg_n + laplace * (len(neg_freqs) + 1))
            else:
                curr_neg = (neg_freqs[curr_key] + laplace) / (neg_n + laplace * (len(neg_freqs) + 1))

            pos_prob += math.log(curr_pos)
            neg_prob += math.log(curr_neg)

        pos_probs.append(pos_prob)
        neg_probs.append(neg_prob)

    return (pos_probs, neg_probs)

# main function for the bigrammixture model
def bigramBayes(train_set, train_labels, dev_set, unigram_laplace=0.0009, bigram_laplace=0.00337, bigram_lambda=0.6785,pos_prior=0.8, silently=False):
    # Keep this in the provided template
    print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior)
    
    pos_data = naive_bayes_freqs(train_set, train_labels, 1)
    neg_data = naive_bayes_freqs(train_set, train_labels, 0)

    pos_freqs, pos_n = pos_data[0], pos_data[1]
    neg_freqs, neg_n = neg_data[0], neg_data[1]

    unigram_probs = naive_probs(pos_freqs, neg_freqs, pos_n, neg_n, dev_set, unigram_laplace, pos_prior, silently)

    

