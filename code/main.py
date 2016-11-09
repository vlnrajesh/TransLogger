#!/usr/bin/env python
try:
    import logging
    import os
    import re
    from pprint import pprint
    from TransLogger import TransLogger
except ImportError, err:
    print err

TRANS_OBJECT = {}
MAX_NO_OF_TRANSACTIONS = 0


class LevelFilter(logging.Filter):
    def __init__(self, low, high):
        self._low = low
        self._high = high
        logging.Filter.__init__(self)

    def filter(self, record):
        if self._low <= record.levelno <= self._high:
            return True
        return False


def load_transaction():
    dir_name = os.path.join(os.path.dirname(os.getcwd()), 'trans')
    for file_name in os.listdir(dir_name):
        fp = open(os.path.join(dir_name, file_name), 'r')
        TRANS_OBJECT[file_name] = fp.read().splitlines()
        fp.close()


def read_trans(number_of_transactions):
    if not any(TRANS_OBJECT): load_transaction()
    try:
        for transaction in sorted(TRANS_OBJECT):
            _message = "<START %s>" % transaction
            logging.info(_message)
            logging.debug(_message)
            eval_trans(transaction, TRANS_OBJECT[transaction][0:number_of_transactions])
    except KeyboardInterrupt:
        _message = "<ABORT %s>" %transaction
        logging.info(_message)
        logging.debug(_message)


def eval_trans(transaction_ID, trans_array=[]):
    if not transaction_ID in MEMORY_OBJECT:
        MEMORY_OBJECT[transaction_ID] = {}
    if not transaction_ID in ONDISK_OBJECT:
        ONDISK_OBJECT[transaction_ID] = {}
    trans_logger = TransLogger()
    for each_trans in trans_array:
        (MEMORY_OBJECT[transaction_ID], ONDISK_OBJECT[transaction_ID]) = \
            trans_logger.evaluate\
                (MEMORY_OBJECT[transaction_ID], ONDISK_OBJECT[transaction_ID], each_trans, transaction_ID)


if __name__ == '__main__':
    try:
        load_transaction()
        for _EACH_TRANS in TRANS_OBJECT:
            if len(TRANS_OBJECT[_EACH_TRANS]) > MAX_NO_OF_TRANSACTIONS:
                MAX_NO_OF_TRANSACTIONS = len(TRANS_OBJECT[_EACH_TRANS])

        _number_of_transactions = 1

        logger = logging.getLogger()
        logger.propagate = False
        logger.setLevel(logging.DEBUG)
        _formatter = logging.Formatter \
            ("%(message)s")
        log_location = os.path.join(os.path.dirname(os.getcwd()), 'log')
        if not os.path.exists(log_location): os.makedirs(log_location)
        while _number_of_transactions <= MAX_NO_OF_TRANSACTIONS:
            undo_log_file = "%s/%s.txt_%s" % (log_location, _number_of_transactions, 'undo')
            redo_log_file = "%s/%s.txt_%s" % (log_location, _number_of_transactions, 'redo')
            MEMORY_OBJECT = {}
            ONDISK_OBJECT = {}
            undo_logger = logging.FileHandler(undo_log_file, 'w', encoding=None)
            undo_logger.setLevel(logging.DEBUG)
            undo_logger.addFilter(LevelFilter(10, 10))
            undo_logger.setFormatter(_formatter)
            logger.addHandler(undo_logger)

            redo_logger = logging.FileHandler(redo_log_file, 'w', encoding=None)
            redo_logger.setLevel(logging.INFO)
            redo_logger.addFilter(LevelFilter(20, 20))
            redo_logger.setFormatter(_formatter)
            logger.addHandler(redo_logger)

            read_trans(_number_of_transactions)

            logger.removeHandler(undo_logger)
            logger.removeHandler(redo_logger)
            _number_of_transactions += 1
        print "****END OF PROGRAM"
    except Exception,err:
        print err

    print "********OUTPUT*********"
    print "TRANS_OBJECT"
    pprint(TRANS_OBJECT)
    print "MEMORY_OBJECT"
    pprint(MEMORY_OBJECT)
    print "ONDISK_OBJECT"
    pprint(ONDISK_OBJECT)
