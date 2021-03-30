#%%
import os
import pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build
from traverse_files import Drive

# Setup GDrive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'form-corp-data.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)
drive = Drive(drive_service)


def main():
    if not os.path.exists("docs/"): os.mkdir("docs/")

    # Search GDrive for all txt files
    files = drive.list_site_md()

    for txt in files:
        # Convert md to html
        if txt['name'].endswith('.md'):
            fcontent = drive.get_file_content(txt['id'])
            outfile = txt['name'].replace('.md', '.html.txt')
            Pandoc(fcontent, f"docs/{outfile}")


def Pandoc(mdstring, outfile):
    temp = "temp.txt"
    with open(temp, "w", encoding="utf-8") as f: f.write(mdstring)
    
    cmd = f'''
        ./pandoc
            {temp}
            -f markdown
            -o {outfile}
            --to=html5
            --section-divs
            --citeproc
            --bibliography="references.bib"
            --csl="apa.csl"
            --metadata link-citations=false
        '''
    cmd = [x.strip() for x in cmd.strip().split('\n')]
    status = os.system(' '.join(cmd))
    os.remove(temp) # Clean up

    if status != 0:
        print(f"[WARNING] Failed to make {outfile}")
    print(' '.join(cmd))

    return status



if __name__ == '__main__':
    main()