from rootClassification import app
from flask import render_template
import re
import operator

@app.route('/')
@app.route('/home')
def homepage():
   return render_template('mainPage.html')

@app.route('/messages')
def importMessages():
   # Be careful that the path is existing one and about the file name

   # Messages should be formated as a file of Strings, where one String can contain more that one sentence.
   # One String is one commit message.
   # with open('messages.txt', 'r') as f:
   with open('/home/nejrabahtic/flask_app/rootClassification/static/messages.txt', 'r') as f:
      commits = f.readlines()
   print(commits)
   return render_template('mainPage.html')

@app.route('/dictionary')
def dictionary():
   def create_dictionary():
      dictionary = {
         "asyncwait" : ["async", "await", "wait", "delay", "flaky", "flakiness", "sleep", "threads", "synchronization"],
         "concurrency" : ["concurrency", "flakiness", "flaky", "parallel", "execution", "waiting", "mapping", "block"],
         "testorder" : ["test", "order", "dependency", "flaky", "flakiness", "dependency", "other"]
      }
      return dictionary
   return render_template('dictionary.html', arrays=create_dictionary(), arraysLen=len(create_dictionary()))

@app.route('/results')
def loadAndClassify():
   # The purpose of this script is to classify imported commit messages and show results of the process

   classifier = []

   # The keywords dictionary used for the classification is created in the next function

   def create_dictionary():
      dictionary = {
         "asyncwait" : ["async", "await", "wait", "delay", "flaky", "flakiness", "sleep", "threads", "synchronization"],
		   "concurrency" : ["concurrency", "flakiness", "flaky", "parallel", "execution", "waiting", "mapping", "block"],
		   "testorder" : ["test", "order", "flaky", "flakiness", "dependency", "other"]
      }
      return dictionary

   # Next function is used for converting the keywords dictionary to data type dictionary for easier usage

   def results_container(dictionary):
      results = {}
      for key in dictionary:
         results.update({key: 0})
      return results

   # Function for matching words from commit messages and dictionary

   def find_matching_word_group(word, dictionary, results):
      #print("WORD BEFORE", word)
      for key in dictionary:
         if word.lower() in dictionary[key]:
            results[key] = results[key] + 1

   # Function for cleaning the words from different characters

   def clean_word(word):
      cleaned_word = word.replace(r"'", '') and word.replace(r'"', '')
      return cleaned_word

   # Function for splitting commit messages in the words and collecting results in classifier

   def find_matching_group(message, dictionary, results):
      words = re.split(r"[, \-!?:]+", message)

      for word in words:
         cleaned_word = clean_word(word)
         print("WORD BEFORE", cleaned_word)
         find_matching_word_group(cleaned_word, dictionary, results)

      highest = max(results.items(), key=operator.itemgetter(1))

      classifier.append(highest)

      for key in results:
         results[key] = 0

   # Calling the main function for the classification process

   def classify_text(messages, dictionary, results):
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
      dictionary = create_dictionary()

      results = results_container(dictionary)

      with open('/home/nejrabahtic/flask_app/rootClassification/static/messages.txt', 'r') as f:
            messages = f.readlines()

      classify_text(messages, dictionary, results)

      print_message_classifier(messages, classifier)

   main()

   return render_template('results.html', arrays=create_dictionary(), arraysLen=len(create_dictionary()))