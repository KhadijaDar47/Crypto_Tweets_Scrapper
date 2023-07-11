from twitterScraper import TwitterScraper
import datetime

def Time(coin):
    current_date = datetime.datetime.now().date()
    while True:
        fromTweets = input("\033[32m\nEnter the start date for your tweets (YYYY-MM-DD or YYYY/MM/DD):\033[0m ")
        try:
            start_date = datetime.datetime.strptime(fromTweets, "%Y-%m-%d").date()
        except ValueError:
            try:
                start_date = datetime.datetime.strptime(fromTweets, "%Y/%m/%d").date()
            except ValueError:
                print("\033[31m\nError: Invalid start date format.\033[0m")
                continue

        if start_date > current_date:
            print(f"\033[31m\nError: Start date ({start_date}) cannot be greater than the current date ({current_date}).\033[0m")
            continue

        while True:
            toTweets = input("\033[32m\nEnter the end date for your tweets (YYYY-MM-DD or YYYY/MM/DD):\033[m ")
            try:
                end_date = datetime.datetime.strptime(toTweets, "%Y-%m-%d").date()
            except ValueError:
                try:
                    end_date = datetime.datetime.strptime(toTweets, "%Y/%m/%d").date()
                except ValueError:
                    print("\033[31m\nError: Invalid end date format.\033[0m")
                    continue
            break

        if end_date > current_date:
            print(f"\033[31m\nError: End date ({end_date}) cannot be greater than the current date ({current_date}).\033[0m")
            continue

        if end_date > start_date + datetime.timedelta(days=182):
            print("\033[31m\nError: The gap between the start and end dates should be less than 6 months.\033[0m")
            continue

            

        break

    print("\033[33m\nStart date:", start_date.strftime("%Y-%m-%d"), "\033[0m")
    print("\033[33mEnd date:", end_date.strftime("%Y-%m-%d"), "\033[0m")
    TwitterScraper("{} until:{} since:{}".format(coin, toTweets, fromTweets), coin)

