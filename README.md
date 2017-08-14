# EXALP
EXtraction and ALignment Pipeline

EXALP takes unstructed files as an input and provides aligned sentences in .html and .txt
EXALP was built for extracting and aligning Serbian and English sentences, but is adaptable for most language pairs

# Usage
From the toplevel directory
`python abc_sr.pdf abc_en.pdf`

# Output
## Project tree
.
 * abc
 * abc_en
   * abc_en.xml
   * abc_en_extracted.txt
   * abc_en_snt.txt
   * abc_en_unitex.txt
 * abc_sr
   * abc_sr.xml
   * abc_sr_extracted.txt
   * abc_sr_snt.txt
   * abc_sr_unitex.txt
 * abc_dictionary.dic
 * abc_en_abc_sr_hun.txt
 * abc_en_abc_sr_garg.html
 * abc_en_abc_sr_garg.txt
 * lrstyle.css
 
 # Dependencies and requirements
 A.1 Unitex/GramLab <br />
 • Install Unitex/GramLab according to your OS. http://unitexgramlab.org/ <br />
 • Install python bindings for Unitex/Gramlab. https://github.com/patwat/python-unitex <br />
 • Compile grammars for languages you want to use. For example: `./Unitex-GramLab-3.1/App/UnitexToolLogger ./Unitex-GramLab-3.1/French/Graphs/Preprocessing/Sentence Grf2Fst2 grf` <br />
 • For additional modiﬁcations consult Unitex’s manual: http://www.cis.uni-muenchen.de/people/lg3/ManuelUnitex.pdf <br />
 
 A.2 hunalign <br />
 • Install hunalign https://github.com/danielvarga/hunalign <br />
 • Dictionaries can be modiﬁed in `cd ./hunalign-1.1/data` <br />
 • To run hunalign outside EXALP: <br />
 	– Show the result as text, no realignment <br /> 
	`hunalign -text dictionary.dic L1.txt L2.txt > result.txt` <br /> 
	– Use realignment <br />
	`hunalign -text -realign dictionary.dic L1.txt L2.txt > result.txt` <br />
• Dictionary argument is obligatory, if you don’t want to use it, enter null.dic <br />
• For additional options consult https://github.com/danielvarga/hunalign <br />

A.3 Gargantua <br />
• Download Gargantua from https://sourceforge.net/projects/gargantua/ <br />
• Follow the README, but skip the part with data preparation - only the aligner is needed <br />
• Prepare the ﬁlesystem accordingly (!important!) — All the ﬁles in all of the folders in the ﬁlesystem should have the same name <br />
• Compile the source code `cd src make clean make` <br />
• To run Gargantua outside EXALP, use only `./sentence-aligner` <br />

For further requirements see `requirements.txt` <br />
