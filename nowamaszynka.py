# twitch-downloader

import os
ffmpeg_path = "ffmpeg" #dodatkowo ffmpeg był potrzebny to musiałem go dodatkowo doinstalować "TwitchDownloaderCLI ffmpeg -d" ta komenda pomogła
twitch_cli_path = "TwitchDownloaderCLI.exe" #tutaj podaje nazwe executable pliku TwitchDownloaderCLI, jak masz Mac'a to tu można znaleźć inne wersje https://github.com/lay295/TwitchDownloader/releases/
# to exe wyżej pobrałem stąd https://github.com/lay295/TwitchDownloader/releases/download/1.54.0/TwitchDownloaderCLI-1.54.0-Windows-x64.zip wystarczy potem wypakować exe i wrzucić w główny folder
def create_catalog(name):
    try:
        os.mkdir(name)
        print("Utworzono folder o nazwie:", name)
    except FileExistsError:
        print("Folder o nazwie", name, "już istnieje.")


with open("input.txt", "r") as file:
    date = file.readline().strip()
    vodId = file.readline().strip()
    main_catalog = vodId

    create_catalog(main_catalog)

    for line in file:
        timestamps = line.strip().split(" ")
        start, end, title = timestamps[1], timestamps[3], timestamps[4]

        start_h, start_m, start_s = start.split(":")
        start_sec = int(start_h) * 3600 + int(start_m) * 60 + int(start_s)

        end_h, end_m, end_s = end.split(":")
        end_sec = int(end_h) * 3600 + int(end_m) * 60 + int(end_s)
        
        
        print(title, start_sec, end_sec)

        #get clip
        clip_catalog_path = f'{main_catalog}/{title}'
        create_catalog(clip_catalog_path)
        getClipCommand = f'{twitch_cli_path} videodownload --id {vodId} --ffmpeg-path {ffmpeg_path} -o {clip_catalog_path}/{title}.mp4 -b {start_sec} -e {end_sec}'
        os.system(getClipCommand)

        #get chat
        getChatCommand = f'{twitch_cli_path} chatdownload --id {vodId} -o {clip_catalog_path}/{title}-chat.json -b {start_sec - 60} -e {end_sec}'
        os.system(getChatCommand)

        #chatupdate
        #renderChatCommand = f'{twitch_cli_path} videodownload --id {vodId} --ffmpeg-path {ffmpeg_path} -o {clip_catalog_path}/{title}.mp4 -b {start_sec} -e {end_sec}'
        #os.system(renderChatCommand)

        #render chat
        renderChatCommand = f'{twitch_cli_path} chatrender -i {clip_catalog_path}/{title}-chat.json -w 500 -h 1080 --background-color 000000 --font-size 24 --ffmpeg-path {ffmpeg_path} -o {clip_catalog_path}/{title}-chat.mp4'
        os.system(renderChatCommand)
