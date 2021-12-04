[Code and Resources](https://github.com/smartcontractkit/full-blockchain-solidity-course-py)

**VS Code extensions**

- Solidty
- Python
- Prettier
- Bracket Pair Colorizer

**Dependencies**

- Python/Python3

`$ sudo apt install npm (install Node.js and npm)`
Pip  
Ganache (local test network)
GUI: download the AppImage and run it
CLI: `$ npm install -g ganache-cli` (need root access, $sudo su first) 
    Or  
    `$npm install --global yarn`(need root permission, $sudo su) `$yarn global add ganache-cli` 
`$pip install py-solc-x (python solidity compiler)` `$pip install web3`
`$pip install python-dotenv (for managing private_key in the env)`

** Attention **

- When using python, need to add **"0x"** in front of the private key (if it's not there, e.g. Ganache GUI version). Python always looks for the hexadecimal version of the private key.
- don't forget put **.env** in **.gitignore**)
- run `$ganache-cli --deterministic` (close Ganache GUI first) and keep it running in a separate shell. **--deterministic** so addresses and keys won't change from run to run.
