
##########################
#     SHA-512 HASHER     #
##########################

# Import the HASHLIB library
import hashlib

def fGetHash(password):
    # Get password and change it into a hash using hashlib
    password = hashlib.sha512(bytes(password,encoding='ascii'))
    password = password.hexdigest()

    # Make the hash smaller for security purposes and to reduce database size
    passwordCut = password[:64]
    return passwordCut
