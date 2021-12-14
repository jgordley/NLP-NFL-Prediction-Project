# NLP Fall 2021 Final Project
NFL win prediction using Twitter sentiment analysis.
John Gordley

Please see `Final_Report.pdf` for a detailed report of the entire project motivation, methods, experiments, and conclusion.
## Part 1 - Data Acquisition
Credit to [Kevin Gimpel](https://home.ttic.edu/~kgimpel/) and his initial work on this problem, as well as the [dataset he made publicly available](https://home.ttic.edu/~kgimpel/).  Please see the `README.md` in the folder `nfl-tweets-v1.0` for more information on this dataset. 

### Twitter Data
The dataset provided by Kevin Gimpel contains id's of 930000 weekly tweets from the 2012 NFL season. Weekly tweets are described as " those that occurred at least 12 hours after the start of the previous game and 1 hour before the start of the upcoming game for their assigned team."

To gather the text content of these Tweets, I signed up for a [Twitter Developer Account](https://developer.twitter.com/en) and used the [GET endpoint for multiple Tweets by id](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets) (which is limited to 100 ids per request and ~280 requests per 15 minute window). Located in the file `tweet_scraping.ipynb` is my code to gather these tweets until I hit the 15 minute time limit, then sleep for 15 minutes and resume tweet collection until all tweets are collected. 

Interestingly, as these tweets are almost 9 years old, many of them had been deleted or their accounts were no longer public and so the tweet content could not be gathered. 545705 out of 930000 tweets were public, available, and collected, for an overall percentage of 58.7%. A JSON dictionary mapping tweet id's to their text content can be found in the file `tweet_ids_0_to_930000`.

### NFL Game Data
Although the Kevin Gimpel dataset included total points and winner of each game, I wanted to use more specific game information to make a prediction for each team. I built a web scraper (utilizing [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)) to go to [TeamRankings](https://www.teamrankings.com/nfl/stat/passing-yards-per-game?date=2012-09-19) and gather passing-yards-per-game, points-per-game, rushing-yards-per-game, and turnover-margin-per-game for each team, for each week of the 2012 NFL season. The scraper I made is located in `game_data_crawler.ipynb`. In my prediction, I use the average over the previous 3 games for each prediction, and in the case of week 1 where there are no previous games, I use the previous season 2011 average for each stat. The game information I scraped is stored in `2012-passing-yards-per-game.csv`, `2012-points-per-game.csv`, `2012-rushing-yards-per-game.csv`, and `2012-turnover-margin-per-game.csv`.
## Part 2 - Baseline Prediction
I gathered all the game data I had collected and used the file `baseline.ipynb` to combine all of it into a single file (including which team won, who was home and away, etc.) `all_game_data.csv`. The columns are as follows:
* home (which team was home i.e. BUF)
* away (which team was away i.e. PIT)
* week (week # of the season 1-16)
* home_pass (avg passing yards for the home team over the last 3 games)
* away_pass (avg passing yards for the away team over the last 3 games)
* home_rush (avg rushing yards for the home team over the last 3 games)
* away_rush (avg rushing yards for the away team over the last 3 games)
* home_points (avg points scored for the home team over the last 3 games)
* away_points (avg points scored for the away team over the last 3 games)
* home_turnover (avg turnover margin for the home team over the last 3 games)
* away_turnover (avg turnover margin for the away team over the last 3 games)
* home_win (the value to be predicted, 1 if the home team won and 0 if they lost)

Using this aggregated data, in `baseline_prediction.ipynb` I scaled each column using [Sci-kit learn's MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html) and then ran a simple [Sci-kit learn KNeighbors Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html) on the data, resulting in the following accuracies for K values between 1 and 26:

![K value graph](baseline_k_values.JPG?raw=true "K values vs Accuracy")

The best value for K I determined to be 18, with an accuracy of **64.5%** and so I decided to go with this for my baseline. Pretty good accuracy for only a few simple pregame stats!

## Part 3 - Sentiment Classification
To understand more about how to build a sentiment classifier to use on the tweets I collected, I completed the Coursera course [Natural Language Processing with Classification and Vector Spaces](https://www.coursera.org/learn/classification-vector-spaces-in-nlp) by Younes Bensouda Mourri from Stanford. Here, I learned how to build the Naive Bayes model for classification that learns Tweet sentiment based on the [NLTK](https://www.nltk.org/) twitter dataset. The model I build can be found in `naive_bayes_sentiment_classifier.py`. The `utils.py` file was created and given by this course, I did not modify it in any way, so credit to Professor Mourri for that and for the basic skeleton on creating a Naive Bayes classifier from scratch. 

## Part 4 - Sentiment Prediction
For my sentiment implementation, I tried out 2 different ways of generating a sentiment score for each team (home and away):
1. Aggregate method (`sentiment_prediction.ipynb`) - sum up the naive bayes predicted p value for each team to get a total score for each team
2. Proportion method (`sentiment_prediction_proportion.ipynb`) - tally the number of positive and negative tweets for each team and use the proportion of positive to negative tweets as the score

For both score methods, I tried out using only the `home_sentiment` and `away_sentiment` to predict a winner. Then, I moved on to combine the `home_sentiment` and `away_sentiment` scores with the rest of the previous game data I had collected to predict a winner. The resulting accuracies for each method combination is shown below in the table:

![accuracy chart](accuracies.JPG?raw=true "Method Accuracies")

The optimal K values for each method are also shown below in the table:

![optimal K](optimal_k.JPG?raw=true "Optimal K Values")

These results are extremely encouraging because they show that both sentiment scores hold promise for predicting a winner. Even the proportion score which appears to perform slightly worse than the aggregate score seems to give information on who the likely winner will be. Combined with game data, both methods of sentiment scoring elevate the model accuracy above the baseline I set with only game data at 64.5%! I am very happy with the results of these experiments. Please see the `Final_Report.pdf` for more analysis and thank you for checking out my projecT!