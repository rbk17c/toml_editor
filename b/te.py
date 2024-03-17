#!/usr/bin/python

import sys
import argparse
import tomlkit
import pprint






def delete_trailing_comments(s):
    with open('test.toml') as f:
        d=tomlkit.load(f)

    d.add('new', "raw-holger")


    d['subs'].add('new', "sub-holger")




    tab=tomlkit.table()
    tab.add('new', "bulb-holger")

    s=d.pop('subs')

    d['bubs']=tab


    #print ("ts:", s.values(), type(s))
    #s0=s.get('Subs_a')
    #print ("s0:", s0, type(s0))
    #s.add(tomlkit.comment("new comment-----"))

    #s.add("val123", "1234")

    #print ("ts:", s, type(s))

    #for i in s:
    #    print ("s:", i, tomlkit.items.StringType(s))

    #d['subs']=s


    bdy=d._body
    ln=len(bdy)
    print (f"{ln=}")

    for c in range(ln-1,-1,-1 ):
        bdyc=bdy[c]
        print (f"{c=} : ", bdyc[0], '=', "t:", type(bdyc[1]) )
        if isinstance(bdyc[1], tomlkit.items.Comment):
            del d._body[c]
            print ( 'deleted' )
        else:
            print ( 'keep', bdyc[1] )


     

    print ("----- out -------")
    print (tomlkit.dumps(d) )

    #with open('out.toml', 'w') as f:
    #    tomlkit.dump(d, f)

    return tomlkit.dumps(d)

    #parser.add_argument(
    #        '--log', default=sys.stdout, type=argparse.FileType('w'),
            #help='the file where the sum should be written')


class file_io:
    def __init__(self, args):
        self.args=args;
        self.backup=args.backup
        self.cur=None
    def __iter__(self):
        for file_name in self.args.files:
            self.cur=file_name
            try:
                with open (file_name, 'r') as f:
                    yield f.read()
            except (OSError) as e:
                print("cant read file, ", file_name, e)
                
    def save(self, s):
        #if self.backup:
        save_file=self.cur+".1"
        try:
            with open(save_file) as f:
                s.write(s)
        except (OSError) as e:
            print("cant write file, ", save_file, e)
        

def ls(s, fio):
    fl=len(s)
    print ("look, a file: ", fio.cur, "its ", fl, "long")
    return False
    
def main():
    parser = argparse.ArgumentParser(description='toml mass editor')
    parser.add_argument("-v", "--verbose",
        help="increase output verbosity",
        action="store_true")

    parser.add_argument( "-b", "--backup",
            required = False,
            help = 'create a backup, before overwriting file',
            action = 'store_true')

    parser.add_argument( "--action",
            required = False,
            help = """What action to take on files
There must always be one action:
    - delete_trailing_comments (dt):
      delete all comments from the button of the file, and up,
      until a non-comment is found
      all whitespace ( whitelines? ) are perserved

    - list (ls):
      test

""",
            action = 'store')
            
    parser.add_argument( "files",
            help = 'what files to change',
            nargs = '+',
            action = 'store')

    args = parser.parse_args()

    if not args.action:
        args.action=args.files.pop(0)

    if not len(args.files):
        print("nothing to do")
        return -13

    match args.action:
        case 'dt' | 'delete_trailing_comments':
            print ("uuh. yes, lets delete random stuff...")
            action=delete_trailing_comments
        case 'ls' | 'list':
            action=ls
        case _:
            print ("unknown action")
            return -9
            #return usage(args)


            return ls(args, ls)


    flist=file_io(args)
    for fs in flist:
        r=action(fs, flist)
        if r and isinstance(r, str):
            flist.save(r)
    return 0


if __name__ == '__main__':
    sys.exit(main())

