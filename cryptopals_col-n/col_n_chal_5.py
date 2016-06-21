'''
challenge 5
repeating key XOR
'''

	#this is a list comprehension that does the following, in order:
	#return as bytes (because we always work in bytes)
	#take each letter of s (our secret) and XOR (^) it against the key
	#as for which letter of the key, it is the ith element modulous the length of the secret s
	#in other words, we use modular arithmatic to automatically select the approprirate element of the key with regards to the secret

def repeatingxor(secret,key):
	return bytes([secret[i] ^ key[i % len(key)] for i in range(len(secret))])

#don't forget the b', as we always work in bytes
s_phrase = b'''Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal'''
my_key = b'ICE'

import binascii

cipher_text = repeatingxor(s_phrase, my_key)
#we have to display as hex instead of bytes, but they are equivalent
encoded_cipher = binascii.hexlify(cipher_text).decode('ascii')
print(encoded_cipher)

we_should_get = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

if encoded_cipher == we_should_get:
	print('it seems you have encrypted correctly')