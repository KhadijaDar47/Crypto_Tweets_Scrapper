import datetime
import re
from bs4 import BeautifulSoup
import requests
import os
import csv
import twitterScraper as t
import scrapingInterface as s

All_Coins = []


def CoinScrapper():
    try:
        soup = BeautifulSoup(requests.get("https://www.coingecko.com/en/crypto-gainers-losers?time=y1").content,
                             'html.parser')
        table = soup.find('table')
        class_name = "lg:tw-flex font-bold tw-items-center tw-justify-between"
        elements = table.find_all(class_=re.compile(r'\b' + re.escape(class_name) + r'\b'))
        print("\033[32mList of all Top Gainer Coins\n\033[0m")
        for i, element in enumerate(elements, start=1):
            content = element.get_text(strip=True)
            All_Coins.append((i, content))
            print("\033[36m{}. {}\033[0m".format(i, content))
        return True
    except Exception as e:
        print("Error in getting coin list:", str(e))


# Function to save all the coins
def SaveAllCoins():
    try:
        filename = "Files\\All_Coins.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Index", "Top Gainers"])
            writer.writerows(All_Coins)

        print("Data saved to", filename)
    except Exception as e:
        print("Error in saving all Coins:", str(e))


def Save_Selected_Coin():
    try:
        CoinSelect = input("\033[32m\nWrite the index of the coin you want to scrap: \033[0m")
        # Check if the user's input is a valid index
        if CoinSelect.isdigit() and int(CoinSelect) <= len(All_Coins):
            selected_index = int(CoinSelect) - 1
            selected_coin = All_Coins[selected_index]
            print(f"\033[33m\nYou Selected: {selected_coin[1]} \033[0m")
            s.Time(selected_coin[1])
        else:
            print("\033[31mInvalid Input. Enter Valid Index\033[0m")

    except Exception as e:
        print("Error in Saving Selected Coin:", str(e))


def MultipleCoin(selected_indices):
    selected_coins = []
    for index in selected_indices:
        if index <= len(All_Coins):
            coin_index = index - 1
            selected_coin = All_Coins[coin_index][1]
            selected_coins.append((index, selected_coin))

    
    while True:
        fromTweets = input("\033[32m\nEnter the start date for your tweets (YYYY-MM-DD):\033[0m ")
        toTweets = input("\033[32m\nEnter the end date for your tweets (YYYY-MM-DD):\033[0m ")

        # Check if the formats of the "from" and "to" dates are different
        if len(fromTweets) != 10 or len(toTweets) != 10 or fromTweets.count('-') != 2 or toTweets.count('-') != 2:
            print("\033[31m\nError: Invalid date format. Please use the format 'YYYY-MM-DD'.\033[0m")
        else:
            break
    for index, coin in selected_coins:
        print(f"Scrapping Coin: {coin}")
        t.TwitterScraper("{} until:{} since:{}".format(coin,toTweets, fromTweets),coin)

    return selected_coins


if __name__ == "__main__":
   

            folder_path = "Files"
            os.makedirs(folder_path, exist_ok=True)
            if CoinScrapper():
                while True:
                    CoinSelect = input("\033[32m\nPress 1 to select Multiple Coins.\nPress 2 to select a specific Coin.\n"
                                    "Press 3 to select the top-gained coin:\n\033[0m")
                    if CoinSelect == "1":
                        selected_indices = input("\033[32m\nEnter the indices of the coins you want to select (separated by spaces): \033[0m")
                        selected_indices = [int(index) for index in selected_indices.split() if index.isdigit()]
                        if selected_indices:
                            MultipleCoin(selected_indices)
                        else:
                            print("\033[31mInvalid Input. Enter Valid Indices\033[0m")
                    elif CoinSelect == "2":
                        Save_Selected_Coin()
                    elif CoinSelect == "3":
                        coin_index = 1  
                        selected_coin = All_Coins[coin_index - 1][1]
                        print(f"\033[33m\nTop Gainer is: {selected_coin} \033[0m")
                        s.Time(selected_coin)
                    else:
                        print("\033[31mInvalid Input.\033[0m")
   



            
        

           
        
