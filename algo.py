import re

##########
#### SEARCH FOR TODO and fix


# Anything following "//" is a comment until end of line
commentPat = re.compile(r'//(.*)')

# Grab anything within $...$. Make sure to use 
mathPat =  re.compile(r'\$(.*?)\$')

#All id-like words, including optional leading '\' and 
# field access sequences 
# Examples: abc,  foo.length, \xxx
wordPat = re.compile( r'[\\A-Za-z][\.a-zA-Z_]*' )

#Take a set of all the unique symbols in opsToTex's keys. 
#Like this r'[<=>.]+'   etc. 
opPat = re.compile( r'[<\-=.>!+]+' )

# A line of the form "proc myfunc(a, b)".
procPat = re.compile( r'^proc (.*)\((.*)\)' )

keywordsToTex = {
    'for'    : r'\For'        ,     'if'     : r'\If'          , 
    'end'    : r'\End'        ,     'then'   : r'\Then'        , 
    'while'  : r'\While'      ,     'do'     : r'\Do'          ,  
    'to'     : r'\To'         ,     'by'     : r'\By'          , 
    'downto' : r'\Downto'     ,     'repeat' : r'\Repeat'      , 
    'until'  : r'\Until'      ,     'elseif' : r'\Elseif'      ,
    'elsif'  : r'\Elseif'     ,     'return' : r'\Return'      , 
    'error'  : r'\Error'      ,     'nil'    : r'\const{nil}'  , 
    'true'   : r'\const{true}',     'false'  : r'\const{false}'
}

opsToTeX = {
    '<-' : r'\leftarrow' ,      '->' : r'\rightarrow',      '==' : r'\isequal' ,
    '<=' : r'\leq'       ,      '>=' : r'\geq'        ,      '>' : '>'          , 
    '<' : '<'            ,      '!=' : r'\neq'       ,      '=' : r'\eq'       , 
    '...' : r'\threedots',      '..' : r'\twodots'  ,       '-' : r'-'      ,
    '+' : r'+'
}

def processLine(line):
    processedContent = processContent(re.split(commentPat,line)[0]) 
    processedComment = ''
    if re.search(commentPat,line):
        processedComment = processComment(re.search(commentPat,line).group(1))
    return processedContent + processedComment
    # Split line into content part and comment part
    # Comments are always to the right, but are optional
    # return processContent(content) + processComment(comment)

def processContent(content):
    if(re.search(procPat, content)):
        return processProc(content)
    # Treat the entire content as if it is already in math mode
    # processProc if it matches a proc line
    # Otherwise,
    # Treat the entire content as if it is already in math mode.
    # If there are any embedded '$...$' fragments, then strip the dollar signs
    # out.
    re.sub(mathPat,lambda a:a.group(1),content)
    return '\\zi' + processOps(processWords(content))
    # Prepend '\zi' to the returned line, unless content matches a proc declaration

def processProc(lineMatch):
    s = re.search(procPat,lineMatch)
    ans = '\\proc{' + s.group(1) + "}"
    ans = ans + '('+processWords(s.group(2))+')'
    ans = '\\Procname{' + ans + "}"
    return ans

def processMath(mathPart):
    stringMathPart = mathPart
    if(type(mathPart)!=type('a')):
        stringMathPart = mathPart.group(1)
    processedMathPart = processOps(processWords(stringMathPart))
    return processedMathPart
    # call processOps(processWords) on the matching part.

def processWords(fragment):
    return re.sub(wordPat,processWord,fragment)
    # call re.sub with wordPat and processWord

def processWord(wordMatch):
    word = wordMatch.group(0)
    #TODO
    # Handle four cases. 
    #   Word starts with '\' ... return word untouched
    if word[0]=="\\":
        return word
    #   Word has embedded '.'. Convert "abc.def.ghi" to "\attribbb{abc}{def}{ghi}"
    #            The number of 'b's following attrib should equal the number of dots
    if '.' in word:
        lst = word.split('.')
        ans = '\\attri' + 'b'*(len(lst)-1)
        for x in lst:
            ans += '{' + x + '}'
        return ans
    #   Word belongs to keywords (see testalgo.py for all keywords). Replace with latex substitute
    if word in keywordsToTex.keys():
        return keywordsToTex[word]
    #   Otherwise replace with "\id{word}"
    return "\\id{" + word + "}"

def processOps(fragment):
    return re.sub(opPat, processOp, fragment)

def processOp(opMatch):
    op = opMatch.group(0)
    if op in opsToTeX.keys():
        return '$' + opsToTeX[op] + '$'
    return op
    # replace op with matching latex equivalent if any, and surround with '$'
    # That is, '==' becomes '$\isequal$', but '===' remains unchanged.

def processComment(comment):
    comment = re.sub(mathPat,processMath,comment)
    return r'\Comment '+ comment
    #Treat comment as if it is in text mode, but all embedded math expressions must be translated
    #by processMath
    # See testalgo.py for expected behaviur


def main(filename):
    with open(filename) as f:
        print(r'\begin{codebox}')
        for line in f:
            line = line.rstrip()
            print(processLine(line))
        print(r'\end{codebox}')

def usage():
    print("""
algo.py <file.algo>
Translates a pseudocode algorithm to LaTeX's clrscode3e environment. 
The format is a simplification of that environment, the objective being to 
not have to introduce math-mode or have special keywords like \For and \If 

Keywords: 
- Loops: for, to, by, downto, do, while, repeat, until
- Selection: if, then, else, elseif/elsif
- Jumps: return, error, goto
- Constants: nil, true, false

do/end blocks are required for indent/dedent, but do not appear in final output

Operators like <-, !=, ==, <= etc are replaced by the LaTeX equivalents.

Example:

proc insertion-sort(A, B)
   for j <- 2 to A.length do
      key <- A[j] // Insert $A[j]$ into the sorted sequence $A[1 .. j-1]$
      i <- j - 1
      while i > 0 and A[i] > key do
         A[i+1] <- A[i]
         i <- i - 1
      end
      A[i+1] <- key
   end
   if x == 3 then do
      {{Do something special}}
   end
end

""")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    main(sys.argv[1])
    
   
