"""
Tests for making sure that CrazyTokenizer works as expected
Author: Evgenii Nikitin <e.nikitin@nyu.edu>
Part of https://github.com/crazyfrogspb/RedditScore project

Copyright (c) 2018 Evgenii Nikitin. All rights reserved.
This work is licensed under the terms of the MIT license.
"""

import re

from redditscore.tokenizer import CrazyTokenizer

trump_rant = '@realDonaldTrump #fucktrump WHO ELECTED this Guy?! 😭'
doc_emoji = '😍 😭 😩???!!!!'
vova_text = 'Vladimir Putin is the BEST AND AMAZING'
norm_text = 'eeeeeeeeboy this shiiit is good'
quotes_text = '"PBR is the best beer" - said no one ever'
stem_text = 'who has stolen my vodka friends'
punct_text = "this is the text, which contains a lot of punctuation!!! amazing, isn't it? who knows..."
break_text = """I
love
linebreaks"""
nonunicode_text = "no love for russian language пиздец товарищи 😭"
decontract_text = "I've been waiting to drink this beer! I won't give it to you"
hashtag_text = "#makeamericagreatagain #makerussiadrunkagain #MAGA"
replacement_text = "http://fscorelab.ru is number 1 site according to @crazyfrogspb. http://www.google.com"
replacement_text2 = "en919@nyu.edu was hacked by u/AngryConservative from /r/The_Donald #americanhacking"
spartak_text = "Spartak is a champion! Spartalke is the best!"
english_stop = "for on you"
russian_stop = "привет, я Женя"
story_of_my_life = """
    Hi, my name is @crazyfrogspb. I loooove beer. Plato once said - "He was a wise man who invented beer".
    Not a bad way to phrase it. #anotherpintplease
    by the way, don't forget to visit https://github.com/crazyfrogspb/RedditScore.
    I'm also on Reddit as u/crazyfrogspb. I especially love /r/machinelearning
    Sending my love to you. As they say - "stay safe"! ❤ 24
    """
url_text = "I always go to http://rt.com to chat about politics, http://forums.news.cnn.com/ sucks man"
short_url_text = "JOBS, JOBS, JOBS! Unemployment claims have fallen to a 45-year low. https://t.co/pN2TE5HDQm"
untokenized_text = "Rats are actually more polite in New York City than in Los Angeles"


def test_emoji():
    tokenizer = CrazyTokenizer(
        pos_emojis=True, neg_emojis=True, neutral_emojis=True)
    tokens = tokenizer.tokenize(doc_emoji)
    assert tokens == ['POS_EMOJI', 'NEG_EMOJI', 'NEG_EMOJI']


def test_repeated():
    tokenizer = CrazyTokenizer(
        pos_emojis=True, neg_emojis=True, neutral_emojis=True)
    for i in range(100):
        tokenizer.tokenize(trump_rant)


def test_lowercase_keepcaps():
    tokenizer = CrazyTokenizer(lowercase=True, keepcaps=True)
    tokens = tokenizer.tokenize(vova_text)
    assert tokens == ['vladimir', 'putin',
                      'is', 'the', 'BEST', 'AND', 'AMAZING']
    tokenizer = CrazyTokenizer(lowercase=True, keepcaps=False)
    tokens = tokenizer.tokenize(vova_text)
    assert tokens == ['vladimir', 'putin',
                      'is', 'the', 'best', 'and', 'amazing']
    tokenizer = CrazyTokenizer(lowercase=False, keepcaps=False)
    tokens = tokenizer.tokenize(vova_text)
    assert tokens == ['Vladimir', 'Putin',
                      'is', 'the', 'BEST', 'AND', 'AMAZING']


def test_normalize():
    tokenizer = CrazyTokenizer(normalize=3)
    tokens = tokenizer.tokenize(norm_text)
    assert tokens == ['eeeboy', 'this', 'shiiit', 'is', 'good']
    tokenizer = CrazyTokenizer(normalize=2)
    tokens = tokenizer.tokenize(norm_text)
    assert tokens == ['eeboy', 'this', 'shiit', 'is', 'good']


def test_ignorequotes():
    tokenizer = CrazyTokenizer(ignorequotes=True, removepunct=True)
    tokens = tokenizer.tokenize(quotes_text)
    assert tokens == ['said', 'no', 'one', 'ever']


def test_stop():
    tokenizer = CrazyTokenizer(ignorestopwords=[
                               'vladimir', 'putin', 'and'], lowercase=False)
    tokens = tokenizer.tokenize(vova_text)
    assert tokens == ['is', 'the', 'BEST', 'AMAZING']
    tokenizer = CrazyTokenizer(ignorestopwords='english')
    tokens = tokenizer.tokenize(english_stop)
    assert tokens == []
    tokenizer = CrazyTokenizer(ignorestopwords='russian')
    tokens = tokenizer.tokenize(russian_stop)
    assert tokens == ['привет', 'женя']


def test_stem():
    tokenizer = CrazyTokenizer(stem='stem')
    tokens = tokenizer.tokenize(stem_text)
    assert tokens == ['who', 'ha', 'stolen', 'my', 'vodka', 'friend']


def test_removepunct():
    tokenizer = CrazyTokenizer(removepunct=True)
    tokens = tokenizer.tokenize(punct_text)
    print(tokens)
    assert tokens == ['this', 'is', 'the', 'text', 'which', 'contains', 'a',
                      'lot', 'of', 'punctuation', 'amazing', "isn't", 'it', 'who', 'knows']


