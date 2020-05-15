import re
from collections import Counter

def save():
    contents = paragragh()
    str_list = [line+'\n' for line in contents]
    with open('./txt/A.txt','w', encoding = 'utf-8') as f:
        f.writelines(str_list)

# Add stopWords to filt common vocabularies
def __stopWord():
    stop_word = []
    with open('./txt/stopWord.txt','r', encoding="utf-8") as stop:
        for line in stop.readlines():
            stop_word.append(line.strip('\n'))
    return stop_word

# get paragragh in XML file
def paragragh():
    lst = []; 
    re_h=re.compile(r'<[?|!|/]?\w+[^>]*>')
    with open('./XML/US08438662-20130514/US08438662-20130514.XML','r', encoding="utf-8") as xml:
        for line in xml:
            s = re_h.sub('',line)
            lst.append(s)
    return [x for x in lst if x is not None]
    
def vocab(lst):
    lst_ret = []; ret_lst = []; lst_rep = []
    stop = __stopWord()

    # Replace unnecessary symbols
    for line in lst:
        rep = line.replace(',','').replace('.','').replace('“','').replace('”','').replace('\n',' ').replace('"','')
        lst_rep.append(rep)

    # split the sentences to words
    for i in range (0,len(lst_rep)):
        lst_ret.append(re.split(' ',lst_rep[i]))

    # extract element in each list
    extract = []
    for i in lst_ret:
        for j in range(0,len(i)):
            extract.append(i[j])

    # Extract only english vocabularies
    redun = [chr(item) for item in range(32,127) if item not in range(65,90) and item not in range(97,123)]
    redun_str = "|".join(redun)
    for voc in extract:
        judge = voc.strip(redun_str)
        if len(judge)>2:
            ret_lst.append(judge)
    to_low = [voc.lower() for voc in ret_lst if voc.lower() not in stop]

    # Return results
    ret1 = list(set(to_low))
    count = dict(Counter(to_low))
    ret = dict(sorted(count.items() , key = lambda item : item[1] , reverse=True))
    ret2 = __majority_top20(ret)
    return ret1 , ret2

# find compound words with combination of top20 words
def find_comp(kw):
    lst = []; lst_use = []; comp_str = ""; comp_red = ""; 
    ret1 = []; ret_dict = {}
    art = " ".join(paragragh())
    for (k,v) in enumerate(kw.items()):
        lst.append(v)
    for word in lst:
        lst_use.append(word[0])
    for i in range(0,len(lst_use)):
        for j in range(len(lst_use),0,-1):
            comp_str = lst_use[i] + ' ' + lst_use[j-1]
            comp_red = lst_use[j-1] + ' ' + lst_use[i]
            a = [m for m in re.findall(comp_str, art ,flags = re.I|re.M)]
            b = [m for m in re.findall(comp_red, art ,flags = re.I|re.M)]
            if len(a):
                ret1.append(comp_str)
                ret_dict[comp_str] = len(a)
            if len(b):
                ret1.append(comp_red)
                ret_dict[comp_red] = len(b)
    sort = dict(sorted(ret_dict.items() , key = lambda item : item[1] , reverse=True))
    ret2 = __majority_top20(sort)
    return ret1 ,ret2

def __majority_top20(kw_cnt):
    ret_dict = {}
    for i,(k,v) in enumerate(kw_cnt.items()):
        ret_dict[k] = v
        if i == 19:
            break
    return ret_dict
    
    