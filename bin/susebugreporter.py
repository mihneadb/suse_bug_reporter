#!/usr/bin/env python
 
import sys
import argparse
 
def do_aid(args):
    print "do_aid"
    print args.choice

def do_gather(args):
    print "do_gather"
    print args
 
def main():
 
    # creating the parser for the arguments
    parser = argparse.ArgumentParser(description='Bugzilla interactions')
    commands = parser.add_subparsers()
    
    aid = commands.add_parser('aid', help='aid users')
    aid.set_defaults(func=do_aid)
    aid.add_argument('choice', type=int)
    
    gather = commands.add_parser('gather', help='gather')
    gather.set_defaults(func=do_gather)

 
    args = parser.parse_args()
    args.func(args)
 
    #print(args)
 
 
if __name__ == '__main__':
    main()
