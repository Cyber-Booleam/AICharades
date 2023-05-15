#install PyQt6

import os
import random
import openai
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QPushButton
)

wordlist=[]

class Window(QWidget):
    global_word = ""
    def __init__(self):
        super().__init__()
        openai.api_key = "YOUR_API_KEY"
        self.modelGPT = "gpt-3.5-turbo"
        self.buildUI()

    def getRandomWord(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "nouns.txt"), "r") as file:
            for line in file:
                wordlist.append(line.rstrip())
        return random.choice(wordlist)
    
    def welcome(self):
        global global_word
        global_word = self.getRandomWord()
        self.chat_area.insertPlainText("Welcome to AICharades. Provide a clue for the word '" + global_word + "' and ChatGPT will attempt to find it\n\n")

    def buildUI(self):
        self.chat_area = QTextEdit()
        self.welcome()
        self.chat_area.setReadOnly(True)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your text here. Enter 'exit' to exit")
                                      
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.submit_text)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_area)
        layout.addWidget(self.user_input)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.setWindowTitle("AICharades")
        self.setFixedSize(700,500)

    def askChatGPT(self, clue):
        chatresponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant that plays charades. Generate 50 words that match the description from the user input. The words generated are one word."},
                {"role": "user", "content": clue}
            ],temperature=0
        )
        # print(clue)
        # print(chatresponse)
        return self.parseResponse(chatresponse)

    def submit_text(self):
            user_input_text = self.user_input.text()

            if (user_input_text == "exit"):
                sys.exit(app.exec())
            else:
                self.chat_area.insertPlainText(f"User: {user_input_text}\n")
                self.user_input.clear()
                result = self.askChatGPT(user_input_text)
                num = self.resultScoring(global_word,result)

                if(num<51):
                    # print(f"{global_word} was the #{num} guess")
                    self.chat_area.insertPlainText(f"{global_word} was the #{num} guess\n")
                else:
                    # print(f"{global_word} was not found in the first 50 guesses")
                    self.chat_area.insertPlainText(f"{global_word} was not found in the first 50 guesses\n")
                with open("results.txt", 'a') as file:
                    file.write(f"\n{global_word},{user_input_text},{num}")

                self.welcome()

    def parseResponse(self, chatresponse):
        parse = chatresponse['choices'][0]['message']['content'].split('\n')
        # print(len(parse))
        if len(parse) >10:
            for i in range(len(parse)):
                # print(parse[i])
                # self.chat_area.insertPlainText(f"\n{parse[i]}\n")
                parse[i] = parse[i].split(".")[1].strip()
            return parse
        else:
            return []
        # self.askChatGPT(user_input_text)

    def resultScoring(self, clue, result):
        for i,word in enumerate(result):
            # print(i,word)
            if word.lower()==clue.lower():
                # print(word,clue)
                return i+1
        return 51


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
