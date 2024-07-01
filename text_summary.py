import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Samsung Group or simply Samsung is a South Korean multinational manufacturing conglomerate 
headquartered in Samsung Digital City, Suwon, South Korea. It comprises numerous affiliated businesses, most 
of them united under the Samsung brand, and is the largest South Korean chaebol (business conglomerate).
 As of 2020, Samsung has the eighth highest global brand value. Samsung was founded by Lee Byung-chul in 1938 as 
 a trading company. Over the next three decades, the group diversified into areas including food processing, 
 textiles, insurance, securities, and retail. Samsung entered the electronics industry in the late 1960s and the 
 construction and shipbuilding industries in the mid-1970s; these areas would drive its subsequent growth. 
 Following Lee's death in 1987, Samsung was separated into five business groups  Samsung Group, Shinsegae Group, 
 CJ Group and Hansol Group, and JoongAng Group."""


def summarizer(rawdocs, selected_len):
    stopwords = list(STOP_WORDS)
    #print(stopwords)

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)

    no_of_words = sum(1 for token in doc if token.is_alpha)

    tokens = [token.text for token in doc]
    #print(tokens)

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] +=1
    #print(word_freq)

    if word_freq:
        max_freq = max(word_freq.values())
        for word in word_freq.keys():
            word_freq[word] = word_freq[word] / max_freq
    else:
        max_freq = 1

    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    #print(sent_scores)

    total_len = len(sent_tokens)
    #print(total_len)

    select_len = int(selected_len)
    #print(select_len)

    summary = nlargest(select_len, sent_scores, key = sent_scores.get)
    #print(summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    if selected_len is not None and selected_len > total_len:
        selected_len = total_len
        no_of_words = len(summary.split(' '))
    
    # print(text)
    # print('\n')
    # print(summary)
    # print("Length of original text ", len(text.split(' ')))
    # print("Length of Summary", len(summary.split(' ')))

    return summary, doc, no_of_words, len(summary.split(' ')), select_len, total_len

summarizer(text, 5)