#install PyQt6

import os
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

class Window(QWidget):
    def __init__(self):
        super().__init__()
        openai.api_key = ${{ github.OPENAI_PRIVATE_KEY }} 
        self.modelGPT = "gpt-3.5-turbo"
        self.buildUI()

    def buildUI(self):
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.insertPlainText("Welcome to AICharades. Provide a clue and ChatGPT will attempt to find the corresponding word.\n\n")
        self.welcome()

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
                
    def welcome(self):
        self.chat_area.insertPlainText("\nEnter your clue in the form of a sentence.\nFor example: The word I am thinking of is a metal piece, often used in woodworking that is hit with a hammer\n")

    def submit_text(self):
        user_input_text = self.user_input.text()
        self.chat_area.insertPlainText(f"\nUser: {user_input_text}\n")
        if (user_input_text == "exit"):
            sys.exit(app.exec())
        else:
            clue = self.askChatGPT(user_input_text)
        self.user_input.clear()

    def askChatGPT(self, clue):
        chatresponse = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that plas a game of charades. Give your answers as the top 5 words you think are correct with the confidence respresented as decimal."},
                {"role": "user", "content": clue}
            ],temperature=0
        )
        self.parseResponse(chatresponse)
        return chatresponse

    def parseResponse(self, chatresponse):
        parse = chatresponse['choices'][0]['message']['content'].split('\n')
        for i in range(len(parse)):
            print(parse[i])
            self.chat_area.insertPlainText(f"\n{parse[i]}\n")
            parse[i] = parse[i][3:len(parse[i]) - 1].split(' (')
            if len(parse[i]) > 1:
                parse[i][1] = float(parse[i][1])
        return parse

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
