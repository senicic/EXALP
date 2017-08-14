# -*- coding: utf-8 -*-
from __future__ import print_function

#=====================================================
# author:	Danica Senicic
# date:		9/8/2017 --- ver submitted for thesis
# email:	danica.senicic@gmail.com
#
# usage: python exalp.py 1_sr.pdf 1_en.pdf
#	 python exalp.py 1_sr.txt 1_en.pdf
#
# argument order depends on the dictionary hunalign
# uses : if dic is en-sr.dic then arguments should
# be in sr-en order!
#
# put language markers in the name of your files:
# en - English
# sr - Serbian
# fr - French
# de - German
# ...
#=====================================================

#import modules

import codecs      # for resolving encoding issues (utf-8)
import re          # regular expressions
import textract    # extract txt from pdf
import sys
import os
import time


reload(sys)
sys.setdefaultencoding('utf-8')

start_time = time.time()

# Set dictionary
hun_dictionary = '../../data/en-sr.dic'	#you can change your dictionaries here, make sure they are in the right path; if you don't want the dictionary, use null.dic

# Do we need realign?
hun_realign_flag = True			#you can use hunalign's realign (True) or only dictionary (False)

file_to_process1 = sys.argv[1]	# file 1 to be processed, write as path
file_to_process2 = sys.argv[2]	# file 2 to be processed, write as path

# make folders

folder = os.path.basename(file_to_process1)[:-7]	#ex: Mng_47-48
folder_1 = os.path.basename(file_to_process1)[:-4]
folder_2 = os.path.basename(file_to_process2)[:-4]

os.mkdir(folder)
os.mkdir(folder + '/' + folder_1)
os.mkdir(folder + '/' + folder_2)

def css(filename):					#this will make a css file in your folder to give colors to your html output
	with open (filename, 'w') as f_css:
		f_css.write('table.lrtext { width: 100% } \n th.lr2th { width: 50% } \n hr.lrhr { width: 100% } \n tr.lriffy { background-color: #EECCCC; } \n tr.lriffyaltline { background-color: #EEC8FF; } \n tr.lraltline { background-color: #CCE8FF; }')

def extract(f):						#I will extract raw text from your unstructured data
	file_name	= os.path.basename(f)
	file_name_noext = file_name[:-4]
	language	= file_name[-6:-4] # en or sr?	
	extension	= f[-4:]

	
	if extension == '.pdf':				#if it's a pdf I will use textract, otherwise I'll skip this
		txt = textract.process(f, method = 'pdfminer')
	elif extension == '.txt':
		txt = f
	else:
		print ('Sorry, EXALP can only process .pdf and .txt at this time.')	#but we can easily add more options in the future in the conditions above! like epub, mobi...
	
	os.chdir(folder + '/' + file_name_noext)	#I jump in my language specific folder like 1_en or 1_sr	

	with open ('pr1.txt', 'w') as f_w:
		f_w.write(txt)
	f_w.close()
	
	with open ('pdf2text.txt', 'w') as f_w:
		f_w.write(txt)
	f_w.close()

	# hyphenation

	with open ('pdf2text.txt', 'r') as f_r:
		filedata = f_r.read()
		filedata = filedata.replace('-\n','')
	f_r.close()

	with open ('tmp1.txt', 'w') as f_w:
		f_w.write(filedata)
	f_w.close()

	# delete page numbers

	with open ('tmp1.txt', 'r') as f_r:
		with open ('tmp2.txt', 'w') as f_w:
			for line in f_r:
				line = line.strip()	#clear white space
				try:
					int(line)	#is this a number?
				except ValueError:
					f_w.write(line + '\n')
		f_w.close()
	f_r.close()

	# delete broken and empty lines

	with open ('tmp2.txt', 'r') as f_r:
		filedata = f_r.read()
        	filedate = filedata.replace('\n\n', '<p>')
        	filedata = filedata.replace('\n', ' ')
        	filedata = filedata.replace('<p>', '\n\n')
        	filedata = filedata.replace('  ', ' ')
        	filedata = filedata.replace('•', '')

	# diacritical letters

		filedata = filedata.replace('~','č')
        	filedata = filedata.replace('}','ć')
        	filedata = filedata.replace('`','ž')
        	filedata = filedata.replace('{','š')
        	filedata = filedata.replace('|','đ')
        	filedata = filedata.replace('Ê','Š')
        	filedata = filedata.replace('^','Č')
		filedata = filedata.replace('–','"')
		filedata = filedata.replace('“','"')		#did you know different languages use different quotation marks? this helps me regulate them
		filedata = filedata.replace('”','"')
		filedata = filedata.replace('‘','"')
		filedata = filedata.replace('’','"')
		filedata = filedata.replace('„','"')
		filedata = filedata.replace('"','')
		filedata = filedata.replace('\t',' ')
        	filedata = re.sub(r'(?<=[A-Z])\;?\n','.', filedata) # replace occurrences of ; into . when followed by an uppercase --- so I can treat ; separated strings as sentences
        	filedata = filedata.replace('  ',' ')

	
	final = file_name_noext + '_extracted.txt'	#this is my file which contains only raw text
	with open (final, 'w') as f_w:
		f_w.write(filedata)
	f_w.close()
	f_r.close()

	# clean up --- I don't need to keep these, but if I need to control files to look for errors, I'll comment these

	os.system('rm ./pr1.txt')
	os.system('rm ./tmp1.txt')
	os.system('rm ./tmp2.txt')
	os.system('rm ./pdf2text.txt')

	os.chdir('../..') # going back to my home folder

	print ('Created raw text file for ' + file_name_noext + '.')

	return final

	
