#!/usr/bin/env python

def html_header(stylesheet='lrstyle.css'):
    meta = '<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">'
    style = '<link rel="stylesheet" href=%s type="text/css">' % stylesheet
    return '<html><head>%s\n%s\n</head><body>' % (meta, style)

def html_footer():
    return "</body></html>"

def paragraph_header():
    th = '<th class="lr2th"></th>'
    return '<hr class="lrhr">\n<table class="lrtext">%s%s\n' % (th, th)

def paragraph_footer():
    return "</table>"

def calculate_line_class(rating, index):
    if rating < 0:
        if index % 2:
            return "lriffyaltline"
        return "lriffy"
    if index % 2:
        return "lraltline"
    else:
        return ""

def split_hunline(hunline):
    expanded = hunline.split("\t")
    if len(expanded) != 3:
        raise ValueError, "Unexpected line format\n%s" % hunline
    try: float(line[2]) #the last thing should be a score
    except: ValueError, "Unexpected line format\n%s" % hunline
    return expanded

def hun2html_line(line, index=0):
    expanded = split_hunline(line)
    #now is it a content line or just a matching blank?
    #content:
    if expanded[0].strip() or expanded[1].strip():
        lrclass = calculate_line_class(float(expanded[2].strip()), index)
        htmlized_line = "<tr class=%s><td>%s</td>\n<td>%s</td></tr>\n" % (lrclass, expanded[0], expanded[1])
    else: #blank line -- this codepath can't be hit if called via hun2html_par
        htmlized_line = ""
    #print >> sys.stderr, index, htmlized_line
    return htmlized_line

def hun2html_par(paragraph):
    if not paragraph.strip():
        return ''
    par_text = [paragraph_header()]
    lines = paragraph.strip('\n').split('\n')
    index = 0
    for line in lines:
        par_text.append(hun2html_line(line, index))
        index += 1
    par_text.append(paragraph_footer())
    return ''.join(par_text)

def hun2html(contents, paragraph_delimiter="\t\t0.3\n"):
    text = [html_header()]
    paragraphs = contents.split(paragraph_delimiter)
    for par in paragraphs:
        text.append(hun2html_par(par))
    text.append(html_footer())
    return '\n'.join(text)

if __name__ == '__main__':
    import sys
    if not sys.argv[1:]:
        print "Use: %s infile > outfile" % sys.argv[0]
        sys.exit(1)
    contents = open(sys.argv[1]).read()
    print hun2html(contents)
