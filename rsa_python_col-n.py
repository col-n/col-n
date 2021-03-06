__author__ = 'col-n'
import timeit, random
'''
A python implementation of RSA (https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29).
Finds random prime numbers of specified length (up to 32 bits).
Demonstrates why larger numbers are better by factoring the resulting private key from the computed public key,
using a very unsophisticated factoring method.

Uses the built in python bitwise exclusive or operator
'''

#let's define some functions for generating random numbers of length n.
#we do this by generating many random numbers via the crpyographically accecptable random.SystemRandom.
#generating lots of numbers and taking the least significant bit ensure maximum entropy ... which is good

def pprime(length):
    import random
    if length > 32:
        print('max length is 32!')
        return None
    if length < 5:
        print('min length is 5!')
    pos_prime = '1'
    for i in range(1,length):
        x = str(('{0:032b}'.format(random.SystemRandom().randint(1, 4294967295))))
        pos_prime = pos_prime+x[-1]
    pos_prime = pos_prime+'1'
    return pos_prime

'''
RSA depends on getting prime numbers and then doing things to them, like multiplying and taking exponents.
While we could use python's built in modular exponentiation algo, lets make our own
'''

def faste(a,x,n):
    x = "{0:b}".format(x)
    l = len(x)
    y = 1
    for i in range(0,l):
        y = (y * y) % n
        if x[i] == '1':
            y = (a * y) % n
    return y

'''
We need to test whether our random number is prime. We will use the Miller-Rabin Algo.
https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
we need to fina random 'a' and take its exponent to the power of our 'possibly prime' minus 1,
to the modulus of our 'possibly prime'. There are other tests we do that you can read about in the wiki article

'''

#we need to generate lots of 'a's ...

def randoma(n):
    import random
    if type(n) is str:
        n = int(n,2)
    n = n-1
    #in binary
    #i = linno()+'the random a to be tested is: '+str(('{0:032b}'.format(random.SystemRandom().randint(1, mya))))
    a = random.SystemRandom().randint(1, n)
    return a

def millerrab(a, n):
    #test for bad square root and that a isn't 1 or n-1
    if (a*a%n) is 1 and a !=1 and a !=n-1:
        return 0
    #test a**(n-1) mod n; ensure it does not equal 1
    #a return of 0 means 'n is definitely not prime'
    if faste(a,(n-1),n) != 1:
        return 0
    #a return of 1 means that 'n is possibly a prime'
    else:
        return 1

#we'll test a certain number of 'a's to be 'sure' (probibalistcally speaking) we have a prime number
def isprime(num):
    if type(num) is str:
        num = int(num,2)
    ppint = num
    primelist = 0
    #set the number of tests by changing the range. Most people in real implementations use 100.
    for i in range (1, 101):
        testa = randoma(ppint)
        #print('the ',i,'a to be tested is:',testa)
        isprime = millerrab(testa,ppint)
        if isprime is 0:
            #print("n is not prime")
            return 0
            break
        primelist += isprime
    if primelist > 99:
        #print('n is likely prime enough for our purposes')
        return 1

'''
Now we're ready to generate a list of 2 random prime numbers, which we will use to construct the private and public key
I add a while loop to check that the prime numbers are different, which is an issue for small bit lengths
'''
def getprimes(length):
    listoprimes=[]
    while len(listoprimes) <2:
        x = 0
        while x < 1:
            pp = pprime(length)
            x+=isprime(pp)
        y = int(pp,2)
        if y not in listoprimes:
            listoprimes.append(y)
        else:
            getprimes(length)
    return listoprimes
'''
There are three people in our system: Alice, Bob, and Trent.  Alice and Bob wish to communicate.
Trent is the 'trusted' authority who signs Alice's public key so that Bob can be sure he is communicating with Alice.

We have generated two primes, p and q. We get the phi-n of them by (p-1) * (q-1).
We then find "n" by multiplying p * q.
We then find "e", the public key, by find a small number that is relatively prime with phi-n.
We then find "d", the private key, but getting the modular inverse
(https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) of 'e' to the moduluous of phi-n

'''

#extended euclidean algorithm on 'a' and 'b'.  Set the constants and continue in a loop.
#return the greatest common denominator and the multiplicative inverse and modulo
def xgcd(a, b):
    x = 0
    y = 1
    u = 1
    v = 0
    while a != 0:
        q = b//a
        r = b%a
        m = x-u*q
        n = y-v*q
        b = a
        a = r
        x = u
        y = v
        u = m
        v = n
    gcd = b
    return gcd, x, y

