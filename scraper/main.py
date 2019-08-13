from bs4 import BeautifulSoup
import requests

# ! For result file name, I just don't want duplication
import uuid

FAQ_URLS = [
    "https://drexel.edu/undergrad/apply/int-instructions/faq/",
    "https://drexel.edu/undergrad/apply/freshmen-instructions/faq/"
]

# * This is a counter for number of resulted yaml file(s).
# ! Also prevent duplication as will be added to file name
count = 0

if __name__ == "__main__":
    for FAQ_URL in FAQ_URLS:
        response = requests.get(FAQ_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        # file_name = (soup.title.string.rstrip().lstrip())

        # ! OK so after some investigation on how ChatterBot works, I realize that 
        # ! each category (or entity) should be in seperate files
        # ! for better training and managing

        # * There's only one article tag in page so findAll is unecessary
        __article = soup.find('article') 

        # * Get all tags that is inside <article> which contains all Q&A
        __article_children = __article.children

        # ! Begin going down the tree:
        # * On each <h2> which is category, create a new file
        # * If see h3 -> create new question
        # * If see others (p and so on) -> add as answer
        # ! Preserving <a> tag in answer has no harm in training process

        tempAns = ""
        questionStarted = False # ! To remove any warning before Q&A
        file = None
        for art in __article_children:
            if art.name == "h2": # * Category
                if file != None:
                    # ! Just to make sure everything is printed out
                    if tempAns != "":
                        file.write("  - " + tempAns.replace(':', "-"))
                        tempAns = ""
                    file.close()
                    file = None
                count += 1
                file = open(art.string.rstrip().lstrip() + " - " + str(count) + ".yaml", "w+")
                file.write('categories:\n')
                file.write("- " + art.string + "\n")
                file.write('conversations:\n')
            elif art.name == "h3": # * Question
                questionStarted = True
                if tempAns != "":
                    file.write("  - " + tempAns.replace(':', "-") + "\n") # ! Seems like having : broke yaml file (dirty fix)
                    # questionStarted = False
                tempAns = ""
                file.write("- - " + art.string.replace(':', "-") + "\n")
            elif art.name == "p" and questionStarted:
                try:
                    for content in art.contents:
                        tempAns += str(content).rstrip(']').lstrip('[').rstrip('"').rstrip("'").lstrip('"').lstrip("'").rstrip().lstrip()
                except:
                    pass

        # ! On last question of last category, answer is not inserted and file is not yet closed
        if tempAns != "":
            file.write("  - " + tempAns.replace(':', "-"))
            tempAns = ""
        file.close()
        file = None