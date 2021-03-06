import os
import sys
_PATH_ = os.path.dirname(os.path.dirname(__file__))

if _PATH_ not in sys.path:
    sys.path.append(_PATH_)

import argh

from utils.load_data_sets import *


# Credit: Brain Lee

# this method doesn't read .sgf recursively from a folder to subfolder
# make sure dataset looks like this:
# --|-folder1/.sgfs
#   |-folder2/.sgfs
#   ...
#   |-folderN/.sgfs
def preprocess(*data_sets, processed_dir="processed_data"):
    processed_dir = os.path.join(os.getcwd(), processed_dir)
    if not os.path.isdir(processed_dir):
        os.mkdir(processed_dir)
        
    test_chunk, training_chunks = parse_data_sets(*data_sets)
    print("Allocating %s positions as test; remainder as training" % len(test_chunk), file=sys.stderr)

    print("Writing test chunk")
    test_dataset = DataSet.from_positions_w_context(test_chunk, is_test=True)
    test_filename = os.path.join(processed_dir, "test.chunk.gz")
    test_dataset.write(test_filename)
    test_dataset = None

    training_datasets = map(DataSet.from_positions_w_context, training_chunks)
    for i, train_dataset in enumerate(training_datasets):
        if i % 10 == 0:
            print("Writing training chunk %s" % i)
        train_filename = os.path.join(processed_dir, "train%s.chunk.gz" % i)
        train_dataset.write(train_filename)
    print("%s chunks written" % (i+1))


if __name__=="__main__":

    p = argh.ArghParser()
    p.add_commands([preprocess])
    p.dispatch()
