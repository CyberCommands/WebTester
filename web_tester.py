#!/usr/bin/env python3
# Coded by CyberCommands.
import os
import nmap
import time
import ipwhois
import socket
import requests
import dns.resolver
from pprint import pprint
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

os.system('cls' if os.name == 'nt' else 'clear')

print('\033[1;36m=\033[0m'*62)
print('\033[1;91m[!] WARNING: \033[0mThe Author is not responsible for illegal users.\n')
print('''\t\t     \033[1m[*] Options: \n
\033[1;33m\t[1] \033[1;32mIP Whois.
\033[1;33m\t[2] \033[1;32mWebsite Checker.
\033[1;33m\t[3] \033[1;32mPort Scanner.
\033[1;33m\t[4] \033[1;32mNmap Scanner.
\033[1;33m\t[5] \033[1;32mServer Information (HTTP Headers).
\033[1;33m\t[6] \033[1;32mNameservers of Domain.
\033[1;33m\t[7] \033[1;32mCMS Detector.
\033[1;33m\t[8] \033[1;32mExit. \n''')
print('\033[1;36m=\033[0m'*62)

def main():
    num = input('\n> CMD $ ')
    if num == '1':
        ip = input("[*] Enter Target IP: ")
        resault = ipwhois.IPWhois(ip).lookup_whois()
        pprint(resault)
        main()

    elif num == '2':
        addr = input("[*] Enter Target Url: ")
        try:
            response = urlopen(addr).getcode()
            #if response == 200:
            #    print('\033[92m[+] HTTP 200 Success. OK, this website is up. \033[0m')
            #if response == 400:
            #    print('\033[91m[-] HTTP 400 Client Errors. Bad Request. \033[0m')
            #if response == 500:
            #    print('\033[91m[-] HTTP 500 Server Errors. Internal Server Error. \033[0m')

        except URLError as err:
            print('\033[91m[-] Couldn\'t find a server.\033[0m')
            print('\033[91m[!] Reason: \033[0m', err.reason)

        except HTTPError as err:
            print('\033[91m[-] Couldn\'t check target Url. \033[0m')
            print('\033[91m[!] Error code: \033[0m', err.code)
        main()

    elif num == '3':
        site_ip = input("[*] Enter Target IP: ")
        try:
            for port in range(20, 1024):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn = sock.connect_ex((site_ip, port))
                if conn == 0:
                    print('Port \033[92m{}\033[0m:\t \033[92mOpen \033[0m'.format(port))
                    sock.close()

        except KeyboardInterrupt:
            print('\033[31m[!] \033[0m \033[33mCtrl +C Detected. Cancel Scanning... \033[0m')
            main()
        main()

    elif num == '4':
        target_ip = input("[*] Enter Target IP: ")
        res = nmap.PortScanner().scan(target_ip, "0-255")  # Range IP address.
        print(res)
        main()

    elif num == '5':
        server = input("[*] Enter Target Url: ")
        headers = requests.get(server).headers
        print("[*] Checking HTTP Header information...")
        time.sleep(1)
        # Headers is a dict so we can use items() function to get it as Key, Value.
        for key, value in headers.items():
            print(key + "\t\t \033[92m ==> \033[0m " + value)
        main()

    elif num == '6':
        dom = input("[*] Enter Target Address (example.com): ")
        ans = dns.resolver.query(dom, 'NS')
        for server in ans:
            print(server)
        main()

    elif num == '7':
        site = input("[*] Enter Target Url: ")

        # Wordpress Scanner.
        print("\n[*] Scan for WordPress...")
        time.sleep(1.5)

        wpLcheck = requests.get(site + "/wp-login.php")
        if wpLcheck.status_code == 200 and "user_login" in wpLcheck.text and "404" not in wpLcheck.text:
            print("\033[92m[+] WordPress detected: Admin Panel ➤ \033[0m" + site + "/wp-admin.php")
        else:
            print("\033[91m[-] WordPress not detected. \033[0m")
            pass

        wpAcheck = requests.get(site + "/wp-admin")
        if wpAcheck.status_code == 200 and "user_login" in wpAcheck.text and "404" not in wpAcheck.text:
            print("\033[92m[+] WordPress detected: Admin Panel ➤ " + site + "/wp-admin")
        else:
            pass

        # Joomla Scanner.
        print("\n[*] Scan for Joomla...")
        time.sleep(1.5)
        
        jmAcheck = requests.get(site + "/administrator")
        if jmAcheck.status_code == 200 and "mod-login-username" in jmAcheck.text and "404" not in jmAcheck.text:
            print("\033[92m[+] Joomla detected: Admin Panel ➤ \033[0m" + site + "/administrator")
        else:
            print("\033[91m[-] Joomla not detected. \033[0m")
            pass

        jmScheck = requests.get(site)
        if jmScheck.status_code == 200 and "joomla" in jmScheck.text and "404" not in jmScheck:
            print("\033[92m[+] Joomla detected: 'joomla' on index. \033[0m")
        else:
            pass

        # Drupal Scanner.
        print("\n[*] Scan for Drupal...")
        time.sleep(1.5)
        drRcheck = requests.get(site + "/readme.txt")
        if drRcheck.status_code == 200 and 'drupal' in drRcheck.text and '404' not in drRcheck.text:
            print("\033[92m[+] Drupal detected: Drupal Readme.txt ➤ \033[0m" + site + '/readme.txt')
        else:
            print("\033[91m[-] Drupal not detected. \033[0m")
            pass

        drCcheck = requests.get(site + '/core/COPYRIGHT.txt')
        if drCcheck.status_code == 200 and 'Drupal' in drCcheck.text and '404' not in drCcheck.text:
            print("\033[92m[+] Drupal detected: Drupal COPYRIGHT.txt ➤ \033[0m" + site + '/core/COPYRIGHT.txt')
        else:
            pass

        # Magento Scanner.
        print("\n[*] Scan for Magento...")
        time.sleep(1.5)

        mgRcheck = requests.get(site + '/RELEASE_NOTES.txt')
        if mgRcheck.status_code == 200 and 'magento' in mgRcheck.text:
            print("\033[92m[+] Magento detected: Magento Release_Notes.txt ➤ \033[0m" + site + '/RELEASE_NOTES.txt')
        else:
            print("\033[91m[-] Magento not detected. \033[0m")
            pass

        mgCcheck = requests.get(site + '/js/mage/cookies.js')
        if mgCcheck.status_code == 200 and "404" not in mgCcheck.text:
            print("\033[92m[+] Magento detected: Magento cookies.js: \033[0m" + site + '/js/mage/cookies.js')
        else:
            pass
        main()

    elif num == '8':
        quit()

    else:
        print("\033[1;31m[!!] Wrong Input. \033[0m")
        main()

if __name__ == '__main__':
    main()
