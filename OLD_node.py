from blockchain import Blockchain
from wallet import Wallet
from uuid import uuid4
from utility.verification import Verification

class Node:
    def __init__(self):
        #self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)
        

    def get_transaction_value(self):
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Enter transaction amount: '))
        return (tx_recipient, tx_amount)

    def get_user_choice(self):
        user_input = input("Choice: ")
        return user_input

    def print_blockchain_elements(self):
        for block in self.blockchain.get_chain():
            print("-" * 20)
            print("outputting block ")
            print(block)
        else:
            print("-" * 20)

    def listen_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print("Please choose")
            print("1: Add new transaction value")
            print("2: Mine new block")
            print("3: Output blockchain blocks")
            print("4: Check transaction validity")
            print("5: Create wallet")
            print("6: Load wallet")
            print("7: Save Keys")
            print("Q: Exit")
            user_choice = self.get_user_choice()
            if user_choice == "1":
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print("Added transaction")
                else:
                    print("Transaction failed")
                print(self.blockchain.get_open_transactions())
            elif user_choice == "2":
                if not self.blockchain.mine_block():
                    print("Mining failed. Please check you have a wallet")
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(self.blockchain.get_open_transactions() , self.blockchain.get_balance):
                    print("All transactions valid")
                else:
                    print("Invalid transactions present")
            elif user_choice == "5":
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "6":
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "7":
                self.wallet.save_keys()
            elif user_choice.lower() =="q":
                waiting_for_input = False
            else:
                print("Invalid input, please choose an option from the list")
            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blockchain_elements()
                print("Invalid blockchain")
                break
            print('Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))

        print("Done!")

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()