def test_removebreaks():
    tokenizer = CrazyTokenizer(removebreaks=True)
    tokens = tokenizer.tokenize(break_text)
    assert tokens == ['i', 'love', 'linebreaks']


def test_remove_nonunicode():
    tokenizer = CrazyTokenizer(remove_nonunicode=True)
    tokens = tokenizer.tokenize(nonunicode_text)
    assert tokens == ['no', 'love', 'for', 'russian', 'language']


def test_decontract():
    tokenizer = CrazyTokenizer(decontract=True)
    tokens = tokenizer.tokenize(decontract_text)
    assert tokens == ['i', 'have', 'been', 'waiting', 'to', 'drink',
                      'this', 'beer', 'i', 'will', 'not', 'give', 'it', 'to', 'you']


def test_splithashtags():
    tokenizer = CrazyTokenizer(splithashtags=True, hashtags=False)
    tokens = tokenizer.tokenize(hashtag_text)
    assert tokens == ['make', 'america', 'great', 'again',
                      'make', 'russia', 'drunk', 'again', 'maga']


def test_replacement():
    tokenizer = CrazyTokenizer(twitter_handles='handle', urls='url', hashtags='hashtag',
                               numbers='number', subreddits='subreddit', reddit_usernames='redditor',
                               emails='email')
    tokens = tokenizer.tokenize(replacement_text)
    assert tokens == ['url', 'is', 'number', 'number',
                      'site', 'according', 'to', 'handle', 'url']
    tokens = tokenizer.tokenize(replacement_text2)
    assert tokens == ['email', 'was', 'hacked', 'by',
                      'redditor', 'from', 'subreddit', 'hashtag']


def test_extra_patterns():
    tokenizer = CrazyTokenizer(extra_patterns=[('zagovor', re.compile(
        ('([S,s]partak|[S,s]paratka|[S,s]partalke)')), 'GAZPROM')])
    tokens = tokenizer.tokenize(spartak_text)
    assert tokens == ['GAZPROM', 'is', 'a',
                      'champion', 'GAZPROM', 'is', 'the', 'best']


def test_tokenizing():
    tokenizer = CrazyTokenizer(lowercase=True, keepcaps=True, normalize=3, ignorequotes=True, ignorestopwords=['is', 'are', 'am', 'not', 'a', 'the'],
                               stem=False, removepunct=True, removebreaks=True, remove_nonunicode=False, decontract=False,
                               splithashtags=True, twitter_handles='TOKENTWITTERHANDLE', urls='', hashtags=False,
                               numbers=False, subreddits='TOKENSUBREDDIT', reddit_usernames='TOKENREDDITOR',
                               emails='TOKENEMAIL', extra_patterns=None, pos_emojis=True, neg_emojis=None, neutral_emojis=None)

    tokens = tokenizer.tokenize(story_of_my_life)
    correct_answer = ['hi', 'my', 'name', 'TOKENTWITTERHANDLE', 'I', 'looove', 'beer', 'plato', 'once', 'said', 'bad', 'way', 'to',
                      'phrase', 'it', 'another', 'pint', 'please', 'by', 'way', "don't", 'forget', 'to', 'visit', "i'm", 'also', 'on',
                                      'reddit', 'as', 'TOKENREDDITOR', 'I', 'especially', 'love', 'TOKENSUBREDDIT', 'sending', 'my', 'love', 'to', 'you',
                                      'as', 'they', 'say', 'POS_EMOJI', '24']
    assert tokens == correct_answer


def test_batch_tokenizing():
    documents = [story_of_my_life, russian_stop,
                 english_stop, vova_text, spartak_text]
    tokenizer = CrazyTokenizer(decontract=True)
    all_tokens = tokenizer.tokenize_docs(documents, batch_size=2, n_threads=2)
    assert len(all_tokens) == len(documents)


def test_url_tokenizing():
    tokenizer = CrazyTokenizer(urls='domain')
    tokens = tokenizer.tokenize(url_text)
    assert tokens == ['i', 'always', 'go', 'to', 'rt', 'to',
                      'chat', 'about', 'politics', 'cnn', 'sucks', 'man']


def test_url_unwrapping():
    tokenizer = CrazyTokenizer(urls='domain_unwrap')
    tokens = tokenizer.tokenize(short_url_text)
    assert tokens == ['jobs', 'jobs', 'jobs', 'unemployment', 'claims',
                      'have', 'fallen', 'to', 'a', '45-year',
                      'low', 'bloomberg']


def test_url_fast_unwrapping():
    tokenizer = CrazyTokenizer(urls='domain_unwrap_fast')
    tokens = tokenizer.tokenize(short_url_text)
    assert tokens == ['jobs', 'jobs', 'jobs', 'unemployment', 'claims',
                      'have', 'fallen', 'to', 'a', '45-year',
                      'low', 'bloomberg']


def test_url_title():
    tokenizer = CrazyTokenizer(urls='title')
    tokens = tokenizer.tokenize("http://google.com")
    assert tokens == ['google']


def test_keep_untokenized():
    tokenizer = CrazyTokenizer(
        keep_untokenized=['New York City', 'Los Angeles'])
    tokens = tokenizer.tokenize(untokenized_text)
    assert tokens == ['rats', 'are', 'actually', 'more', 'polite',
                      'in', 'new_york_city', 'than', 'in', 'los_angeles']
