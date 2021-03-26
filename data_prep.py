import pandas as pd

# ---------------- #
# WSB CLEANUP
# ---------------- #

reddit = pd.read_csv("raw_data/reddit_wsb.csv")
reddit.body = reddit.body.fillna('')
reddit.title = reddit.title.fillna('')
reddit['fulltext'] = reddit.apply(lambda x: ' '.join([x['title'],x['body']]).lower(), axis=1)

reddit["mentions_GME"] = reddit.apply(lambda x: 1 if ("gme" in x["fulltext"] or "gamestop" in x["fulltext"]) else 0, axis=1)

reddit['date']= pd.to_datetime(reddit['timestamp'])
reddit['date']=reddit['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

reddit_subset = reddit[['date','mentions_GME']]
reddit_sums = reddit_subset.groupby('date')['mentions_GME'].sum().reset_index()
reddit_sums = reddit_sums[reddit_sums.date >= "2021-02-08"]
reddit_sums = reddit_sums[reddit_sums.date <= "2021-03-25"]

reddit_sums.to_csv("data/reddit_wsb_new.csv",index=False)

# ---------------- #
# GME STOCK CLEANUP
# ---------------- #

stock = pd.read_csv("raw_data/GME_stock.csv")
idx = pd.period_range(min(stock.Date), max(stock.Date))
stock.set_index('Date',inplace=True)
idx_string = [str(x) for x in idx]
stock = stock.reindex(idx_string, fill_value=5000000)
stock.reset_index(inplace=True)

stock = stock[stock.Date >= "2021-02-08"]
stock = stock[stock.Date <= "2021-03-25"]

stock.to_csv("data/GME_stock_new.csv",index=False)