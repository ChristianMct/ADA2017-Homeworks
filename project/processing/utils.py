import sys
import os
import multiprocessing as mp


def process_file_by_line(file_in, file_out, processing_func, limit=None):
    lines = file_in.readlines()
    if limit and limit > 0:
        lines = lines[:limit]

    line_c = len(lines)
    thread_c = mp.cpu_count()
    pool = mp.Pool(thread_c)
    data = pool.imap_unordered(processing_func, lines)
    for i, processed_line in enumerate(data, 1):
        sys.stdout.write('\rProcessing %i pages using %i threads... (%i %%)' % (line_c, thread_c, (i/line_c)*100))
        if processed_line:
            file_out.write(processed_line+os.linesep)
    sys.stdout.write('\n')
