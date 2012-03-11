#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#   Region Pruner.
#   Prune your minecraft world of scattered chunks.
#   Copyright (C) 2011  Alejandro Aguilera (Fenixin)
#   https://github.com/Fenixin/Minecraft-Region-Pruner
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from nbt import region
import sys
from os.path import join, exists, split
from os import remove
from optparse import OptionParser
from glob import glob

def main():
    
    usage = 'usage: %prog [options] <world-path>'
    epilog = 'Copyright (C) 2011  Alejandro Aguilera (Fenixin) \
    This program comes with ABSOLUTELY NO WARRANTY; for details see COPYING.txt. This is free software, and you are welcome to redistribute it under certain conditions; see COPYING.txt for details.'

    parser = OptionParser(description='Small script to check for scattered chunks in Minecraft worlds.\
                                            Author: Alejandro Aguilera (Fenixin).',\
    prog = 'region-pruner', version='0.0.1', usage=usage, epilog=epilog)

    parser.add_option('--threshold', '-t', type=int, dest = 'threshold', help = 'If a region file has less than this number of chunks it will be checked for disconnection.', default = 20)
    parser.add_option('--delete', '-d', action = 'store_true', dest = 'delete', help = 'Delete all the very unconnected region-files. Use it with care!', default = False)
    parser.add_option('--only-list', '-l', action = 'store_true', dest = 'only_list', help = 'Only prints the list of disconnected region files', default = False)

    # Options and chcks
    (options, args) = parser.parse_args()

    if not args:
        parser.error("No world path specified! Use --help for a complete list of options.")
        sys.exit(1)
    elif len(args) > 1:
        parser.error("Only one world dirctory needed!")
        sys.exit(1)

    world_path = args[0]
    if not exists(world_path):
        parser.error("The world path doesn't exists!")
        sys.exit(1)
    
    # List of mca files per dimension
    normal_mca_files = glob(join(world_path, "region/r.*.*.mca"))
    nether_mca_files = glob(join(world_path,"DIM-1/region/r.*.*.mca"))
    aether_mca_files = glob(join(world_path,"DIM1/region/r.*.*.mca"))

    if not options.only_list:
        print "Welcome to Region Pruner!"
        print "Scanning world..."

    # for now only scan the overworld
    good_list = []
    bad_list = []
    threshold = options.threshold
    counter = 0
    total = len(normal_mca_files)
    for name in normal_mca_files:
        # some feedback
        reg = region.RegionFile(name)
        if reg.chunk_count > threshold:
            good_list.append(name)
        else:
            # check for good neighbours in a 3x3 grid centered in this
            # region file, if one found this region is a good one
            x, z = get_region_coords(name)
            has_neighbour = False
            for i in range(-1,2,1):
                for j in range(-1,2,1):
                    if i == 0 and j == 0:
                        continue
                    n = get_region_name(world_path, x + i, z + j)
                    if n in good_list:
                        break
                    elif exists(n):
                        nreg = region.RegionFile(n)
                        if nreg.chunk_count > threshold:
                            has_neighbour = True
                            break
                if has_neighbour:
                    break
            if not has_neighbour:
                bad_list.append(name)

        counter += 1
        if not options.only_list:
            if counter % 20 == 0 or counter == total:
                print "Scanned {0} of {1} region files".format(counter, total)


    if not options.only_list:
        print "... scan finished!"
        print "There are {0} disconnected region files of a total of {1}:\n".format(len(bad_list), total)
    for f in bad_list:
        print f
    
    if options.delete:
        if not options.only_list:
            print "Deleting disconnected region files."
        for r in bad_list:
            remove(r)


def get_region_coords(name):
    f = split(name)[-1]
    f = f.split(".")
    x = f[1]
    z = f[2]
    return int(x),int(z)

def get_region_name(world_path, x, z):
    return join(world_path, "region/r." + str(x) + "." + str(z) + ".mca")

if __name__ == '__main__':
    main()