def unitex(f):	# I call Unitex with this --- Unitex delimits my sentences --- if your graphs don't work, make sure you compiled them properly (check Unitex's manual)
		
	language = f[-16:-14]			# en or sr or fr? this is why I need language markers in my arguments!
	name     = os.path.basename(f)[:-14]	# name witout extension like Mng_47-48_en
	
	os.chdir('Unitex-GramLab-3.1/App')	

	if language == 'sr':
        	os.system('./UnitexToolLogger Fst2Txt ../Serbian-Latin/Graphs/Preprocessing/Sentence/Sentence.fst2 -t ../../' + folder + '/' + name + '/' + name + '_extracted.txt -o ../../' + folder + '/'+ name + '/' + name + '_unitex.txt')
	
	elif language == 'en':
		os.system('./UnitexToolLogger Fst2Txt ../English/Graphs/Preprocessing/Sentence/Sentence.fst2 -t ../../' + folder + '/' + name + '/' + name + '_extracted.txt -o ../../' + folder + '/'+ name + '/' + name + '_unitex.txt')
       
	elif language == 'de':		#untested --- need data
		os.system('./UnitexToolLogger Fst2Txt ../German/Graphs/Preprocessing/Sentence/Sentence.fst2 -t ../../' + folder + '/' + name + '/' + name + '_extracted.txt -o ../../' + folder + '/'+ name + '/' + name + '_unitex.txt') 

	elif language == 'fr':		#untested --- need data
		os.system('./UnitexToolLogger Fst2Txt ../French/Graphs/Preprocessing/Sentence/Sentence.fst2 -t ../../' + folder + '/' + name + '/' + name + '_extracted.txt -o ../../' + folder + '/'+ name + '/' + name + '_unitex.txt')

	else:
        	print('Please specify the language in your file like this: abc_en.txt or abc_sr.pdf')
        	sys.exit()
	
	unitex_file = name + '_unitex.txt'
	print ('Created Unitex processed file for ' + name + '.')
	os.chdir('../..')	# going back to my home folder

	return unitex_file

