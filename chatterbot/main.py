import os.path

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Drexel ISSS Bot')

trainer = ChatterBotCorpusTrainer(chatbot)

# # * Learn basic sentence I guess
# trainer.train('chatterbot.corpus.english')

# ! Recommended to delete the db.sqlite3 file on each new train (unknown reason, might have to read more in docs)
trainer.train(
    "../scraper/Application Process - 1.yaml",
    "../scraper/Scholarships and Financial Aid - 2.yaml",
    "../scraper/Drexel Co-op - 3.yaml",
    "../scraper/Application Process - 4.yaml",
    "../scraper/Scholarships - 5.yaml",
    "../scraper/Financial Aid - 6.yaml",
    "../scraper/Student Life - 7.yaml",
    "../scraper/Drexel Co-op - 8.yaml",
)

# ! This get a great result
print("===========================================================")
response = chatbot.get_response('How can I apply for scholarship?')
print(response)

print("===========================================================")
# ! This is not (so even slight modification in the question heavily affect the system)
response = chatbot.get_response('How can I get scholarship?')
print(response)