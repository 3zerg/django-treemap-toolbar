""" Profiling code taken from https://gist.github.com/1229681
        Build another version of this for use with SQL queries?

        Extend it so you have a full table showing the stacktrace, then when
        you select a node it hightlights the item. The table could contain
        local vars etc.
"""
from django.conf import settings
from debug_toolbar.panels import DebugPanel
import cProfile
import pstats
from cStringIO import StringIO


class TreemapDebugPanel(DebugPanel):
    name = 'Treemap'
    template = 'panels/treemap.html'
    has_content = True

    def __init__(self, *args, **kwargs):
        super(TreemapDebugPanel, self).__init__(*args, **kwargs)

    def nav_title(self):
        return 'Profile Treemap'

    def url(self):
        return ''

    def title(self):
        return self.nav_title()

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.profiler = cProfile.Profile()
        args = (request, ) + view_args
        return self.profiler.runcall(view_func, *args, **view_kwargs)

    def process_response(self, request, response):
        """ Takes the data collected by the profile and parses it in to a
            string suitable for displaying in a Google Treemap Visualization.

            The data can be displayed in a flat format by setting the
            parent attribute (second column) of the data to entry.caller
            (commented out below as an example).
        """
        self.profiler.create_stats()
        stats = pstats.Stats(self.profiler)
        entries = parse_calls(stats)
        stats_string = ['["Parent",null,0,0],']
        for entry in entries:
            #stats_string.append('["%s:%s","Parent",%f,%s],' % ( # Flat
            stats_string.append('["%s:%s","%s",%f,%s],' % ( # Hierarchial
                            entry.code.co_filename,
                            entry.code.co_name,
                            entry.caller,
                            entry.totaltime,
                            entry.callcount))
        self.record_stats({
            'data': '\n'.join(stats_string) ,
        })


class Code(object):
    pass

class Entry(object):
    pass


def parse_calls(data):
    """Helper to convert serialized pstats back to a list of raw entries

        Converse opperation of cProfile.Profile.snapshot_stats()
    
        Slightly modified version of :
        https://bitbucket.org/ogrisel/pyprof2calltree/src/68edcd9f02e4/pyprof2calltree.py
    """
    entries = dict()
    allcallers = dict()

    # first pass over stats to build the list of entry instances
    for code_info, call_info in data.stats.items():
        # build a fake code object
        code = Code()
        code.co_filename, code.co_firstlineno, code.co_name = code_info

        # build a fake entry object
        cc, nc, tt, ct, callers = call_info
        entry = Entry()
        entry.code = code
        entry.callcount = cc
        entry.reccallcount = nc - cc
        entry.inlinetime = tt
        entry.totaltime = ct

        # to be filled during the second pass over stats
        entry.calls = list()
        entry.caller = 'Parent' # set this in case there is no caller

        # collect the new entry
        entries[code_info] = entry
        allcallers[code_info] = callers.items()

    # second pass of stats to plug callees into callers
    for entry in entries.itervalues():
        entry_label = cProfile.label(entry.code)
        entry_callers = allcallers.get(entry_label, [])
        for entry_caller, call_info in entry_callers:
            # The caller attribute is used by the treemap to refer to the
            # 'parent' caller.
            entries[entry_label].caller = '%s:%s' % (entry_caller[0],
                                                     entry_caller[2])
            entries[entry_caller].calls.append((entry, call_info))

    return entries.values()
