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

#returns two lists of the probabilities of each doc being pos / being neg

def naive_bayes_probs(train_set, train_labels, dev_set, laplace=0.0015, pos_prior=0.8,silently=False):
    # Keep this in the provided template
    # print_paramter_vals(laplace,pos_prior)

    #0 is negative, 1 is positive
    #remember to use log and sums instead of products

    #populate frequency dicts and count uniques for pos & neg
    unique_count_pos, unique_count_neg = 0, 0   #count of unique words for pos and neg train sets
    len_pos, len_neg = 0, 0                     #num of seen words in pos & neg sets
    freqs_pos, freqs_neg = {}, {}               #dicts to store frequencies of words in pos & neg train sets

    #training phase
    for i in range(len(train_set)):
        curr_set   = train_set[i]
        curr_label = train_labels[i]

        if curr_label == 0: #negative
            len_neg += len(curr_set)
            for word in curr_set:
                if freqs_neg.get(word) == None:
                    freqs_neg[word] = 1
                    unique_count_neg += 1
                else:
                    freqs_neg[word] += 1
        else:
            len_pos += len(curr_set)
            for word in curr_set:
                if freqs_pos.get(word) == None:
                    freqs_pos[word] = 1
                    unique_count_pos += 1
                else:
                    freqs_pos[word] += 1

    #development phase: calc P(Type = p|Words) and P(Type = n|Words) for EACH REVIEW
    pos_probs = []
    neg_probs = []

    # for doc in tqdm(dev_set,disable=silently):
    for doc in dev_set:
        #calculate odds for pos and neg of curr doc
        prob_pos, prob_neg = math.log(pos_prior), math.log(1 - pos_prior)
        for word in doc:
            curr_odds_pos, curr_odds_neg = 0, 0
            if freqs_pos.get(word) == None: #not found in positive
                curr_odds_pos = laplace / (len_pos + laplace * (unique_count_pos + 1))
            else:
                curr_odds_pos = (freqs_pos[word] + laplace) / (len_pos + laplace * (unique_count_pos + 1))
            
            if freqs_neg.get(word) == None: #not found in positive
                curr_odds_neg = laplace / (len_neg + laplace * (unique_count_neg + 1))
            else:
                curr_odds_neg = (freqs_neg[word] + laplace) / (len_neg + laplace * (unique_count_neg + 1))

            prob_pos += math.log(curr_odds_pos)
            prob_neg += math.log(curr_odds_neg)

        pos_probs.append(prob_pos)
        neg_probs.append(prob_neg)
    
    return (pos_probs, neg_probs)

"""
You can modify the default values for the Laplace smoothing parameter and the prior for the positive label.
Notice that we may pass in specific values for these parameters during our testing.
"""

def naiveBayes(train_set, train_labels, dev_set, laplace=0.0015, pos_prior=0.8,silently=False):
    # Keep this in the provided template
    print_paramter_vals(laplace,pos_prior)

    yhats = []
    probs = naive_bayes_probs(train_set, train_labels, dev_set, laplace, pos_prior, silently)
    pos_probs, neg_probs = probs[0], probs[1]

    i = 0
    for doc in tqdm(dev_set,disable=silently):
        if pos_probs[i] >= neg_probs[i]: yhats.append(1)
        else:                         yhats.append(0)
        i += 1

    return yhats


# Keep this in the provided template
def print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior):
    print(f"Unigram Laplace {unigram_laplace}")
    print(f"Bigram Laplace {bigram_laplace}")
    print(f"Bigram Lambda {bigram_lambda}")
    print(f"Positive prior {pos_prior}")


# main function for the bigrammixture model
def bigramBayes(train_set, train_labels, dev_set, unigram_laplace=0.0015, bigram_laplace=1.0, bigram_lambda=1.0,pos_prior=0.8, silently=False):

    # Keep this in the provided template
    print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior)

    #0 is negative, 1 is positive
    #remember to use log and sums instead of products

    #populate frequency dicts and count uniques for pos & neg
    #keys to dict are now tuples of words (word1, word2)
    unique_count_pos, unique_count_neg = 0, 0   #count of unique words for pos and neg train sets
    len_pos, len_neg = 0, 0                     #num of seen words in pos & neg sets
    freqs_pos, freqs_neg = {}, {}               #dicts to store frequencies of words in pos & neg train sets

    #training phase
    for i in range(len(train_set)): 
        curr_set   = train_set[i]
        curr_label = train_labels[i]

        if curr_label == 0: #negative
            len_neg += len(curr_set) - 1
            for j in range(len(curr_set) - 1):               #look at consecutive pairs of words
                curr_key = (curr_set[j], curr_set[j + 1])
                if freqs_neg.get(curr_key) == None:
                    freqs_neg[curr_key] = 1
                    unique_count_neg += 1
                else:
                    freqs_neg[curr_key] += 1
        else:
            len_pos += len(curr_set) - 1
            for word in curr_set:
                curr_key = (curr_set[j], curr_set[j + 1])
                if freqs_pos.get(curr_key) == None:
                    freqs_pos[curr_key] = 1
                    unique_count_pos += 1
                else:
                    freqs_pos[curr_key] += 1

    naive_probs = naive_bayes_probs(train_set, train_labels, dev_set, unigram_laplace, pos_prior, silently)
    naive_pos_probs, naive_neg_probs = naive_probs[0], naive_probs[1]

    #development phase: calc P(Type = p|Words) and P(Type = n|Words) for EACH REVIEW
    yhats = []
    i = 0
    for doc in tqdm(dev_set,disable=silently):
        #calculate odds for pos and neg of curr doc
        prob_pos, prob_neg = math.log(pos_prior), math.log(1 - pos_prior)
        for j in range(len(doc) - 1): #every pair of words in curr doc
            curr_key = (doc[j], doc[j + 1])
            curr_odds_pos, curr_odds_neg = 0, 0
            if freqs_pos.get(curr_key) == None: #not found in positive
                curr_odds_pos = bigram_laplace / (len_pos + bigram_laplace * (unique_count_pos + 1))
            else:
                curr_odds_pos = (freqs_pos[word] + bigram_laplace) / (len_pos + bigram_laplace * (unique_count_pos + 1))
            
            if freqs_neg.get(curr_key) == None: #not found in positive
                curr_odds_neg = bigram_laplace / (len_neg + bigram_laplace * (unique_count_neg + 1))
            else:
                curr_odds_neg = (freqs_neg[word] + bigram_laplace) / (len_neg + bigram_laplace * (unique_count_neg + 1))
            
            prob_pos += math.log(curr_odds_pos)
            prob_neg += math.log(curr_odds_neg)
        
        #combine with naive_bayes
        combined_prob_pos = (1 - bigram_lambda) * naive_pos_probs[i] + bigram_lambda * prob_pos
        combined_prob_neg = (1 - bigram_lambda) * naive_neg_probs[i] + bigram_lambda * prob_neg

        if combined_prob_pos >= combined_prob_neg: yhats.append(1)
        else                                     : yhats.append(0) 

        i += 1

    return yhats

