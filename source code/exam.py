from process import *

def main():
    # Get Paragragh
    lst = paragragh()
    print('(A) Convert XML file to readable one\n')
    save()

    print('(B) List random 20 vocabularies\n')
    voc , dict_voc = vocab(lst)
    print(voc[:20],'\n')

    print('(C) Count frequency of occurrence of vocabularies\n')
    print(dict_voc,'\n')
    
    print('(D) List 20 compound words\n')
    compound , times = find_comp(dict_voc)
    print(compound[:20],'\n')

    print('(E) Count frequency of occurrence of compound vocabularies\n')
    print(times,'\n')

if __name__ == "__main__" : main()
    