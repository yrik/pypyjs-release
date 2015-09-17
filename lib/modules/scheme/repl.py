from Queue import Empty
from scheme import debug


__author__ = 'perkins'

from scheme.parser import Parser
import scheme.processer


processer = scheme.processer.processer
import sys, time


def repl(f=sys.stdin, prompt='schemepy> ', of=sys.stdout):
    global parser
    parser = Parser(f)
    last_break=time.time()
    while True:
        ast=None
        if of:
            of.write(prompt)
        try:
            ast = parser.ast
        except Exception as e:
            print e
            continue
        while not ast:
            yield parser.pause_object
            try:
                ast = parser.ast
            except Exception as e:
                print e
                continue
        try:
            dp = processer.doProcess(ast)
            r = dp.next()
            while r is processer.pause_object:
                if time.time() - last_break > 1:
                    last_break=time.time()
                    yield r
                r=dp.next()
        except Empty as e:
            # noinspection PyUnresolvedReferences
            if hasattr(e, 'ret'):
                r = e.ret
            else:
                import traceback
                traceback.print_exc()
                raise e
        except Exception as e:
            if debug.DEBUG:
                import traceback
                print traceback.format_exc()
                print processer.ast
                print processer.children[-1].ast
                print scheme.processer.current_processer.ast
            r = e
        if r is not None and of:
            print >> of, r
