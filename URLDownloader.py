import os
import sys
import requests
import  urllib.request
from urllib.parse import urlparse 

# Checking if url link is downloadable or not
def IsDownloadable(url):
    h = requests.head(url, allow_redirects = True)
    header = h.headers
    content_type = header.get("content-type")
    print(content_type)
    if 'text' in content_type.lower():
        return False
    
    if 'html' in content_type.lower():
        return False
    return True

def isConnection():
    try:
        urllib.request.urlopen(url = 'http://216.58.192.142',timeout = 4)
        return True

    except urllib.error.URLError:
        return False


def GetFilenameFromCD(url):
    a = urlparse(url)
    return os.path.basename(a.path)

def Download(url, directive):

    allowed  = IsDownloadable(url)
    
    if allowed:#if true

        try:
            print(url)
            filename = GetFilenameFromCD(url)
            destPath = os.path.join(directive,filename)

            res = requests.get(url, stream = True)
            with open(destPath , "wb") as fd:
                for chunk in res.iter_content(chunk_size=1024): 
                    if chunk:
                        fd.write(chunk)
        except Exception:
            print("Exception")
            return False
    else:
        print("File is not downloadable")
        return False

def DownloadFiles(linkFile , directive):

    connection = isConnection()

    if connection:
        if not os.path.isabs(directive):
            directive = os.path.abspath(directive)

        if not os.path.exists(directive):
            os.mkdir(directive)

        if(os.path.exists(linkFile)):
            with open(linkFile , "r") as fp:
                for url in fp:
                    Download(url,directive)
        else:
            print("File which content link is not found\n")
    else:
        print("No internet connection\n")

def main():
    if len(sys.argv) < 2:
        print("Downloader_Error: Invalid argument")
        exit()

    #Help
    if sys.argv[1] == '-h' or sys.argv[1] == '-H':
        print("Downloader_Help: Download files from URL's spacified in file")
        exit()

    # Usage
    if sys.argv[1] == '-u' or sys.argv[1] == '-U':
        print(f"Downloader_Usage: {sys.argv[0]}  FileName  DirName")
        print("FileName: File which contains list of URL's")
        print("DirName: Name of directory to store downloaded files")
        exit()
    
    if len(sys.argv) != 3:
        print("Downloader__Error: Invalid arguments")
        exit()

    DownloadFiles(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    main()
