#!/usr/bin/env python3.6

import re
import operator

classifier = []

def create_dictionary():
	"""Creating dictionary with group names as a keys and lists of keywords as a values"""
	dictionary = {
		"asyncwait" : ["async", "await", "wait", "delay", "flaky", "flakiness"],
		"concurreny" : ["concurrency", "flakiness", "flaky", "parallel", "execution"],
		"testorder" : ["test", "order", "dependency", "flaky", "flakiness"],
		"no decision" : []
	}
	return dictionary


def results_container(dictionary):
	"""List of results for every key"""
	result = {}
	for key in dictionary:
		result.update({key: 0})
	return result


def find_matching_word_group(word, dictionary, results):
	for key in dictionary:
		if word.lower() in dictionary[key]:
			results[key] = results[key] + 1


def find_matching_group(message, dictionary, results):
	words = re.split("[, \-!?:]+", message)

	for word in words:
		find_matching_word_group(word, dictionary, results)

	highest = max(results.items(), key=operator.itemgetter(1))

	classifier.append(highest)

	for key in results:
		results[key] = 0


def classify_text(messages, dictionary, results):
	for message in messages:
		find_matching_group(message, dictionary, results)


def print_message_classifier(messages, classifier):
	count = 0
	while count < len(messages):
		print(messages[count], classifier[count], "\n")
		count += 1

def main():
	dictionary = create_dictionary()

	results = results_container(dictionary)

	messages = [
		"Cucumber salad avocado has green color, apple and tomato are red. However, 1 is not equal to ..2 ?!",
		"TOMATO IS RED, APPLE IS RED, LEMON IS YELLOW",
		"AVOCADO, cucumber, SaLaD, tomato, apple,"
	]

	classify_text(messages, dictionary, results)

	print_message_classifier(messages, classifier)


if __name__ == '__main__':
	main()
