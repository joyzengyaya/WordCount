#!/usr/bin/env python2.7
import numpy as np
import re, string, pdb
import collections

def analysis_text(text=None, filename=None):
  
  if text is not None:
    contents = text
  elif filename is not None:
    f = open(filename, 'r')
    contents = f.read()
    f.close()
  
  words = []
  sentences = []
  
  contents = contents.lower()
  contents = contents.replace('\n', ' ')
  sentences = [s.strip() for s in re.split('[\.\?!]' , contents) if s.strip()]
  for i in range(len(sentences)):
    sentences[i] = ''.join(c for c in sentences[i] if c not in string.punctuation)
  
  for sentence in sentences:
    words.extend(sentence.split())
  
  word_count = len(words)
  unique_word = len(set(words))
  sent_count = len(sentences)
  avg_sent_len = word_count / float(sent_count)
  words_by_desc_frequency = collections.Counter(words)
  
  
  def sentenceToGrams(sentence, k):
    """
    Return a list of k-grams in a sentence.
    """
    words = sentence.split()
    n = len(words)
    return [tuple(words[i:i + k]) for i in range(n - k + 1)]
    
  def sentencesToGramCounter(sentences, k, whitelist=None):
    """
    Return a dictionary with key the k-gram tuples, and value the count
    If whitelist is None, search exhaustively for all k-grams.
    If whitelist is given, then only look at k-grams, whose (k-1)-gram is inside the whitelist, i.e. A-priori algorithm is used.
    """
    rtn = collections.defaultdict(int)
    if not whitelist:
      for sentence in sentences:
        grams = sentenceToGrams(sentence, k)
        for gram in grams:
          rtn[gram] += 1
    else:
      # A-priori algorithm
      for sentence in sentences:
        words = sentence.split()
        n = len(words)
        for i in range(n - k + 1):
          if tuple(words[i:i + k - 1]) in whitelist and tuple(words[i + 1:i+k]) in whitelist:
            rtn[tuple(words[i:i + k])] += 1
    return rtn

  k = 3
  # Using A-priori
  all_grams_apriori = []
  gram_counter = None
  while True:
    gram_counter = sentencesToGramCounter(sentences, k, whitelist=gram_counter)
    k += 1
    if not gram_counter:
      break
    else:
      for gram in gram_counter:
        if gram_counter[gram] >= 3:
          all_grams_apriori.append(gram)
  
  return (sentences, words, word_count, unique_word, \
          sent_count, avg_sent_len, words_by_desc_frequency, all_grams_apriori)  

if __name__ == "__main__":
  choice = ''
  while not (choice == '1' or choice == '2'):
    choice = raw_input('Please choose 1 for raw text and 2 for text filename (only enter a number, 1 or 2):')
    if not (choice == '1' or choice == '2'):
      print 'please only enter a number, 1 or 2'
  
  if choice == '1':
    text = raw_input('Please enter the text:')
    filename = None
  elif choice == '2':
    text = None
    filename = raw_input('Please enter the text file name:')
    
  words, sentences, word_count, unique_word, \
  sent_count, avg_sent_len, words_by_desc_frequency, all_grams_apriori = analysis_text(text = text, filename = filename)
  #print words
  #print sentences
  print 'Total word count: {word_count}'.format(word_count = word_count)
  print 'Unique words: {unique_word}'.format(unique_word = unique_word)
  print 'Total sentences: {sent_count}'.format(sent_count = sent_count)
  print 'Average sentences length in words: {avg_sent_len}'.format(avg_sent_len = avg_sent_len)
  print 'Words in order of descending frequency:'
  print words_by_desc_frequency
  print 'Frequently used phrases:'
  print all_grams_apriori
  
  
  
  
  
  