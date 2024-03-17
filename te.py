#!/usr/bin/python

import sys
import os
import re
import argparse
import tomlkit
import pprint




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
        if self.backup:
            save_file="backup"+self.cur+".1"
            try:
                os.rename(self.cur, save_file)
            except (OSError) as e:
                print("cant write file, ", save_file, e)
                return False
        try:
            with open(self.cur, 'w') as f:
                f.write(s)
        except (OSError) as e:
            print("cant write file, ", save_file, e)
            return False
        return True

def ls(s, fio):
    fl=len(s)
    print ("look, a file: ", fio.cur, "its ", fl, "long")
    s+="\n#the end\n"
    return s

def play(s):
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

    return tomlkit.dumps(d)

def bad_delete_trailing_comments(s, fio):
    try:
        d=tomlkit.loads(s)
    except (Exception) as e:
        print("not a good toml file, ", fio.cur)
        return False
    bdy=d._body
    ln=len(bdy)
    cnt=0
    dellist=[]
    for c in range(ln-1,-1,-1 ):
        bdyc=bdy[c]
        c_type=bdy[c][1]
        #DEBUG print (f"{c=} : ", bdyc[0], '=', "t:", type(bdyc[1]) )
        if isinstance(c_type, tomlkit.items.Comment):
            dellist.append(c)
            cnt+=1
            print ("del:", d._body[c])
            continue
        #if isinstance(c_type, tomlkit.items.Whitespace ):
        #    continue
        print (type(c_type))


    print (dellist)
    for c in dellist:
        del d._body[c]

    print ("----- out -------")
    print (tomlkit.dumps(d) )
    print (f"--- removed {cnt} lines -------")

    return False #tomlkit.dumps(d)


def delete_trailing_comments(s, fio):
    slist = s.splitlines()
    ln = len(slist)
    pattern = re.compile('\\s*#')
    newline = 0
    for rline in range(ln-1,-1,-1 ):
        l = slist[rline]
        if not len(l):
            newline+=1
            continue
        if pattern.match(l):  # No match; search doesn't include the "d"
            continue
        break
    out_list = slist[0:rline+1]
    out_list.append('')
    if newline:
        out_list.append('')
    return "\n".join(out_list)

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
            action = 'store',
            help = """What action to take on files
There must always be one action:
    - delete_trailing_comments (dt):
      delete all comments from the button of the file, and up,
      until a non-comment is found
      all whitespace ( whitelines? ) are perserved

    - list (ls):
      test

""",)
            
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
            print ("run: delete_trailing_comments")
            action=delete_trailing_comments
        case 'ls' | 'list':
            print ("run: list")
            action=ls
        case _:
            print ("unknown action")
            return -9
            #return usage(args)


            return ls(args, ls)


    flist=file_io(args)
    for fs in flist:
        r=action(fs, flist)
        print("on file ", flist.cur)
        if r and isinstance(r, str):
            flist.save(r)
    return 0


if __name__ == '__main__':
    sys.exit(main())

