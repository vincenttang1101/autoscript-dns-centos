import os
from subdomain import *

def findZoneLine(linkFile, keyword, domain):
    indexLine = ""
    if os.path.isfile(linkFile):
        fileOpen = open(linkFile, "r")
        lines = fileOpen.readlines()
        indexLine = -1
        numberLines = sum(1 for countLine in lines) - 1
        for line in lines:
            tempKeyword = ""
            indexLine += 1
            tempDomain = ""
            indexCharacter = -1
            countTemp = 0
            outLoop = 0
            for character in line:
                indexCharacter += 1 
                tempKeyword += str(character)
                if tempKeyword == keyword: 
                    countTemp += 1
                if countTemp == 1:
                    tempDomain += str(line[indexCharacter + 1])
                    if line[indexCharacter + 2] == '"':
                        countTemp -= 1
                        if tempDomain == domain:
                            outLoop += 1
                            break
            if outLoop == 1:
                break
        if indexLine == numberLines:
            indexLine = -1000
        fileOpen.close()
    return indexLine

def delZoneLine(indexLine):
    statusDelZoneLine = "2"
    if os.path.isfile("/etc/named.rfc1912.zones") and indexLine >= 0:
        fileOpen = open("/etc/named.rfc1912.zones", "a+")
        lines = fileOpen.readlines()
        del lines[indexLine]
        del lines[indexLine]
        del lines[indexLine]
        del lines[indexLine]
        del lines[indexLine] 
        fileOpen.truncate(0)
        for lineNotDeleted in lines:
            fileOpen.write(lineNotDeleted)    
        fileOpen.close()
        statusDelZoneLine = "1"
    return statusDelZoneLine 

def delZoneLine_2(domain, indexLine):
    oldFile = open("/etc/named.rfc1912.zones", "r+")
    oldLines = oldFile.readlines()
    oldForwardFile = oldLines[indexLine + 2].strip()
    tempForward = ""
    completeForward = ""
    indexCharacter = -1
    countTemp = 0
    statusDelZoneLine_2 = ""
    for character in oldForwardFile:
        tempForward += str(character)
        indexCharacter += 1
        if tempForward == 'file "':
            countTemp += 1
        if countTemp == 1:
            completeForward += str(oldForwardFile[indexCharacter + 1])
            if oldForwardFile[indexCharacter + 2] == '"':
                break
    statusDelZoneLine = delZoneLine(indexLine)
    if statusDelZoneLine == "1": 
        statusDelZoneLine_2 = "1"
    else: statusDelZoneLine_2 = "2"
    return statusDelZoneLine_2

def delFile(linkFile):
    statusDelFile = "2"
    if os.path.isfile(linkFile):
        os.remove(linkFile)
        statusDelFile = "1"
    return statusDelFile

def addZone(domain):
    fileOpen = open("/etc/named.rfc1912.zones", "a")
    completeDomain = '\nzone "' + domain + '" IN {\n'
    completeDomain += '\ttype master; \n'
    completeDomain += '\tfile "' + 'forward.' + domain + '";\n'
    completeDomain += '\tallow-update { none; };\n'
    completeDomain += '};'    
    fileOpen.write(completeDomain)
    fileOpen.close()
    statusAddZone = "1"
    return statusAddZone

def checkDomain(domain):
    indexLineZone = findZoneLine("/etc/named.rfc1912.zones", 'zone "', domain)
    statusDomain = []
    if indexLineZone >=0:
        statusDomain.append("1")
        statusDomain.append(indexLineZone)
    else: 
        statusDomain = "2"
    return statusDomain

def checkDomainSuper(domain):
    statusDomainSuper = ""
    statusCheckDomain = checkDomain(domain)
    if statusCheckDomain[0] == "1":
        statusDomainSuper = "1"
    elif statusCheckDomain == "2":
        statusSubdomainSuper = checkSubdomainSuper(domain)
        if statusSubdomainSuper[0] == "1":
            statusDomainSuper = []
            statusDomainSuper.append("2")
            statusDomainSuper.append(statusSubdomainSuper[1])
            statusDomainSuper.append(statusSubdomainSuper[2])
        else: statusDomainSuper = "3"
    return statusDomainSuper 