#getting phi_n, the product of our two primes minus 1
def getphi(n):
    phi_n = (n[0]-1)*(n[1]-1)
    return phi_n

#get n, the product of two primes, in the form of a list of exactly two primes generated by the 'get primes' function
def getn(lp):
    n = lp[0] * lp[1]
    return n

#find a small number that is relatively prime with phi_n to be the public key e
#modern protocalls all use the same exponent, which is 65537, which is not necessary, but useful as it is easy to use

def find_rprime(phi_n):
    f100p = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
             109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
             229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
             353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467,
             479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613,
             617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751,
             757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
             907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033,
             1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153,
             1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283,
             1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427,
             1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531,
             1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637,
             1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783,
             1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913,
             1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053,
             2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179,
             2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297, 2309, 2311,
             2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423, 2437,
             2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591, 2593,
             2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711,
             2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837,
             2843, 2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971,
             2999, 3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137,
             3163, 3167, 3169, 3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257, 3259, 3271, 3299,
             3301, 3307, 3313, 3319, 3323, 3329, 3331, 3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413,
             3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547,
             3557, 3559, 3571, 3581, 3583, 3593, 3607, 3613, 3617, 3623, 3631, 3637, 3643, 3659, 3671, 3673, 3677,
             3691, 3697, 3701, 3709, 3719, 3727, 3733, 3739, 3761, 3767, 3769, 3779, 3793, 3797, 3803, 3821, 3823,
             3833, 3847, 3851, 3853, 3863, 3877, 3881, 3889, 3907, 3911, 3917, 3919, 3923, 3929, 3931, 3943, 3947,
             3967, 3989]
    for item in f100p:
        gcd, x, y = xgcd(item,phi_n)
        if gcd != 1:
            continue
        else:
            return item

#find the modular inverse of 'e' above modulo phi_n, which is the private key d, first testing if one exists
def modinv(a,m):
    gcd, x, y = xgcd(a,m)
    if gcd != 1:
        return None
    else:
        return x % m

#we will need to hash a 'challenge' that alice and bob will mutually agree on.
#I will use a trivial one by taking the exclusive or of byte strings, but this could easily be extended to use a real one
#PSA. Don't use MD5 or SHA-1 - they are broken. Use SHA2 or better.

#take a list of bits as a string and return a list of bytes as integers
def get_list_bytes(st):
    b_list = []
    l = int(len(st)/8)+1
    for i in range(1,l):
        p1 = (i-1)*8
        p2 = p1+7
        byte = st[p1:p2]
        b_list.append(int(byte,2))
    return b_list

#take the exclusive or
def hash(mylist):
    result = 0
    for i in mylist:
        result ^= i
    return result

#given a compound integer of length n, determine the length in bits of the challenge (k) and each parties portion (u)
#returns the length of k, u1, u2
def find_k_u(anyn):
    in_bits = '{0:032b}'.format(anyn)
    in_bits = in_bits.strip('0')
    len_k = len(in_bits)-1
    each_u = (len_k-1)/2
    if ((len_k-1)  % 2 == 0):
        return len_k, int(each_u), int(each_u)
    else:
        return len_k, int(each_u+.5), int(each_u-.5)

#find a random string of bits and return it as a string. this is bob or alice's portion.
def find_my_u(anyu):
    import random
    myu='1'
    for i in range(1,anyu+1):
        i = str(('{0:032b}'.format(random.SystemRandom().randint(1, 4294967295))))
        myu+=i[-1]
    return myu

#some of the less interesting and tedious portions are left out. 

#Alice
primelist1 = getprimes(13)

#Trent
primelist2 = getprimes(13)

# get phi_n for alice...
phin1 = getphi(primelist1)

# ...and trent
phin2 = getphi(primelist2)

# get n for alice ...
alicen = getn(primelist1)

# ... and trent
trentn = getn(primelist2)

#get e for alice ...
alicee = find_rprime(phin1)

#... and trent
trente = find_rprime(phin2)
print('alice e is:',alicee)

#get d for alice ...
aliced = modinv(alicee,phin1)

# ... and trent
trentd = modinv(trente,phin2)
print('alice d is:',aliced)

print('Alices p=',primelist1[0],'q=',primelist1[1],'n=',alicen,'e=',alicee,'d=',aliced)

