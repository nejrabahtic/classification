#!/usr/bin/env python3.6

import re
import operator

# The purpose of this script is to classify imported commit messages and show results of the process

classifier = []

# The keywords dictionary used for the classification is created in the next function
def create_dictionary():
	dictionary = {
		"asyncwait" : ["async", "await", "wait", "delay", "flaky", "flakiness", "sleep", "threads", "synchronization"],
		"concurreny" : ["concurrency", "flakiness", "flaky", "parallel", "execution", "waiting", "mapping", "block"],
		"testorder" : ["test", "order", "dependency", "flaky", "flakiness", "dependency", "other", "test"]
	}
	return dictionary

# Next function is used for converting the keywords dictionary to data type dictionary for easier usage
def results_container(dictionary):
	result = {}
	for key in dictionary:
		result.update({key: 0})
	return result

# Function for matching words from commit messages and dictionary
def find_matching_word_group(word, dictionary, results):
	for key in dictionary:
		if word.lower() in dictionary[key]:
			results[key] = results[key] + 1

# Function for splitting commit messages in the words and collecting results in classifier
def find_matching_group(message, dictionary, results):
	words = re.split("[, \-!?:]+", message)

	for word in words:
		find_matching_word_group(word, dictionary, results)

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

	with open('messages.txt', 'r') as f:
    		messages = f.readlines()

	classify_text(messages, dictionary, results)

	print_message_classifier(messages, classifier)


if __name__ == '__main__':
	main()