def xml(f):	# make xml like the ones we made for ACIDE

	path = folder + '/' + f[:-11]
	os.chdir(path)

	head = f[:-11]

	# regulating double volumes (replace '-' with '/')

	original_head = head
	head	      = head.replace('-','/')

	output	      = original_head + '.xml'

	# open files

	txt_input  = f
	txt_output = output

	# xml content

	xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE body SYSTEM \"body.dtd\">\n<body>\n<div>\n<head>" + head + "</head>\n"

	with codecs.open(txt_input, 'r', encoding = 'utf-16') as f_r:
		filedata = f_r.read()
		filedata = re.sub(r'{S}','</seg>\n<seg>',filedata)
    		filedata = re.sub('\n</seg>\n<seg>','</seg></p>\n\n<p><seg>', filedata)
    		filedata = re.sub('</seg>\n\n','</seg></p>\n\n', filedata)
    		filedata = re.sub('\n\r</seg></p>','</seg></p>', filedata)
    		filedata = filedata.replace('\n\r','')
	f_r.close()

	with codecs.open(txt_output, 'w', encoding = 'utf-8') as f_w:
		f_w.write(xml)
		f_w.write('<p><seg>' + filedata)
		f_w.write('</seg></p>')
		f_w.write('\n</div></body>')
	f_w.close()

	print ('Created xml file for ' + head + '.')

	os.chdir('../..')

	return txt_output

def snt(f):	# I only need sentences for hunalign and gargantua; it's one sentence per line!

	path = folder + '/' + f[:-4]
	os.chdir(path)

	output_snt = f[:-4] + '_snt.txt'

	with open (f, 'r') as f_r:
		filedata = f_r.read()
		start = '<seg>'
		end   = '</seg>'

		extracted = re.findall('%s(.*)%s' % (start, end), filedata) #findall returns a list
	f_r.close()
	
	regex = '^\d+'		# if a line contains only a number, I don't need it; it's probably page number or noise

	with open (output_snt, 'w') as file_w:
    		for i in extracted :
       			if re.match(regex,i) is None:
           			file_w.write(i + "\n")
       			else :
           		#If more than one word in line, skip first and write to file the rest
           			if(len(i.split()) > 1):
               				file_w.write((i.split(None, 1)[1] + '\n'))
	file_w.close()

	print ('Extracted sentences only file for ' + f[:-4] + '.')
	
	os.chdir('../..')

	return output_snt


def hunalign(f1, f2, user_dictionary, realign_flag):

	folder_name  = f1[:-11]
	folder1_name = f1[:-8]
	folder2_name = f2[:-8] 

	aligned = folder1_name + '_' + folder2_name + 'hun'
	
	os.chdir('hunalign-1.1/src/hunalign/')
	if realign_flag:
		os.system('./hunalign -text -realign -autodict=../../../' + folder_name + '/' + folder_name + '_dictionary.dic ' + user_dictionary + ' ../../../' + folder_name + '/' + folder1_name + '/' + f1 + ' ../../../' + folder_name + '/' + folder2_name + '/' + f2 + ' > ../../../' + folder_name + '/' + aligned + '.txt')
	else:
		os.system('./hunalign -text ' + user_dictionary + ' ../../../' + folder_name + '/' + folder1_name + '/' + f1 + ' ../../../' + folder_name + '/' + folder2_name + '/' + f2 + ' > ../../../' + folder_name + '/' + aligned + '.txt')
	os.chdir('../../..')
        css(folder_name + '/lrstyle.css')
	os.system('python hun2html.py ./' + folder_name + '/' + aligned + '.txt > ./' + folder_name + '/' + aligned + '_hun.html')


