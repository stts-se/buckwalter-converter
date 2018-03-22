import buckwalter
import sys
import re

cmdname = "test_buckwalter" # sys.argv[0]
do_debug = False

## TODO: Add tests to check for expected fails (non-ascii characters that couldn't be converted)!

def debug(string):
    if do_debug:
        if string == "":
            print("", file=sys.stderr)
        else:
            print("[%s] %s" % (cmdname, string), file=sys.stderr)

def test_single(file_mode, test_mode, test_no, input_orig, input_norm, expect, cfg):
                    
            res = buckwalter.convert(input_orig, cfg)

            #debug("type: " + cfg.type())
            #debug("input_orig: " + input_orig)
            #debug("input_norm: " + input_norm)
            #debug("expect: " + expect)
            #debug("result: " + res.result)

            input_orig_ucode = buckwalter.unicode_list(input_orig)
            input_norm_ucode = buckwalter.unicode_list(input_norm)
            expect_ucode = buckwalter.unicode_list(expect)
            result_ucode = buckwalter.unicode_list(res.result)

            info = "%s #%s | %s\ninput orig\t%s\t%s\ninput norm\t%s\t%s\nexpected\t%s\t%s\nfound    \t%s\t%s\n" % (file_mode, test_no, test_mode, input_orig, input_orig_ucode, input_norm, input_norm_ucode, expect, expect_ucode, res.result, result_ucode)
            
            if res.result == expect:
            #    print("SUCC: " + info, file=sys.stderr)
                return True
            else:                
                print("FAIL: " + info, file=sys.stderr)
                return False


def test_file(input_file, cfg):
    file_mode = cfg.type()
    ar_index = 0
    bw_index = 1
    if cfg.reverse:
        ar_index = 1
        bw_index = 0

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
            
            a0 = fs[ar_index]
            b0 = fs[bw_index]
            a0norm = a0
            b0norm = b0
            if ar_index == 0:
                a0norm = buckwalter.normalise_ar_input(a0norm)
            if bw_index == 0:
                b0norm = buckwalter.normalise_bw_input(b0norm)

            debug("")
            debug("ari %s" % ar_index)
            debug("bwi %s" % bw_index)
            debug("a0 %s" % a0)
            debug("b0 %s" % b0)

            ok1=True
            ok2=True
            if ar_index == 0:                
                ok1=test_single(file_mode, "plain", test_no, a0, a0norm, b0norm, cfg.copy_with_reverse(False))
                ok2=test_single(file_mode, "reverse", test_no, b0, b0norm, a0norm, cfg.copy_with_reverse(True))
            else:
                ok1=test_single(file_mode, "plain", test_no, b0, b0norm, a0norm, cfg.copy_with_reverse(True))
                ok2=test_single(file_mode, "reverse", test_no, a0, a0norm, b0norm, cfg.copy_with_reverse(False))

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
    
quiet = False
            
test_file("test_data/test_a2b.txt", buckwalter.Config(convertNumbers = False, reverse = False, quiet = quiet))
test_file("test_data/test_a2b.txt", buckwalter.Config(convertNumbers = True, reverse = False, quiet = quiet))

test_file("test_data/test_b2a.txt", buckwalter.Config(convertNumbers = False, reverse = True, quiet = quiet))
test_file("test_data/test_b2a.txt", buckwalter.Config(convertNumbers = True, reverse = True, quiet = quiet))
