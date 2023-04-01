
from domain import *
import os

def main():
    while True:
        print('''
    _         _          ____            _       _   
   / \  _   _| |_ ___   / ___|  ___ _ __(_)_ __ | |_ 
  / _ \| | | | __/ _ \  \___ \ / __| '__| | '_ \| __|
 / ___ \ |_| | || (_) |  ___) | (__| |  | | |_) | |_ 
/_/   \_\__,_|\__\___/  |____/ \___|_|  |_| .__/ \__|
                                          |_|     
        ''')
        optionDomain = int(raw_input("################# Domain Management #################\n1: Add Domain\n2: Edit Domain\n3: Delete Domain\n4: nslookup\n5: Exit\nEnter option: "))
        if optionDomain == 1:
            domain = raw_input("Enter the domain to add: ")
            addDomain(domain)
        elif optionDomain == 2:
            domain = raw_input("Enter the domain to edit: ")
            editDomain(domain)
        elif optionDomain == 3:
            domain = raw_input("Enter the domain to delete: ")
            delDomain(domain)
        elif optionDomain == 4:
            domain = raw_input("Enter the domain to resolve: ")
            print (os.system("nslookup " + domain))
        elif optionDomain == 5:
            exit()
main()
