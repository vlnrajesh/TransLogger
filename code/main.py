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
MEMORY_OBJECT={}
ONDISK_OBJECT={}
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


def read_trans(MEMORY_OBJECT,ONDISK_OBJECT,number_of_transactions):
    if not any(TRANS_OBJECT): load_transaction()
    try:
        if not 'trans' in TRANS_OBJECT: TRANS_OBJECT['trans']=[]
        TRANS_OBJECT['trans'].append(str(number_of_transactions))
        for transaction_ID in sorted(TRANS_OBJECT):
            _message = "<START %s>" % transaction_ID
            logging.info(_message)
            logging.debug(_message)
            eval_trans\
                (MEMORY_OBJECT, ONDISK_OBJECT,transaction_ID,TRANS_OBJECT[transaction_ID][0:number_of_transactions])
    except KeyboardInterrupt:
        _message = "<ABORT %s>" %transaction_ID
        logging.info(_message)
        logging.debug(_message)
    finally:
        return MEMORY_OBJECT,ONDISK_OBJECT


def eval_trans(MEMORY_OBJECT,ONDISK_OBJECT,transaction_ID,trans_array=[]):
    if not 'in_use' in MEMORY_OBJECT:
        MEMORY_OBJECT['in_use'] = []
    trans_logger = TransLogger()
    for each_transaction in trans_array:
        (MEMORY_OBJECT,ONDISK_OBJECT)=trans_logger.evaluate(MEMORY_OBJECT,ONDISK_OBJECT,transaction_ID,each_transaction)


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
            # MEMORY_OBJECT['trans'].append(_number_of_transactions)
            undo_log_file = "%s/%s.txt_%s" % (log_location, _number_of_transactions, 'undo')
            redo_log_file = "%s/%s.txt_%s" % (log_location, _number_of_transactions, 'redo')
            MEMORY_OBJECT = {}
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

            MEMORY_OBJECT,ONDISK_OBJECT=read_trans(MEMORY_OBJECT,ONDISK_OBJECT,_number_of_transactions)
            logger.removeHandler(undo_logger)
            logger.removeHandler(redo_logger)
            if len(MEMORY_OBJECT['in_use']) == 0:
               correctness_trans='\n'
               correctness_trans+=' '.join(TRANS_OBJECT['trans'])
               with open(undo_log_file,'a') as fp:
                   fp.write(correctness_trans)

            _number_of_transactions += 1
        print "*******END OF PROGRAM******"
   except Exception,err:
       print err
   # print "********OUTPUT*********"
   # print "TRANS_OBJECT"
   # pprint(TRANS_OBJECT)
   # print "MEMORY_OBJECT"
   # pprint(MEMORY_OBJECT)
   # print "ONDISK_OBJECT"
   # pprint(ONDISK_OBJECT)