#trent will sign 'r', a string with padding, alice's info, and alice's public key and n
padding = '00000000'
string_alice = '{0:08b}'.format(ord('a'))+'{0:08b}'.format(ord('l'))+'{0:08b}'.format(ord('i'))+'{0:08b}'.format(ord('c'))+'{0:08b}'.format(ord('e'))
r = padding+string_alice+'{0:064b}'.format(alicen)+'{0:064b}'.format(alicee)

# create a list of the bytes and convert to integers for XOR...
b_list_1 = get_list_bytes(r)

trent_hash = hash(b_list_1)

#decrypt the hash with trent private key d:
s = faste(trent_hash, trentd, trentn)
#print r, h(r), s
print('r:',int(r,2))
print('h(r):',trent_hash)
print('s   :',s)

#get the length of the challenge, k, and u bob and u alice, and concatenate them.
#in real life this would be a bunch of communication between them.
a_b_k = find_k_u(alicen)
alice_u = find_my_u(a_b_k[1])
bob_u = find_my_u(a_b_k[2])
the_u = alice_u+bob_u
print('k is:',a_b_k[0])
u = int(the_u,2)
print('u is:',int(the_u,2))

#hash u ...
hash_of_u = hash(get_list_bytes(the_u))
print('h(u):',hash_of_u)

#alice decrypts u with her private key, getting 'v'
alice_v = faste(hash_of_u, aliced, alicen)

#bob checks ...
bob_v_check = faste(alice_v,alicee,alicen)
print('v(d,h(u))=',alice_v)
print('e(e(v)=',bob_v_check)

if bob_v_check == hash_of_u:
    print('you are talking to someone who knows alices private key!')
else:
    print('something is wrong. it is either mallory, or your code ...')

#see how long it takes your computer generate p and q and then to factor the numbers back.


def getprimestime(length):
    start_time = timeit.default_timer()
    listoprimes=[]
    while len(listoprimes) <2:
        x = 0
        while x < 1:
            pp = pprime(length)
            x+=isprime(pp)
        y = int(pp,2)
        if y not in listoprimes:
            listoprimes.append(y)
        else:
            getprimes(length)
    time1 = timeit.default_timer() - start_time
    return listoprimes, time1


def factorstime(n):
    start_time = timeit.default_timer()
    wheel = [1,2,2,4,2,4,2,4,6,2,6]
    w, f, fs = 0, 2, []
    while f*f <= n:
        while n % f == 0:
            fs.append(f)
            n /= f
        f, w = f + wheel[w], w+1
        if w == 11: w = 3
    if n > 1: fs.append(int(n))
    time2 = timeit.default_timer() - start_time
    return fs, time2

#try creating and factoring random bit lengths from  ... warning, this will take a long time with long bit lengths!
mylist = [10,11]

clist = []
flist = []
for i in mylist:
    x,y = getprimestime(i)
    n = (x[0]*x[1])
    #print(n)
    clist.append(y)
    a,b = factorstime(n)
    flist.append(b)
print(clist)
print(flist)

'''
I used the algo above on bit lengths of 10-32 bits.  The results are below for a comp with ~3 GHz i7 and 16 GB ram.

in seconds:
bits	create	factor
10	0.005270632	0.000109706
11	0.005230701	0.000200344
12	0.005701843	0.000397583
13	0.006957714	0.001013058
14	0.004791609	0.001461723
15	0.004986819	0.002961732
16	0.007940306	0.005981596
17	0.006514073	0.018513429
18	0.005834183	0.025434709
19	0.013100112	0.049306284
20	0.005732156	0.092054049
21	0.006645892	0.198051598
22	0.004625693	0.344946078
23	0.007271184	0.804739178
24	0.010514663	1.766220151
25	0.007118291	4.565575443
26	0.008802504	8.07297894
27	0.00619971	16.92048314
28	0.013204597	23.02109739
29	0.007593304	65.92335069
30	0.011055429	108.7945463
31	0.009474718	336.7977034
32	0.021832555	598.2711962

As you can see, past trivial bit lengths (at about 24 bits) each additional bit about doubles the amount of time to 
factor while having basically no effect on the time to create the factor.

'''
#for a great webcomic on passwords ...
#a good password: https://xkcd.com/936/
#https://drive.google.com/open?id=0B5eMNCdPTsppR1puTUEzeGg2dWs
