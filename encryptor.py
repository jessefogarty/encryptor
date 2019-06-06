#!/usr/bin/env python3

import gnupg
import os
from termcolor import cprint
import getpass
import argparse

def encrypt_files(dloc, gpg_recv):
    # TODO: location selection - where are the files located?
    '''
        Encrypt files in a directory for a recipient.
            gpg_recv : str
                - recipient email address used for gpg encryption.
            dloc : str
                - path to directory containing unencrypted files.
            encrypted/ : dir
                - subdirectory storage for encrypted files.
    '''
    # Location for the user's GPG settings
    gpg = gnupg.GPG(gnupghome=os.path.expanduser('~/.gnupg'))
    os.chdir(os.path.expanduser(dloc))
    # Prepare file(s) in directory for encryption
    files_dir = []
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    for f in files:
        files_dir.append(f)

    if os.path.exists('encrypted/'):
        cprint('WARNING: Using existing /encrypted/ subdirectory', 'yellow')
    else:
        os.mkdir(u'encrypted')
        cprint('WARNING: Created /encrypted/ directory - moving encrypted files.', 'yellow')

    cprint('Starting file encryption...', 'yellow' )

    for x in files_dir:
        with open(x, mode='rb') as f:
            # output = files_dir[index(x)] to get file name + add suffix .gpg
            status = gpg.encrypt_file(f, recipients=gpg_recv, output=x+".gpg")
            status_msg = f'{x}: {status.status}'
            cprint(status_msg, 'green')

            os.rename(x + ".gpg", "encrypted/" + x + ".gpg")

def decrypt_files(dloc):
    '''
        Decrypt files in a directory using your user's default GPG key.
            dloc : string
                - Location of the directory containing encrypted ending in .gpg
    '''
    gpg = gnupg.GPG(gnupghome=os.path.expanduser('~/.gnupg'))

    if os.path.exists(dloc) is True:
        os.chdir(dloc)
        cprint(f'Changed working directory: {os.getcwd()}', 'yellow')
    else:
        cprint(f'ERROR: Subdirectory {dloc} not found!', 'red')

    efiles = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.gpg')]

    for f in efiles:
        stream = open(f, 'rb')
        dfile_name = os.path.splitext(f)[0]
        dfile = gpg.decrypt_file(stream, output=dfile_name)
        print(f'{f} status: {dfile.status}')

def sign_files():
    '''
        Sign and create a detached signature file for files in a directory.
    '''

    gpg = gnupg.GPG(gnupghome=os.path.expanduser('~/.gnupg'))
    os.chdir('encrypted')
    files_dir = []

    files = [f for f in os.listdir(".") if os.path.isfile(f)]

    # Add from files var to files_dir var
    for f in files:
        files_dir.append(f)

    gpg_pass = getpass.getpass('Enter your GPG password: ')
    for x in files_dir:
        with open(x, 'rb') as f:
            # sign each file and create the new file.sig
            signed_data = gpg.sign_file(f, passphrase=gpg_pass, detach=True, output=x+'.sig')
            # verify signature files to original data
            sname = x+'.sig'
            with open(sname, 'rb') as s:
                verified = gpg.verify_file(s, x)
                if not verified:
                    ver_err = x+': ' + verified.status + f'({sname})'
                    cprint(ver_err, 'red')
                ver_msg = x+': ' + verified.status + f'({sname})'
                cprint(ver_msg, 'green')
        # Move .sig files to /encrypted/
        #os.rename(x+".sig", "encrypted/"+ x +".sig")

def cli():
    parser = argparse.ArgumentParser(description='Encrypt files in a directory for a recipient.')
    parser.add_argument('--mode', help='Select run mode: encrypt or decrypt', metavar='<MODE>', nargs=1)
    parser.add_argument('--path', help='Path to directory', metavar='<PATH>', nargs=1)
    args = parser.parse_args()
    mode = args.mode[0] ; path = args.path[0]
    if args.mode[0] == 'encrypt':
        gpg_recv = input('Enter a recipient email address for encryption: ')
        encrypt_files(path, gpg_recv)
    elif args.mode[0] == 'decrypt':
        decrypt_files(args.path[0])
    else:
        print(f'Invalid argument: < --mode {args.mode[0]} > supplied. Please try again.')

if __name__ == "__main__":
    cli()
