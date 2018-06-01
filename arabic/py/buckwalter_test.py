import buckwalter
import sys
import re

cmdname = "test_buckwalter"
do_debug = False

def debug(string):
    if do_debug:
        if string == "":
            print("", file=sys.stderr)
        else:
            print("[%s] DEBUG %s" % (cmdname, string), file=sys.stderr)


def unicode_list(string):
    res = ""
    for ch in string:
        try:
            uc = ('U+%04x' % ord(ch))
            res = res + " " + uc
        except getopt.GetoptError as err:
            print("error for char '%s' : %s" % (ch, err), file=sys.stderr)
            help()
            sys.exit(2)

    return res.rstrip()



def test_single(file_mode, test_no, maptable, input, expect):

    test_mode = maptable.name()
    res = buckwalter.convert(maptable, input)

    input_ucode = unicode_list(input)
    expect_ucode = unicode_list(expect)
    result_ucode = unicode_list(res.result)

    #debug("input  %s" % input)
    #debug("expect %s" % expect)
    #debug("result %s" % res.result)
    #debug("mode   %s"% test_mode)

    info = "%s #%s | %s\ninput   \t%s\t%s\nexpected\t%s\t%s\nfound    \t%s\t%s\n" % (file_mode, test_no, test_mode, input, input_ucode, expect, expect_ucode, res.result, result_ucode)
    
    if res.result == expect:
        #    print("SUCC: " + info, file=sys.stderr)
        return True
    else:                
        print("FAIL: " + info, file=sys.stderr)
        return False

errFmt = "for test no %s, expected '%s', got '%s'"

def test_accept(inp, exp, res, test_no):
    if not res.ok:
        print("didn't expect error for test %s! got %s" % (test_no, "; ".join(res.msgs)), sys.stderr)
        return False
    elif res.result != exp:
        print(errFmt % (test_no, exp, res.result), file=sys.stderr)
        return False
    else:
        return True

def test_fail(inp, exp, res, test_no):
    rz = True
    if res.ok:
        print("expected error for test no %s, input %s!" % (test_no, inp), file=sys.stderr)
        rz = False
    elif res.result != exp:
        print(errFmt % (test_no, exp, res.result), file=sys.stderr)
        rz = False
    return rz
    

def test_strings():    
    n_errs = 0
    n_tests = 0

    n_tests+=1
    inp = "Allh"
    exp = "\u0627\u0644\u0644\u0647"
    res = buckwalter.b2a(inp)
    if not test_accept(inp, exp, res, n_tests):
        n_errs+=1

    n_tests+=1
    inp = "Humu~S"
    exp = "\u062D\u064F\u0645\u064F\u0651\u0635"
    res = buckwalter.b2a(inp)
    if not test_fail(inp, exp, res, n_tests):
        n_errs+=1

    n_tests+=1
    inp = "Hum~uS Allh"
    exp = "\u062D\u064F\u0645\u064F\u0651\u0635 \u0627\u0644\u0644\u0647"
    res = buckwalter.b2a(inp)
    if not test_accept(inp, exp, res, n_tests):
        n_errs+=1


    n_tests+=1
    inp = "Hum~uS"
    exp = "\u062D\u064F\u0645\u064F\u0651\u0635"
    res = buckwalter.b2a(inp)
    if not test_accept(inp, exp, res, n_tests):
        n_errs+=1

    n_tests+=1
    inp = "\u062D\u064F\u0645\u064F\u0651\u0635"
    exp = "Hum~uS"
    res = buckwalter.a2b(inp)
    if not test_accept(inp, exp, res, n_tests):
        n_errs+=1

    n_tests+=1
    inp = "\u062D\u064F\u0645\u0651\u064F\u0635"
    exp = "Hum~uS"
    res = buckwalter.a2b(inp)
    if not test_fail(inp, exp, res, n_tests):
        n_errs+=1

        
    print("test_strings", file=sys.stderr)
    print("%s tests run" % (n_tests), file=sys.stderr)
    print("%s tests ok" % (n_tests-n_errs), file=sys.stderr)
    print("%s tests fail" % (n_errs), file=sys.stderr)
    print("", file=sys.stderr)


def test_file(maptable, input_file):
    file_mode = maptable.name()
    ar_index = 0
    bw_index = 1
    if maptable.fr == "b":
        bw_index = 0
        ar_index = 1

    test_no = 0
    n_errs = 0
    n_tests = 0
    with open(input_file, encoding="utf-8") as f:        
        for l in re.split("\n\n+", f.read()):
            test_no+=1
            l = l.rstrip()
            if l.strip() == "":
                continue
            if l.strip().startswith("#"):
                #print("SKIPPING:\n" + l, file=sys.stderr)
                continue
            fs = list(filter(None, l.split("\n")))

            debug(input_file)
            debug(l)
            
            a0 = fs[ar_index]
            b0 = fs[bw_index]

            #debug("")
            #debug("ari %s" % ar_index)
            #debug("bwi %s" % bw_index)
            #debug("a0 %s" % a0)
            #debug("b0 %s" % b0)

            ok1=True
            ok2=True
            ok1=test_single(file_mode, test_no, buckwalter.a2bMap, a0, b0)
            ok2=test_single(file_mode, test_no, buckwalter.b2aMap, b0, a0)

            n_tests+=2
            if not ok1:
                n_errs+=1
            if not ok2:
                n_errs+=1


    print("input file %s" % (input_file), file=sys.stderr)
    print("%s tests run" % (n_tests), file=sys.stderr)
    print("%s tests ok" % (n_tests-n_errs), file=sys.stderr)
    print("%s tests fail" % (n_errs), file=sys.stderr)
    print("", file=sys.stderr)
    
test_file(buckwalter.a2bMap, "test_data/test_a2b.txt" )
test_file(buckwalter.b2aMap, "test_data/test_b2a.txt")
test_strings()
