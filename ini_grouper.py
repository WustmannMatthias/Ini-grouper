
import argparse
import os
import re
import json

parser = argparse.ArgumentParser(description="Regroup phing variables by values")
parser.add_argument("directory", help="directory containing phing ini files", nargs='?', default=os.getcwd())
parser.add_argument("-o", "--output_file", help="file to store results", metavar="output_file")


def main():
	args = parser.parse_args()
	directory = args.directory

	regex = "(?P<key>[^=]+)=(?P<value>[^=]+)"

	hashmap = dict()
	files = os.listdir(directory)

	for file in files:
		fullpath = directory + '/' + file
		with open(fullpath, 'r') as fh:
			lines = fh.read().split('\n')

		for line in lines:
			result = re.match(regex, line)
			if result:
				key 	= result.group('key')
				value 	= result.group('value')

				if value in hashmap.keys():
					if key in hashmap[value].keys():
						hashmap[value][key] += 1
					else:
						hashmap[value][key] = 1
				else:
					hashmap[value] = {key: 1}

	#print(json.dumps(hashmap, indent=4))

	text_output = str(len(hashmap.keys())) + " different values analysed : \n\n"

	for value, proposals in hashmap.items():
		sorted_proposals = sorted(proposals.items(), key=lambda kv: kv[1], reverse=True)
		
		text_output += str(value) + "\n"
		text_output += "Prefered variable name : \t" + str(sorted_proposals[0][0]) + " (" + str(sorted_proposals[0][1]) + " votes) "

		if len(sorted_proposals) > 1:
			text_output += "\n"
			text_output += "Other proposals : \t\t"
			for i in range(1, len(sorted_proposals)):
				text_output += str(sorted_proposals[i][0]) + " (" + str(sorted_proposals[i][1]) + " votes) \n\t\t\t\t"
		text_output += "\n\n"

	text_output += "\n"

	if args.output_file:
		with open(args.output_file, 'w') as fh:
			fh.write(text_output)
	else:
		print(text_output)


if __name__ == '__main__':
	main()