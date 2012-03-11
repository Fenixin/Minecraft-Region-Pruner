=======================
Minecraft Region Pruner
=======================

By Alejandro Aguilera (Fenixin) 

Small script that tries to detect scattered region files in Minecraft
worlds.

This program uses the nbt library by twootlie.

Web page:
https://github.com/Fenixin/Minecraft-Region-Pruner


Supported platforms
===================
This program seems to work with Python 2.7.x, and DOESN'T work with
python 3.x.

How it works
============

It counts the chunks in every region file, then if a region file has
less than '--threshold' chunks the neighbour region files are scanned in
a 3x3 grid centered in this region file. If one of the neighbours has
more than '--threshold' chunks the region file is considered sane,
otherwise the region file goes to the list of bad region files.

This list will be printed at the end of the program. You can delete all
these region files using the '--delete' option.


Warning
=======

This script has been tested in one or two worlds... so, MAKE ABACKUP OF
YOUR WORLD BEFORE RUNNING THIS, I'M NOT RESPONSIBLE OF WHAT HAPPENS TO
YOUR WORLD. Think that you are playing with you precious saved games :P

Good luck! :)
