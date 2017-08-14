# EXALP
EXtraction and ALignment Pipeline

EXALP takes unstructed files as an input and provides aligned sentences in .html and .txt
EXALP was built for extracting and aligning Serbian and English sentences, but is adaptable for most language pairs

## USAGE
From the toplevel directory
`python abc_sr.pdf abc_en.pdf`

## OUTPUT
# Project tree
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
 
 ## Dependencies and requirements
 A.1 Unitex/GramLab 
 • Install Unitex/GramLab according to your OS. http://unitexgramlab.org/ 
 • Install python bindings for Unitex/Gramlab. https://github.com/patwat/python-unitex 
 • Compile grammars for languages you want to use. For example: `./Unitex-GramLab-3.1/App/UnitexToolLogger ./Unitex-GramLab-3.1/French/Graphs/Preprocessing/Sentence Grf2Fst2 grf` 
 • For additional modiﬁcations consult Unitex’s manual: http://www.cis.uni-muenchen.de/people/lg3/ManuelUnitex.pdf
 
 A.2 hunalign 
 • Install hunalign https://github.com/danielvarga/hunalign 
 • Dictionaries can be modiﬁed in `cd ./hunalign-1.1/data` 
 • To run hunalign outside EXALP: 
 	– Show the result as text, no realignment  
	`hunalign -text dictionary.dic L1.txt L2.txt > result.txt` 
	– Use realignment
	`hunalign -text -realign dictionary.dic L1.txt L2.txt > result.txt` 
• Dictionary argument is obligatory, if you don’t want to use it, enter null.dic 
• For additional options consult https://github.com/danielvarga/hunalign

A.3 Gargantua 
• Download Gargantua from https://sourceforge.net/projects/gargantua/ 
• Follow the README, but skip the part with data preparation - only the aligner is needed 
• Prepare the ﬁlesystem accordingly (!important!) — All the ﬁles in all of the folders in the ﬁlesystem should have the same name 
• Compile the source code `cd src make clean make` 
• To run Gargantua outside EXALP, use only `./sentence-aligner`

For further requirements see `requirements.txt`
