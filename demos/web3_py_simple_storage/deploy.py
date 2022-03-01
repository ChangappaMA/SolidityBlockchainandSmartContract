from re import S
from solcx import compile_standard, install_solc

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

#Compile Solidity
install_solc("0.6.0")
complied_sol = compile_standard({
    "language" : "Solidity",
    "sources" : {"SimpleStorage.sol" : {"content": simple_storage_file}},
    "settings": {
        "outputSelection" : {
            "*" : {
                "*": ["abi", "metadata", "evm.bytecode","evm.sourceMap"]
            }
        }
    }
},
solc_version="0.6.0",
)

print(complied_sol)