#!usr/bin/python

import platform as p, subprocess, sys, os, argparse
from datetime import datetime

args_ = None
def main( ):

	script_file = args_.script_argument
	input_file = args_.input_argument
	output_file = args_.output_argument
	log_file = args_.log_argument

	language = script_file.split('.')[1]
	executable = {'py' : 'python', 'R' : 'R', 'pl' : 'perl', 'm' : 'octave'}

	Separatrix = '*****************************\n\n'
	User = ''.join(['Personnel: ', 'Pankaj Chauhan'])
	Date = ''.join(['Date: ', str(datetime.now())])
	System = ''.join(['System: ', p.platform()])
	Script = ''.join(['Script: ', script_file ])

	if executable[language] == 'python' :
		used_version = ''.join([ 'python ', p.python_version()])
	else:
		used_version = subprocess.check_output([executable[language], '--version']).lstrip().split('\n')[0]

	Version = ''.join(['Version: ', used_version ])
	Aim = 'Aim: '

	Output = ''.join(['Output file: ', str(output_file)])

	Separatrix2 = '-----------------------------\n'

	#print script_file, input_file, output_file, log_file



	if os.path.exists(log_file):
		append_write = 'a' # append if already exists
	else:
		append_write = 'w' #
#	subprocess.check_call(pass_arg)

	Input = ''.join(['Input file: ', str(input_file) ])
	info1 = Separatrix + Date + '\n' + log_file + '\n' + User + '\n' + Separatrix2 + '\n'
	info2 = Separatrix + Script + '\n' + Version + '\n' + Date + '\n' + Aim + '\n\n' + System + '\n' +  Input + '\n' + Output + '\n' + Separatrix2

	if append_write == 'w':
		out =  info1 + info2

	else:
		out =  info2
	all_parse = []
	all_parse.append(executable[language])
	all_parse.append(script_file)
	all_parse.append('-i')

	for item in input_file:
		all_parse.append(item)

	all_parse.append('-o')
	for item in output_file:
		all_parse.append(item)

	subprocess.call(all_parse)


	f = open(log_file, append_write)
	f.write(out)
	f.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Master script to execute a program")
	parser.add_argument('-S', dest='script_argument', help="Put the script here ")
	parser.add_argument('-I', nargs='+', dest="input_argument", help="Put all input files here ")
	parser.add_argument('-O', nargs='+', dest="output_argument", help="Put all output files here ")
	parser.add_argument('-L', dest="log_argument", help="Put log file here ")
	args_ = parser.parse_args()
	print( ' Everything all right' )
	main(  )
