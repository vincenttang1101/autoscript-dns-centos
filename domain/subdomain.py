import os

def addForwardFile(linkFile):
    domain = linkFile.replace("/var/named/forward.", "")
    fileOpen = open(linkFile, "a+")
    fileOpen.truncate(0)
    ipDomain = raw_input("Enter IP for this domain: ")
    completeForwardRecord  = '$TTL 86400' + '\n'
    completeForwardRecord += '@' + '\t' + 'IN  SOA' + '\t' + 'server.dns.vn.' + ' ' + 'root.dns.vn. (' + '\n'
    completeForwardRecord += '\t' + '2022240901' + '\t' + ';Serial' + '\n'
    completeForwardRecord += '\t' + '3600' + '\t' + ';Refresh' + '\n'
    completeForwardRecord += '\t' + '1800' + '\t' + ';Retry' + '\n'
    completeForwardRecord += '\t' + '604800' + '\t' + ';Expire' + '\n'
    completeForwardRecord += '\t' + '86400' + '\t'  + ';Minimum TTL' + '\n)' + '\n'
    completeForwardRecord += '@' + '\t' + 'IN  NS  server.dns.vn.' + '\n'
    completeForwardRecord += '@' + '\t' + 'IN  A' + ' ' +  ipDomain  + '\n'
    completeForwardRecord += 'server' + '\t' + 'IN  A' + ' ' + "192.168.1.100" + '\n'
    fileOpen.write(completeForwardRecord)
    fileOpen.close()
    statusAddForward = "1"
    return statusAddForward
    
def findForwardLine(linkFile, keyword):
    indexLine = ""
    if os.path.isfile(linkFile):
        domain = linkFile.replace("/var/named/forward.", "")
        fileOpen = open(linkFile, "r")
        lines = fileOpen.readlines()
        indexLine = -1 
        outLoop = 0
        for line in lines:
            countTemp = 0
            tempKeyword = ""
            indexLine += 1
            for character in line:
                tempKeyword += str(character)
                if " ".join(tempKeyword.split()) == " ".join(keyword.split()):
                    countTemp += 1000000
                    outLoop += 1
                    break
            if outLoop == 1:
                break
        if countTemp == 0:
            indexLine = -1000
        fileOpen.close()
    return indexLine
     
def delForwardLine(linkFile, indexLine):
    statusDelLine = "2"
    if os.path.isfile(linkFile) and indexLine >=0:
        fileOpen = open(linkFile, "a+")
        lines = fileOpen.readlines()
        del lines[indexLine]
        fileOpen.truncate(0)
        for lineNotDeleted in lines:
            fileOpen.write(lineNotDeleted)
        fileOpen.close()
        statusDelLine = "1"
    return statusDelLine 

def checkSubdomain(subdomain, domain):
    statusSubdomain = "2"
    indexLineForward = findForwardLine("/var/named/forward." + domain, subdomain)
    if indexLineForward >= 0 and isinstance(indexLineForward, int):
        statusSubdomain = "1"
    return statusSubdomain

def checkSubdomainSuper(domain):
    tempSubdomain = ""
    completeSubdomain = ""
    indexCharacter = -1
    statusSubdomainSuper = []
    statusDelDomain = ""
    tempDomain = ""
    for character in domain:
        tempSubdomain += str(character)
        indexCharacter += 1
        if character == ".":
            tempDomain = domain.replace(tempSubdomain, "")      
            completeSubdomain = tempSubdomain.replace(tempSubdomain[indexCharacter], "")
            statusSubdomain = checkSubdomain(completeSubdomain, tempDomain)
            if statusSubdomain == "1":
                statusSubdomainSuper.append("1")
                statusSubdomainSuper.append(completeSubdomain)
                statusSubdomainSuper.append(tempDomain)
                break
            elif statusSubdomain == "2":
                statusSubdomainSuper = "2"
    return statusSubdomainSuper

def addSubdomain(subdomain, domain):
    statusCheckSubdomain = checkSubdomain(subdomain, domain)
    statusAddSubdomain = "2"
    if statusCheckSubdomain == "1":
        print "This subdomain already exists"
    else:
        fileForwardRecord = open("/var/named/forward." + domain, "a+")
        ipSubdomain = raw_input("Enter IP for " + subdomain + "." + domain + ": ")
        completeForwardRecord = subdomain + '\t' + 'IN  A' + ' ' + ipSubdomain + '\n'
        fileForwardRecord.write(completeForwardRecord)
        fileForwardRecord.close()
        statusAddSubdomain = "1"
    return statusAddSubdomain

def editSubdomain(option, indexLine, replace, domain):
    statusEditSubdomain = "2"
    statusSubdomain = checkSubdomain(replace, domain)
    if statusSubdomain == "1":
        print "This subdomain already exists"
    elif statusSubdomain == "2":
        if indexLine >= 0 and isinstance(indexLine, int):
            fileOpen = open("/var/named/forward." + domain, "a+")
            lines = fileOpen.readlines()
            subdomainLine = lines[indexLine].split()
            subdomainComplete = " ".join(subdomainLine)
            delForwardLine("/var/named/forward." + domain, indexLine)
            if option == "1":
                tempWord = ""
                for word in subdomainLine:
                    tempWord += str(word) + " "
                    if word == "A":
                        break
                ipSubdomain = subdomainComplete.replace(tempWord, "")
                fileOpen.write(replace + '\t' + 'IN  A' + ' ' + ipSubdomain)
            elif option == "2":
                fileOpen.write(subdomainLine[0] + '\t' + 'IN  A' + ' ' + replace)
            fileOpen.close()
            statusEditSubdomain = "1"
    return statusEditSubdomain

def delSubdomain(subdomain, domain):
    statusDelSubdomain = "2"
    if os.path.isfile("/var/named/forward." + domain):
        fileOpen = open("/var/named/forward." + domain, "a+")
        lines = fileOpen.readlines()
        indexLine = findForwardLine("/var/named/forward." + domain, subdomain)
        lineDel = delForwardLine("/var/named/forward." + domain, indexLine)
        if lineDel == "1":
            statusDelSubdomain = "1"
    return statusDelSubdomain 