def editDomainInZone(domain, replaceDomain):
    statusEditDomainInZone = "2"
    statusDomain = checkDomain(replaceDomain) 
    if statusDomain[0] == "1":
        statusEditDomainInZone = "2"
    elif statusDomain == "2":
        indexLineZone = findZoneLine("/etc/named.rfc1912.zones", 'zone "', domain)
        if indexLineZone >=0 and isinstance(indexLineZone, int):
            statusDelZoneLine_2 = delZoneLine_2(domain, indexLineZone)
            if statusDelZoneLine_2 == "1":
                os.rename("/var/named/forward." + domain, "/var/named/forward." + replaceDomain)
                addZone(replaceDomain)
                statusEditDomainInZone = "1"
    return statusEditDomainInZone 

def editIPDomain(ip, domain):
    statusEditIPDomain = "2"
    indexLine = findForwardLine("/var/named/forward." + domain, "@ IN A")
    if indexLine >=0 and isinstance(indexLine, int):
        statusDelForwardLine = delForwardLine("/var/named/forward." + domain, indexLine)
        if statusDelForwardLine == "1":
            fileOpen = open("/var/named/forward." + domain, "a")
            fileOpen.write('@' + '\t' + 'IN  A' + ' ' +  ip)
            fileOpen.close()
            statusEditIPDomain = "1"
    return statusEditIPDomain

"""
def addDomain(domain):
    statusAddDomain = "2"
    statusDomain = checkDomainSuper(domain)
    if statusDomainSuper == "1":
        inputOption_2 = raw_input("This domain already exists\nDo you want to add a subdomain? (y/n): ")
        if inputOption_2.lower() == "y":
            inputSubdomain_2 = raw_input("Enter subdomain you want to add: ")
            statusAddSubdomain = addSubdomain(inputSubdomain_2, domain)
            if statusAddSubdomain == "1":
                print "This subdomain has been successfully added"
                os.system("systemctl restart named")
            else: print "This subdomain has been unsuccessfully added"
    elif statusDomainSuper[0] == "2":
        inputOption = raw_input("Type: subdomain\nDo you want to add another subdomain of " + statusDomainSuper[2] + "? (y/n): ")
        if inputOption.lower() == "y":
            inputSubdomain = raw_input("Enter subdomain you want to add: ")
            statusAddSubdomain = addSubdomain(inputSubdomain, statusDomainSuper[2])
            if statusAddSubdomain == "1":
                print "This subdomain has been successfully added"
                os.system("systemctl restart named")
            else: print "This subdomain has been unsuccessfully added"
    else: 
        if domain
        statusAddForward = addForwardFile("/var/named/forward." + domain)
        if statusAddForward == "1":
            statusAddZone = addZone(domain)
            if statusAddZone == "1":
                print "This domain has been successfully added" 
                os.system("systemctl restart named")
                statusAddDomain = "1"
        else: 
            print "This domain has been unsuccessfully added"
    return statusAddDomain
"""

def addDomain(domain):
    statusAddDomain = "2"
    statusDomain = checkDomain(domain)
    if statusDomain[0] == "1":
        inputSubdomain = raw_input("This domain already exists\nDo you want to add a subdomain? (y/n): ")
        if inputSubdomain.lower() == "y":
            inputSubdomain_2 = raw_input("Enter subdomain you want to add: ")
            statusAddSubdomain = addSubdomain(inputSubdomain_2, domain)
            if statusAddSubdomain == "1":
                print "This subdomain has been successfully added"
                os.system("systemctl restart named")
            else: print "This subdomain has been unsuccessfully added"
    elif statusDomain == "2":
        statusAddForward = addForwardFile("/var/named/forward." + domain)
        if statusAddForward == "1":
            statusAddZone = addZone(domain)
            if statusAddZone == "1":
                print "This domain has been successfully added" 
                os.system("systemctl restart named")
                statusAddDomain = "1"
        else: 
            print "This domain has been unsuccessfully added"
    return statusAddDomain

