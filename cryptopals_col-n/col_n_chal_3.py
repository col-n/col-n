'''
cryptopals challenge 3
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
has been xor'd against a single character (presumably an ascii character)
decrypt the message
'''
#forgetting to account for spaces will throw things off ... 
#https://en.wikipedia.org/wiki/Letter_frequency
freqdic = {' ': 0.15}

#letter frequency in english - scaped from algorithmy.net
#quick refresher on web scraping and regular expressions
import urllib.request as ul
from bs4 import BeautifulSoup
import re, binascii
from Crypto.Util.strxor import strxor_c

url_root="http://en.algoritmy.net/article/40379/Letter-frequency-English"

url_response=ul.urlopen(url_root,data=None,timeout=5)
soup = BeautifulSoup(url_response)

table = soup.find('table', {'class': "default"})
pattern = re.compile(r"( [A-Z]).{11}(\d+.\d{3})")
for (letter, freq) in re.findall(pattern, str(table)):
    freqdic.update({letter.strip(): float(freq)/100})

#lookup the score of an individual character given a string of characters of finite length
def score(x):
    score = 0
    for i in x:
        char = chr(i).upper()
        if char in freqdic:
            score += freqdic[char]
    return score
    
def bustxor(x):
    #set each possible key and get its score ...
    def key(p):
        return score(p[1])
    #...and return the one with the highest score
    return max([(i, strxor_c(x,i)) for i in range(0,256)], key = key)

myster_code = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
u_m = binascii.unhexlify(myster_code)
broken_code = bustxor(u_m)
print('the key is',chr(broken_code[0]),'and the message is:',broken_code[1].decode('utf-8'))

