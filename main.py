from keys_generator import *
from trng_generator import *
from create_signature import *
from verify_signature import *

keys_generator(trng_generator())

file_name = input('Insert file name to sign: ')

create_signature(file_name)

file_name = input('Insert file name to verify: ')

verify_signature(file_name)

print('Verified')