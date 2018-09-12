# coding: utf-8

import sys
import os
import os.path
import shutil
from distutils.dir_util import copy_tree
from optparse import OptionParser

PROGRAM_VERSION = 1.0
PROGRAM_DATE    = '2018-07-19'
PROGRAM_UPDATE  = '2018-07-19'

# Default log level
LOG_LEVEL = 1

# Output files
REQ_2_SRC_CSV_FILE  = "req_2_src.csv"
SRC_2_REQ_CSV_FILE  = "src_2_req.csv"
ORPHAN_SRC_CSV_FILE = "src_wo_req.csv"

# Just show log message on STDERR, if log level is enough
def log(level, message):

    if LOG_LEVEL >= level:
        sys.stderr.write(message + '\n')
        sys.stderr.flush()

def work_on_dirs(input_path, output_path):

    log(1, "\nWorking on directories...\n")

    for dirname, dirnames, filenames in os.walk(input_path):
        for dir_name in dirnames:
            input_dir = os.path.join(dirname, dir_name)
            if " - " not in dir_name:
                artist = dir_name
                album  = ""
            else:
                artist = dir_name.split(" - ")[0].strip()
                album  = ' - '.join(dir_name.split(" - ")[1:]).strip()
            for letter in artist:
                if letter.isalpha():
                    letter_dir = os.path.join(output_path, letter.upper())
                    if not os.path.isdir(letter_dir):
                        os.makedirs(letter_dir)
                    break;
            artist_dir = os.path.join(letter_dir, artist)
            if not album:
                output_dir = artist_dir
            else:
                if not os.path.isdir(artist_dir):
                    os.makedirs(artist_dir)
                output_dir = os.path.join(artist_dir, album)
            copy_tree(input_dir, output_dir)
            log(1, "> Done " + input_dir + " > " + output_dir)

    return 0

def work_on_files(input_path, output_path):

    log(1, "\nWorking on files...\n")

    for dirname, dirnames, filenames in os.walk(input_path):
        for filename in filenames:
            input_file = os.path.join(dirname, filename)
            for letter in filename:
                if letter.isalpha():
                    letter_dir = os.path.join(output_path, letter.upper())
                    if not os.path.isdir(letter_dir):
                        os.makedirs(letter_dir)
                    break;
            shutil.copy2(input_file, letter_dir)
            log(1, "> Done " + filename + " > " + letter_dir)
    return 0

def main(argv=None):

    global LOG_LEVEL

    program_name           = os.path.basename(sys.argv[0])
    program_version        = "v%1.1f" % PROGRAM_VERSION
    program_build_date     = "%s" % PROGRAM_UPDATE
    program_version_string = "%%prog %s (%s)" % (program_version, program_build_date)
    program_usage          = "usage: %prog [-h] [--verbose=INT] --src-dir=STRING --dst-dir=STRING"
    program_long_desc      = "Sort MP3s directories"

    # Setup options
    if argv is None:
        argv = sys.argv[1:]

    try:
        # Setup options parser
        parser = OptionParser(usage=program_usage,
                              version=program_version_string,
                              epilog=program_long_desc)
        parser.add_option("-v",
                          "--verbose",
                          action="store",
                          dest="verbose",
                          help="set verbose level [default: %default]",
                          metavar="INT")
        parser.add_option("-s",
                          "--src-dir",
                          action="store",
                          dest="src_dir",
                          help="input directory to be scanned",
                          metavar="STRING")
        parser.add_option("-d",
                          "--dst-dir",
                          action="store",
                          dest="dst_dir",
                          help="output directory",
                          metavar="STRING")
        parser.add_option("-i",
                          "--work-on-dirs",
                          action="store_true",
                          dest="work_on_dirs",
                          help="work on directories")
        parser.add_option("-f",
                          "--work-on-files",
                          action="store_true",
                          dest="work_on_files",
                          help="work on files")

        # Set defaults
        parser.set_defaults(verbose=str(LOG_LEVEL))

        # Process options
        (opts, args) = parser.parse_args(argv)

        LOG_LEVEL = int(opts.verbose)

        # Check some of the options
        if not opts.src_dir:
            log(0, "ERROR: missing input directory path. Try --help")
            return 1

        if not opts.dst_dir:
            log(0, "ERROR: missing output directory path. Try --help")
            return 1

        if not os.path.isdir(opts.src_dir):
            log(0, "ERROR: " + opts.src_dir + " directory not found")
            return 1

        if not os.path.isdir(opts.dst_dir):
            log(0, "ERROR: " + opts.dst_dir + " directory not found")
            return 1

        if not opts.work_on_dirs and not opts.work_on_files:
            log(0, "ERROR: missing --work-on-dirs or --work-on-files")
            return 1            

        if opts.work_on_dirs and opts.work_on_files:
            log(0, "ERROR: --work-on-dirs and --work-on-files not allowed together")
            return 1            

    except Exception as error:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(error) + "\n")
        sys.stderr.write(indent + " for help use --help\n")
        return 1

    log(0, "\n" + program_name + " starting...")

    log(2, "\nVerbosity level = %s" % opts.verbose)

    status = 0

    if opts.work_on_dirs:
        status = work_on_dirs(opts.src_dir, opts.dst_dir)
        if status != 0:
            return status

    if opts.work_on_files:
        status = work_on_files(opts.src_dir, opts.dst_dir)
        if status != 0:
            return status

    log(0, "\n" + program_name + " done!")

    return 0

# This module runs in main mode
if __name__ == "__main__":
    sys.exit(main())