def gargantua(f1, f2):

	folder_name  = f1[:-11]
	folder1_name = f1[:-8]
	folder2_name = f2[:-8] 
	aligned = folder1_name + '_' + folder2_name + '_gargantua'

	os.system('cp ./'+ folder_name +'/' + folder1_name + '/' + f1 + ' ./Gargantua1.0c/corpus_to_align/source_language_corpus_prepared/source_target.txt')
	os.system('cp ./'+ folder_name +'/' + folder1_name + '/' + f1 + ' ./Gargantua1.0c/corpus_to_align/source_language_corpus_tokenized/source_target.txt')
	os.system('cp ./'+ folder_name +'/' + folder1_name + '/' + f1 + ' ./Gargantua1.0c/corpus_to_align/source_language_corpus_untokenized/source_target.txt')
	os.system('cp ./'+ folder_name +'/' + folder2_name + '/' + f2 + ' ./Gargantua1.0c/corpus_to_align/target_language_corpus_prepared/source_target.txt')
	os.system('cp ./'+ folder_name +'/' + folder2_name + '/' + f2 + ' ./Gargantua1.0c/corpus_to_align/target_language_corpus_tokenized/source_target.txt')
	os.system('cp ./'+ folder_name +'/' + folder2_name + '/' + f2 + ' ./Gargantua1.0c/corpus_to_align/target_language_corpus_untokenized/source_target.txt')

	os.chdir('./Gargantua1.0c/src')
	os.system('./sentence-aligner')

	os.chdir('../../' + folder_name)

	alignment_result = '../Gargantua1.0c/src/output_data_aligned/info.txt'

	with open(alignment_result, 'r') as f_r_column1:
		column_1 = [line.split('\t')[1] for line in f_r_column1]
	f_r_column1.close()

	with open(alignment_result, 'r') as f_r_column2:
		column_2 = [line.split('\t')[2] for line in f_r_column2]
	f_r_column2.close()

	with open('tmp1.txt', 'w') as f_w_tmp1:
		for item in column_1:
			f_w_tmp1.write('%s\n' % item)
	f_w_tmp1.close()

	with open('tmp2.txt', 'w') as f_w_tmp2:
		for item in column_2:
			f_w_tmp2.write('%s' % item)
	f_w_tmp2.close()

	os.chdir('./' + folder1_name)

	with open(f1, 'r') as f_r:
		list_source = f_r.readlines()
	f_r.close()

	os.chdir('../' + folder2_name)

	with open(f2, 'r') as f_r:
		list_target = f_r.readlines()
	f_r.close()

	os.chdir('../')							# Gargantua gives me only numbers... I want to see sentences!

	output = folder1_name + '_' + folder2_name + '_gargantua.txt'

	with open(output, 'w') as f_output:
		with open('tmp1.txt') as f1, open('tmp2.txt') as f2:
                        linecnt = 0
			for xrow, yrow in zip(f1, f2):
				x = xrow.split()
				y = yrow.split()

				x_cnt = len(x)
				y_cnt = len(y)
				
				if(x_cnt > 1 and y_cnt > 1):

					print ('Incorrect number of elements for mapping.')
					os.system(exit)

				for item in x:
					# Gargantua output has 1-based indices
					f_output.write('%s ' % list_source[int(item) - 1].rstrip())
				f_output.write('\t')

				for item in y:
					# Gargantua output has 1-based indices
					f_output.write('%s ' % list_target[int(item) - 1].rstrip())

				f_output.write('\t 0.5')
				f_output.write('\n')
          			linecnt += 1

	os.chdir('../')
        css(folder_name + '/lrstyle.css')
	os.system('python hun2html.py ./' + folder_name + '/' + aligned + '.txt > ./' + folder_name + '/' + aligned + '_gargantua.html')

	f1.close()
	f2.close()

	f_output.close()



#execute

f1_extr   = extract(file_to_process1)
f2_extr   = extract(file_to_process2)

f1_unitex = unitex(f1_extr)
f2_unitex = unitex(f2_extr)

f1_xml    = xml(f1_unitex)
f2_xml	  = xml(f2_unitex) 

f1_snt	  = snt(f1_xml)
f2_snt    = snt(f2_xml)

print("Extraction: --- %s seconds ---" % (time.time() - start_time))

# gargantua takes a long time, if you need fast alignment comment gargantua and use hunalign

# List all alignment methods to try!
print ('=====> HUNALIGN <=====\n')
hunalign (f1_snt, f2_snt, hun_dictionary, hun_realign_flag)
print("hunalign: --- %s seconds ---" % (time.time() - start_time))
print ('\n\n\n')
print ('=====> GARGANTUA <=====\n')
gargantua (f1_snt, f2_snt)
print("total: --- %s seconds ---" % (time.time() - start_time))

