#!usr/bin/python

import platform as p, subprocess, sys, os
from datetime import datetime

def main( ):

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

	Output = ''.join(['Output file: ', output_file])
	
    	Separatrix2 = '-----------------------------\n'

	#print script_file, input_file, output_file, log_file

	

	if os.path.exists(log_file):
		append_write = 'a' # append if already exists
	else:
		append_write = 'w' # 
	
	if input_value > 1: 

		Input = ''.join(['Input file: ', input_file ])	
		info1 = Separatrix + Date + '\n' + log_file + '\n' + User + '\n' + Separatrix2 + '\n'
		info2 = Separatrix + Script + '\n' + Version + '\n' + Date + '\n' + Aim + '\n\n' + System + '\n' +  Input + '\n' + Output + '\n' + Separatrix2

		if append_write == 'w':  
			out =  info1 + info2
	
		else:
			out =  info2

		subprocess.call([ executable[language], script_file, '-i', input_file, '-o', output_file])

	else: 
		Input = ''.join(['Input file: ', input_file ])	
		info1 = Separatrix + Date + '\n' + log_file + '\n' + User + '\n' + Separatrix2 + '\n'
		info2 = Separatrix + Script + '\n' + Version + '\n' + Date + '\n' + Aim + '\n\n' + System + '\n' +  Input + '\n' + Output + '\n' + Separatrix2

		if append_write == 'w':  
			out =  info1 + info2
	
		else:
			out =  info2

		subprocess.call([ executable[language], script_file, '-i', input_file, '-o', output_file])


	f = open(log_file, append_write)
	f.write(out)
	f.close()


if __name__ == "__main__":
	input_value = (len(sys.argv) - 4)
	if input_value > 1 :
		script_file = sys.argv[1]
		input_file = ''
		
		for arg in sys.argv[2:(len(sys.argv) - 3)]: 
						
			input_file.append(arg)

		output_file = sys.argv[-2]
		log_file = sys.argv[-1]
	else:
		script_file = sys.argv[1]
		input_file = sys.argv[2]
		output_file = sys.argv[3]
		log_file = sys.argv[4]

	print( ' Everything all right' )

    	main(  )
