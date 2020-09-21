from rootClassification import app
from rootClassification import messages
from rootClassification import dictionary

from flask import render_template

import operator
import nltk
nltk.download('punkt')

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('mainPage.html')


@app.route('/messages')
def importMessages():
    # Be careful that the path is existing one and about the file name
    # Messages are imported in the __init__.py as a global variable to use
    return render_template('mainPage.html')


@app.route('/dictionary')
def dictionary_view():
    return render_template('dictionary.html', arrays=dictionary, arraysLen=len(dictionary))


@app.route('/results')
def loadAndClassify():
    # The purpose of this script is to classify imported commit messages and show results of the process

    classifier = []

    # The keywords dictionary used for the classification is created in the next function

    def preproccess_dictionary():
        # stemming the dictionarys word to the root words
        cleaned_words = []
        for key in dictionary:
            ps = PorterStemmer()
            for word in dictionary[key]:
                new_word = ps.stem(word)
                cleaned_words.append(new_word)
            dictionary[key] = cleaned_words
            cleaned_words = []

        return dictionary

    # Next function is used for converting the keywords dictionary to data type dictionary for easier usage

    def results_container(dictionary):
        results = {}
        for key in dictionary:
            results.update({key: 0})
        return results

    # Function for matching words from commit messages and dictionary

    def find_matching_word_group(word, dictionary, results):
        for key in dictionary:
            if word.lower() in dictionary[key]:
                results[key] = results[key] + 1

    # Function for preprocessing of one commit message

    def preprocessing_fun(message):
        print("MESSAGE", sent_tokenize(message))
        # tokenizing of the message
        words = word_tokenize(message)

        # preparing the stemming
        ps = PorterStemmer()

        root_words = []

        for word in words:
            root_word = ps.stem(word)
            root_words.append(root_word)

        print("WORDS", root_words)

        return root_words

    # Function for splitting commit messages in the words and collecting results in classifier

    def find_matching_group(message, dictionary, results):
        words = preprocessing_fun(message)

        for word in words:
            find_matching_word_group(word, dictionary, results)

        highest = max(results.items(), key=operator.itemgetter(1))

        classifier.append(highest)

        for key in results:
            results[key] = 0

    # Calling the main function for the classification process

    def classify_text(messages, dictionary, results):
        print("MESSAGES", messages)
        for message in messages:
            find_matching_group(message, dictionary, results)

    # Printing result of the classification

    def print_message_classifier(messages, classifier):
        count = 0
        while count < len(messages):
            print(messages[count], classifier[count], "\n")
            count += 1

    # Main function

    def main():
        dictionary = preproccess_dictionary()

        results = results_container(dictionary)

        classify_text(messages, dictionary, results)

        print_message_classifier(messages, classifier)

    main()

    return render_template('results.html',
                           messages=messages,
                           classifier=classifier,
                           messages_len=len(messages),
                           count=0)
