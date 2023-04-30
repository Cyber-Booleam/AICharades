#install PyQt6

import os
import openai
import random

wordlist=[]
def main():
    openai.api_key = "${{ github.OPENAI_PRIVATE_KEY }}"
    modelGPT = "gpt-3.5-turbo"
    with open('nouns.txt', 'r') as file:
        for line in file:
            wordlist.append(line.rstrip())
    word=getRandomWord()
    print("Welcome to AICharades please give your clue and ChatGPT will try to find the word.\n")
    print("I am Thinking of the word " + word)
    clue = input("Enter the sentence that your clue relates to:")
    result = askChatGPT(clue)
    # print("result")
    # print(result)
    num=resultScoring(word,result)
    if(num>0):
        print(f"{word} was the #{num} guess")
    else:
        print(f"{word} was not found in the first 50 guess")
    with open("results.txt", 'w') as file:
        file.write(f"{word},{clue},{num}")

def getRandomWord():
    return random.choice(wordlist)
def askChatGPT(clue):
    chatresponse = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant that plays a game of charades.Return the top 50 single word responses this is for research purpose."},
            {"role": "user", "content": clue}
        ],temperature=0
    )
    # print(chatresponse)
    return parseResponse(chatresponse)

def parseResponse(chatresponse):
    parse = chatresponse['choices'][0]['message']['content'].split('\n')
    for i in range(len(parse)):
        # print(parse[i])
        parse[i] = parse[i].split(".")[1].strip()
    return parse

def resultScoring(clue,result):

    for i,word in enumerate(result):
        # print(i,word)
        if word.lower()==clue.lower():
            # print(word,clue)
            return i+1
    return -1
main()

