# Chessnok_CardRedactor
Card redactor for beautiful CCG game - Chessnok, which you can visit at https://vk.com/nastolkin_store and read the rules there https://disk.yandex.ru/d/Hznxzy_QqGlXrA
Currently it provides only one card face; power, name, and text redacting. You can also adjust different settings in /interface/settings.py
To use the redactor you should download the zip file and unpackage it anywhere
The app starts from opening main.py in project's folder

Insruction for interface:
1. File at the top-left corner currently does nothing
2. You can upload your own image by giving the file path at first line or by browsing it after clicking a nearby button. If your image smaller than 515х703 px, then it will be replaced by default image of bubble Sindzi. Currently only png, jpg, and jpeg files are supported.
3. There are 3 inputs for power, name and text. The length of word and height of whole input are restrained, but it should be enough for not-overwhelming card. Text and name are kinda flexible and should shrink if input is too big, but there are shrink limits. You may adjust these limits, spacing, font and font size at image_redacor/constants.py
4. Little hint: you can press tab and print number to make rectangle followed by the number simulating the card draw symbol :)
5. Loaded image can be moved by arrow keys. The movements is restrained by the fact, that card face should be placed fully inside the image. The speed of scrolling is also can be adjusted at interface/settings.py
6. Lastly, you can save your card by clicking the bottom button and browsing the file for overwrite or creating a new one.
7. The app shutdowns by clicking the cross at the top-right.

Future plans:
1. Adding artist, rarity, type, and flavour text fields to redact. Also king table for kings and coins for coin-depended cards.
2. Official Chessnok font will be mine!
3. Different card faces and dynamic text box, which adjusts to your input height.
4. Specials symbols such as card draws, rotations, coins, etc.
5. Resizing images and maybe rotating them
6. Quick card load from data file
7. Easier ways to change settings
8. Useful top-bar if it'll be ever needed.
9. Cosmetic improvements