def editDomain(domain):
    statusEditDomain = "" 
    statusDomain = checkDomain(domain)
    if statusDomain[0] == "1":
        optionDomain = raw_input("Type: domain\n1: Edit domain\n2: Edit IP\nEnter option: ")
        if optionDomain == "1":
            inputEditDomain = raw_input("Enter the domain you want to replace: ")
            statusEditDomainInZone = editDomainInZone(domain, inputEditDomain)
            if statusEditDomainInZone == "1":
                print "Edit domain successfully"
                os.system("systemctl restart named")
                statusEditDomain = "1"
            else: 
                print "Edit domain unsuccessfully"
                statusEditDomain = "2"
        elif optionDomain == "2":
            inputEditDomain = raw_input("Enter IP you want to replace: ")
            statusEditIPDomain = editIPDomain(inputEditDomain, domain)
            if statusEditIPDomain == "1":
                print "Edit IP of domain successfully"
                os.system("systemctl restart named")
            else: print "Edit IP of domain unsuccessfully"
    elif statusDomain == "2":
        statusSubdomainSuper = checkSubdomainSuper(domain)
        if statusSubdomainSuper[0] == "1":
            optionSubdomain = raw_input("Type: subdomain\n1: Edit subdomain\n2: Edit IP\nEnter option: ")
            indexLine = findForwardLine("/var/named/forward." + statusSubdomainSuper[2], statusSubdomainSuper[1])
            if optionSubdomain == "1":
                inputSubdomain = raw_input("Enter subdomain of " + statusSubdomainSuper[2] + " you want to replace: ")
                statusEditSubdomain = editSubdomain(optionSubdomain, indexLine, inputSubdomain, statusSubdomainSuper[2])
                if statusEditSubdomain == "1":
                    print "Edit subdomain successfully"
                    os.system("systemctl restart named")
                else: print "Edit subdomain unsuccessfully"
            elif optionSubdomain == "2":
                inputIPSubdomain = raw_input("Enter IP subdomain of " + statusSubdomainSuper[2]  + " you want to replace: ")
                statusEditSubdomain = editSubdomain(optionSubdomain, indexLine, inputIPSubdomain, statusSubdomainSuper[2])
                if statusEditSubdomain == "1":
                    print "Edit subdomain successfully"
                    os.system("systemctl restart named")
                else: print "Edit subdomain unsuccessfully"
        elif statusSubdomainSuper == "2":
            print "This domain does not exist"
    return statusEditDomain

def delDomain(domain):
    outLoop = 0
    statusDelDomain_2 = ""
    statusDomain = checkDomain(domain)
    if statusDomain[0] == "1":
        inputDomain = raw_input("This is a domain. Do you want delete it? (y/n): ")
        if inputDomain.lower() == "y":
            statusDelZoneLine = delZoneLine(int(statusDomain[1]))
            if statusDelZoneLine == "1":
                statusDelFile = delFile("/var/named/forward." + domain)
                if statusDelFile == "1":
                    statusDelDomain_2 = "1"
                    print "This domain has been successfully deleted"
                    os.system("systemctl restart named")
                else: 
                    statusDelDomain_2 = "2"
                    print "This domain has been unsuccessfully deleted"
    elif statusDomain == "2":
        inputSubdomain = raw_input("This domain can be a subdomain or nothing. Do you want delete it? (y/n): ")
        if inputSubdomain.lower() == "y":
            statusSubdomainSuper = checkSubdomainSuper(domain)
            if statusSubdomainSuper[0] == "1":
                statusDelDomain = delSubdomain(statusSubdomainSuper[1], statusSubdomainSuper[2])
                if statusDelDomain == "1":
                    print "This subdomain has been successfully deleted"
                    os.system("systemctl restart named")
                else: print "This subdomain unsuccessfully deleted"
            else: print "This domain does not exist"
    return statusDelDomain_2