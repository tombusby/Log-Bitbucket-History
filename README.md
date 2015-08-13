Log Bitbucket History
=======

I find Bitbucket's RSS feed of recent history is a good tool when preparing invoices for clients. However, it only provides a limited number of the most recent items. These simple scripts are intended to allow a cron job to keep a permanent record by appending new items to an existing log as they appear.

It's up to you how often you run your script, but I would suggest that once every 24h is probably sufficient.

The scripts comes in two flavours: one which produces a CSV, and one which produces an HTML table. The latter preserves the links and formatting which are present in the summary section of the feed.

Usage: `./logger_csv.py <user_id> <token>`

`<user_id>` and `<token>` come from the URL of the RSS feed:

https://bitbucket.org/some_user/rss/feed?token=abcdef

`<user_id>` in this instance is some_user and `<token>` is abcdef

It's pretty scrappy, so any bugs, feel free to let me know.
