# EXALP
Automatic alignment of bilingual sentences: the case of English and Serbian

EXALP works with many dependencies and libraries.

Please install with the following structure:

EXALP
.
├── Unitex
├── hunalign 
├── Gargantua
├── exalp.py      
├── hun2html.py
├── abc_en.pdf
└── abc_sr.pdf

=========================================================================================

1. Unitex 				http://unitexgramlab.org/
2. python bindings for Unitex		https://github.com/patwat/python-unitex

EXALP uses UnitexToolLogger (12.44 in the manual)		http://unitexgramlab.org/releases/2.1/man/Unitex-GramLab-2.1-usermanual-en.pdf
To extract sentences Unitex needs fst2 
Compile a graph Grf2Fst2    (12.20 in the manual) - do this for every language you want to use

=========================================================================================

3. hunalign			https://github.com/danielvarga/hunalign
				
Find the dictionaries in the ./dictionary folder and copy them in respective hunalign's dictionary dir

=========================================================================================

4. Gargantua			https://sourceforge.net/projects/gargantua/

Make sure to build the structure of Gargantua as requested

=========================================================================================

5. For the rest of dependencies see requirements.txt

=========================================================================================

USAGE: python exalp.py abc_sr.pdf abc_en.pdf

Please name your files with adequate language marker. For example abc_sr.pdf and abc_en.pdf
If you use hunalign dictionary make sure that the order of arguments is INVERSE from the dictionary:
e.g. if it's an en-sr.dic, the order of arguments should be abc_sr.pdf abc_en.pdf

By default, EXALP will do the extraction and the alignment with hunalign and gargantua

==========================================================================================
