import os
import openai

def main():
    openai.api_key = ${{ github.OPENAI_PRIVATE_KEY }}
    modelGPT = "gpt-3.5-turbo"
    print("Welcome to AICharades please give your clue and ChatGPT will try to find the word.\n")
    clue = input("Enter the sentence that your clue relates to:")
    askChatGPT(clue)


def askChatGPT(clue):
    chatresponse = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant that plas a game of charades. Give your answers as the top 5 words you think are correct with the confidence respresented as decimal."},
            {"role": "user", "content": clue}
        ],temperature=0
    )
    parseResponse(chatresponse)
    return chatresponse

def parseResponse(chatresponse):
    parse = chatresponse['choices'][0]['message']['content'].split('\n')
    for i in range(len(parse)):
        print(parse[i])
        parse[i] = parse[i][3:len(parse[i]) - 1].split(' (')
        parse[i][1] = float(parse[i][1])
    return parse

main()
