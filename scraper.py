import requests #import the libraries used for web scraping, data handling, and time management
from bs4 import BeautifulSoup
import json
import csv
import time

URL = "https://www.bbc.com/news" # website URL to scrape headlines 

headers = {
    "User-Agent": "Mozilla/5.0" #browser to check 
}

def scrape_headlines(keyword=None): #function to scrape headlines
    try:
        response = requests.get(URL, headers=headers) #send request to the website with specified headers
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        headlines = []

        articles = soup.find_all("a") #find all links in the webpage

        for article in articles:
            title = article.get_text(strip=True) #extract the text of the link 
            link = article.get("href")

            if title and link:

                if link.startswith("/"):
                    link = "https://www.bbc.com" + link

                if keyword:
                    if keyword.lower() not in title.lower():
                        continue

                headlines.append({ #store headlines information
                    "title": title,
                    "url": link,
                    "time": "N/A"
                })

        return headlines

    except Exception as e:
        print("Error occurred:", e)
        return []


def save_json(data): #function to save data in JSON file
    with open("headlines.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def save_csv(data): #function to save data in CSV file
    with open("headlines.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "url", "time"])
        writer.writeheader()
        writer.writerows(data)


def main(): #main method

    keyword = input("Enter keyword to filter (or press Enter to skip): ")

    headlines = scrape_headlines(keyword)

    print("\nTop Headlines:\n")

    for i, news in enumerate(headlines[:10], 1): #this loop prints 1st ten headlines with their links
        print(f"{i}. {news['title']}")
        print(f"   Link: {news['url']}\n")

    save_json(headlines)
    save_csv(headlines)

    print("Saved to headlines.json and headlines.csv")

    time.sleep(2) #sleep for 2 seconds before ending the program


if __name__ == "__main__":
    main()