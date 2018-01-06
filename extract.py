import os, shutil, re, sys
from bs4 import BeautifulSoup
from collections import OrderedDict

VERBOSE = False

def verbose(*params, sep=' ', end='\n', file=sys.stdout, flush=False):
    if VERBOSE:
        print(*params,  sep=sep, end=end, file=file, flush=flush)
        

def file_to_dict(filename):
    """
        takes filename format dddd+.html (d=digit) and returns a dict with keys ['id',...]
    """

    soup = BeautifulSoup(open(filename), 'html.parser')
    entries = OrderedDict({})
    entries['id']        = filename.split('.')[0]

    if soup.find(string= "No data found or page off-line"):
        for k in ['date','searching','offering','name','adress','tel','email']:
            entries[k]=''
    else:
        try:
            entries['date']      = soup.find('i').text[-len('yyyy-mm-dd'):].replace('/','-') #only <i> tag has last 10 chars as 'yyyy/mm/dd'
        except:
            print("Unexpected error while processing "+filename+":", sys.exc_info()[0])
            raise

        entries['searching'] = soup.find('b', string="Searching language:").next.next.next
        entries['offering']  = soup.find('b', string="Offering language:").next.next.next
    
        entries['name']      = soup.find(string="Contact person:").next.next.text
        
        maybe_addr = soup.find(string="Contact person:").next.next.next.next.next
        entries['adress'] = '' if maybe_addr.startswith('Tel: ') or maybe_addr.startswith('E-Mail: ') else maybe_addr
    
        maybe_tel=soup.find(string = lambda x: x.startswith('Tel:'))
        entries['tel']       = '' if maybe_tel == None else maybe_tel[len('Tel: '):]

        email_tag = soup.find(string = 'E-Mail: ')
        entries['email']     = '' if email_tag == None else email_tag.next['href'].split(':')[1]
    return entries

dict_to_row= lambda dic: ';'.join(dic.values())+'\n'

file_to_row=lambda f: dict_to_row(file_to_dict(f))

def main():
    criterion = lambda x:  os.path.isfile(x) and re.match('\d{4,}\.html$', x)#match 4 or more digits + '.html'
    files = filter(criterion, os.listdir())
    
    sorted_files = sorted(files, key=lambda x : x[:-len('.html')])

    table = open('data.table','a')
    
    for f in sorted_files:
        verbose('reading file '+f)
        row = file_to_row(f)
        table.write(row)

        shutil.move(os.getcwd()+'/'+f,
                    os.getcwd()+'/processed/'+f)
        
    table.close()
        
def parameters():
    global VERBOSE
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h','--help']:
            print("""Your options are as follows:
                     -h show this helptext
                     -v verbose output
                  """)
            exit()
        elif sys.argv[1] == '-v':
            print('yes')
            VERBOSE = True
        else:
            print('unknown parameter: '+sys.argv[1])

    
if __name__ == "__main__":
    parameters()
    main()
