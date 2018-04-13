# RedditScore
Package for performing Reddit-based text analysis

Includes:
- Document tokenizer with myriads of options, including Reddit- and Twitter-specific options
- Tools to build and tune most popular text classification models without any hassle
- Instruments to help you build more efficient Reddit-based models and to obtain RedditScores
- Tools to use pre-built Reddit-based models to obtain RedditScores for your data

Full documentation lives here: http://redditscore.readthedocs.io

Tokenizer usage:

	from redditscore.tokenizer import CrazyTokenizer
	trump_rant = "@realDonaldTrump #fucktrump WHO ELECTED this Guy?! 😭'"
	tokenizer = CrazyTokenizer(ignorestopwords='english', splithashtags=True, neg_emojis=True, hashtags=False)
	tokenizer.tokenize_doc(trump_rant)

	Output:
	['TOKENTWITTERHANDLE', 'fuck', 'trump', 'WHO', 'ELECTED', 'guy', 'NEG_EMOJI']


Model usage:

  import os

  import pandas as pd

  from redditscore import tokenizer, models

  df = pd.read_csv(os.path.join('redditscore', 'reddit_small_sample.csv'))
  tokenizer = CrazyTokenizer(urls='domain', splithashtags=True)
  df['tokens'] = df['body'].apply(tokenizer.tokenize)
  X = df['tokens']
  y = df['subreddit']

  multi_model = sklearn.SklearnModel(
      model_type='multinomial', alpha=0.1, random_state=24, tfidf=False, ngrams=2)
  fasttext_model = fasttext.FastTextModel(minCount=5, epoch=15)

  multi_model.tune_params(X, y, cv=5, scoring='neg_log_loss')
  fasttext_model.fit(X, y)


To install package:

	pip install git+https://github.com/crazyfrogspb/RedditScore.git

To perform complete installation with all features:

	pip install git+https://github.com/crazyfrogspb/RedditScore.git#egg=redditscore[nltk,neural_nets,fasttext]

To cite:

    {
      @misc{Nikitin2018,
      author = {Nikitin, E.},
      title = {RedditScore},
      year = {2018},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/crazyfrogspb/RedditScore}}
    }
