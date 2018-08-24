
Written by Sebastien M. Popoff
[ref=https://github.com/wavefrontshaping/papiview][u][b][color=#70a3c9]github.com/wavefrontshaping.net/papiview[/color][/b][/u][/ref].

Papiview is a frontend for [b]Papis[/b], more information here: [ref=https://github.com/papis/papis][u][b][color=#70a3c9]github.com/papis/papis[/color][/b][/u][/ref].
It requires the library to look for to be accessible via [b]webdav[/b] or [b]sftp[/b].

[b]Toolbar buttons usage[/b]
- [b][color=#70a3c9]Erase button[/color][/b]: Clears the cache, i.e. empty the local database.
- [b][color=#70a3c9]Update button[/color][/b]: Donwloads the information files from the remote library and copy it to the cache folder. 
The document files (mainly pdfs) are not donwloaded. Click on the file name in the detail page of an article to download it and open it.
- [b][color=#70a3c9]Offline download[/color][/b]: Downloads [b]ALL[/b] the files of the remote library for offline use.

[b]Ownclaoud connection[/b]
To connect to a remote library located on an Owncloud server, the webdav configuration shoud look like:
- [b][color=#70a3c9]Host: [/color][/b] test.com
- [b][color=#70a3c9]Remote path: [/color][/b]remote.php/webdav/Biblio_folder/library_folder

