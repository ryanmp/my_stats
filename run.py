import os
from subprocess import *

path_to_repos = '/Users/ryanphillips/Github/'
path_to_linguist = '/Users/ryanphillips/Github/linguist/'

repos = [f for f in os.listdir('..')]

for f in repos:
	if not os.path.isdir(path_to_repos + f): repos.remove(f)
	if f in ['linguist','music_gen']: repos.remove(f)

output = []
d = {}
for i in repos:
	print i

	# get number of lines
	num_lines = -1
	pipe = Popen(['git', 'ls-files'], cwd=path_to_repos+i, stdout=PIPE)

	# let's exclude a whole bunch of file-types....
	excluding = Popen(['grep', '-vE', '(.txt$|.jpeg$|.jpg$|.out$|.o$|.in$|.mp3$|.pdf$|.aux$|.ps$|.p$|.pyc$|.log$|.png$|.dvi$)'], cwd=path_to_repos+i, stdin=pipe.stdout, stdout=PIPE)

	try:
		temp = Popen(['xargs','wc','-l'], cwd=path_to_repos+i, stdin=excluding.stdout, stdout=PIPE).communicate()[0]
		print "final set", temp
		temp = temp.split('\n')
		temp = temp[-2].split(' ')
		num_lines = int(temp[-2])
	except: #xargs is giving an error on one of the repos... ignoring for now
		pass

	print 'num_lines:', num_lines

	# get language breakdown
	rel = '../' + i 
	tmp1 = Popen(["bundle", "exec", "linguist", rel], cwd=path_to_linguist, stdout=PIPE).communicate()[0]
	tmp1 = tmp1.split('\n')
	tmp3 = []
	for i in tmp1:
		if len(i) > 0:
			tmp2 = i.split(' ')
			tmp2[0] = float(tmp2[0][0:-1])*.01 #remove percentage symbol, convert into float percentage
			tmp3.append(tmp2)

	# add both metrics to a list
	#output.append((tmp3, num_lines, i)) 

	#just kidding... let's use a dict and do the calcs on the fly
	if (num_lines > 0):
		for i in tmp3:
			print i
			if len(i[1]) == 0:
				key = i[2]
			else: key = i[1]
			if key in d:
				d[key] += int(i[0]*num_lines)
			else:
				d[key] = int(i[0]*num_lines)

#print output
print d





