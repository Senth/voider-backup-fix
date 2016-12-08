#!/usr/bin/python3
import argparse

from voider_fix.BackupReplacer import BackupReplacer
from voider_fix.InvalidBackupFinder import InvalidBackupFinder
from voider_fix.LocalResourceIndexer import LocalResourceIndexer

# Arguments
parser = argparse.ArgumentParser(description='Fix backup categories')
parser.add_argument('server_files', help='Files from the server to fix')
parser.add_argument('local_files', help='Local files that have been downloaded with the Voider clinet')
parser.add_argument('-d', '--delete', action='store_true',
                    help="Deletes all backup resources that weren't found. See --move for a safer option")
parser.add_argument('-m', '--move', action='store_true',
                    help="Moves files into NOT_FOUND directory that weren't found. Safer than --delete")
args = parser.parse_args()

# Find backups
backupFinder = InvalidBackupFinder(args.server_files)
backupFiles = backupFinder.findAll()
localResourceIndexer = LocalResourceIndexer(args.local_files)
localResourceIndexer.index()
resources = localResourceIndexer.resources

backupReplacer = BackupReplacer(backupFiles, resources)
if args.move:
    backupReplacer.set_move(args.server_files)
elif args.delete:
    backupReplacer.set_delete()
backupReplacer.replace()