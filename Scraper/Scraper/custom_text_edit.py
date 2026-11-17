import json
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from googletrans import Translator
from Crypto_nlp.Load_to_GCP import load
from time import sleep
from io import StringIO

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


#####################
# After scraping, each sentence has single quotes because they are in separate <p> positions, it is in .json file in the form of a dictionary where
# keys are article_name and the value is the article_text, the value for article_text is a list
# Output of the customtextfunc function is a .csv file which is in the form of a dictionary with only outer quotes
# The article_translation output is a translated text
#####################

###################### Below function opens the .json file, changes text in lists into one strig and saves it in Scraped_data_no_quotes2.csv file.
# Does the same thing for article title, assigns id's to articles and appends links
def customtextfunc(file):
    # Read file and create DataFrame
    with open(f'{file}', 'r', encoding='utf8') as f:
        data = f.read()
    df = data.replace('][', ',')
    data = pd.read_json(StringIO(df))

    # Function to convert list to string
    def listToString(s):
        # initialize an empty string
        str1 = " "
        return (str1.join(s))

    # Convert article_text column to string and create DataFrame
    article_text_df = pd.DataFrame()
    for i, text in enumerate(data['article_text']):
        data_string = listToString(text)
        replaced_string = " ".join(data_string.split())
        data_df = pd.DataFrame(data=[replaced_string], columns=["article_text"])
        article_text_df = article_text_df.append(data_df)
        if i > 0:
            article_text_df.to_csv(
                r'C:/Users/Jacklord/PycharmProjects/Crypto_nlp/Crypto_nlp/Scraper/Scraper/spiders/Scraped_data_no_quotes_2.csv',
                index=False, header=True)

    article_name_df1 = pd.DataFrame()
    for i, name in enumerate(data["article_name"]):
        article_name_df = pd.DataFrame(data=[name], columns=["article_name"])
        article_name_df1 = article_name_df1.append(article_name_df)

    article_name_df1.reset_index(inplace=True)

    article_link = pd.DataFrame(data['article_link'])

    article_name_df1 = pd.concat([article_link, article_name_df1], axis=1).drop(columns=['index'])
    article_name_df1['id'] = int()

    # #ID generator - for now not used
    # def count_non_digits(s):
    #     count = 0
    #     for i in range(len(s)):
    #         if not s[i].isdigit():
    #             count = count + 1
    #
    #     return count


    # Below code assigns values from the ids list to the id column of the article_name_df1 dataframe. If the index of the
    # current element is less than the length of the ids list, the element is assigned the value at the corresponding
    # index in the ids list. Otherwise, it is assigned the last value in the ids list.
    ids = [1049, 1108, 1026, 1077, 1069, 1055]
    article_name_df1['id'] = [ids[i] if i < len(ids) else ids[-1] for i, c in enumerate(article_name_df1['article_name'])]

    article_name_df1.insert(0, 'id', article_name_df1.pop("id"))
    ##########################


    ########################## Below code joins two .csv files into one

    article_name_df1.to_csv(
        r'C:/Users/Jacklord/PycharmProjects/Crypto_nlp/Crypto_nlp/Scraper/Scraper/spiders/Scraped_data_no_quotes1.csv',
        index=False, header=True)

    article_name_df = pd.read_csv('C:/Users/Jacklord/PycharmProjects/Crypto_nlp/Crypto_nlp/Scraper/Scraper/spiders/Scraped_data_no_quotes1.csv', encoding="utf8")

    article_text_df = pd.read_csv('C:/Users/Jacklord/PycharmProjects/Crypto_nlp/Crypto_nlp/Scraper/Scraper/spiders/Scraped_data_no_quotes2.csv', encoding="utf8")

    df_total = pd.concat([article_name_df, article_text_df], axis=1)

    #Here empty Scraped_data.csv file is created
    filename = "C:/Users/Jacklord/PycharmProjects/Crypto_nlp/Crypto_nlp/Scraper/Scraper/spiders/Scraped_data.csv"
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    f.close()

    df_total.to_csv(filename, index=False, header=True)

    # load(filename, 'article')
    print("The original text is cleared, saved as Scraped_data.csv and thrown into the article table" )
##########################


########################## Below code translates original text to english
def article_translation(file):

    df=pd.read_csv("C:/Users/Jacklord/PycharmProjects/Crypto_nlp/Crypto_nlp/Scraper/Scraper/spiders/Scraped_data.csv", encoding="utf8")

    ########################## translation function
    def translate(string):
        translator = Translator()
        text_str_translated = translator.translate(string, src='auto', dest='en')
        return text_str_translated.text

    article_link = pd.DataFrame(df['article_link'])
    id_df = pd.DataFrame(df['id'])
    text_translated_df1 = pd.DataFrame(columns=["article_text"])
    article_name_translated_df1 = pd.DataFrame(columns=["article_name"])

    for i, row in df.iterrows():
        # text_translated_df1 = text_translated_df1.append({"article_text": translate(row["article_text"])},
        #                                                  ignore_index=True)
        # article_name_translated_df1 = article_name_translated_df1.append(
        #     {"article_name": translate(row["article_name"])}, ignore_index=True)
        print("row", row)

    # text_translated_all = pd.concat([id_df, article_name_translated_df1, text_translated_df1, article_link], axis=1)
    # filename = text_translated_all.to_csv(r'C:/Users/Jacklord/PycharmProjects/Crypto_nlp/Crypto_nlp/Scraper/Scraper/spiders/article_translated.csv', index = False, header=True)
    # load(filename, 'article_translated')
    # print("Original text translated and saved as article_translated.csv")
    ##########################