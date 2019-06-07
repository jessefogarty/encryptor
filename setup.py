import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(name='encryptor-dot-py', version='0.2', author='Jesse Fogarty',
                 author_email='jessefogarty@tuta.io', description='a tool to encrypt and decrypt directories.',
                 long_description=long_description, long_description_content_type='text/markdown',
                 url='https://github.com/jessefogarty/encryptor',packages=setuptools.find_packages(),
                 classifiers=[
                     'Development Status :: 4 - Beta',
                     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                     'Programming Language :: Python :: 3 :: Only'
                     'Topic :: Utilities'
                 ],)
