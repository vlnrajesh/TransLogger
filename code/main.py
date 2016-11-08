#!/usr/bin/env python
try:
    from logging.handlers import RotatingFileHandler
    import logging
    import os
    import re
    from pprint import pprint
    from TransLogger import TransLogger

except ImportError, err:
    print err

MEMORY_OBJECT = {}
ONDISK_OBJECT = {}
TRANS_OBJECT = {}
MAX_NO_OF_TRANSACTIONS=0

def logger_initilizer(filename):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Console logging
    _handler = logging.StreamHandler()
    _handler.setLevel(logging.INFO)
    _formatter = logging.Formatter \
        ("%(message)s")
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)
    # File logging
    # _handler=logging.FileHandler(filename,'a',encoding=None,delay='true')
    _handler = RotatingFileHandler(filename, 'a', maxBytes=1048576, encoding=None, backupCount=2, delay='true')
    _handler.setLevel(logging.DEBUG)
    _formatter = logging.Formatter \
        ("[%(asctime)s] [%(levelname)-6s] --- %(message)s (%(filename)s:%(lineno)s)", "%d-%m-%Y %H:%M:%S")
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)


def load_transaction():
    dir_name = os.path.join(os.path.dirname(os.getcwd()), 'trans')
    for file_name in os.listdir(dir_name):
        fp = open(os.path.join(dir_name, file_name), 'r')
        TRANS_OBJECT[file_name] = fp.read().splitlines()
        fp.close()


def read_trans(number_of_transactions):
    if not any(TRANS_OBJECT): load_transaction()
    for transaction in sorted(TRANS_OBJECT):
        eval_trans(transaction, TRANS_OBJECT[transaction][0:number_of_transactions])


def eval_trans(transaction_ID, trans_array=[]):
    if not transaction_ID in MEMORY_OBJECT:
        MEMORY_OBJECT[transaction_ID] = {}
    if not transaction_ID in ONDISK_OBJECT:
        ONDISK_OBJECT[transaction_ID]={}
    trans_logger = TransLogger()
    for each_trans in trans_array:
        (MEMORY_OBJECT[transaction_ID],ONDISK_OBJECT[transaction_ID])=\
            trans_logger.evaluate(MEMORY_OBJECT[transaction_ID],ONDISK_OBJECT[transaction_ID],each_trans)


if __name__ == '__main__':
    load_transaction()
    for _EACH_TRANS in TRANS_OBJECT:
        if len(TRANS_OBJECT[_EACH_TRANS]) > MAX_NO_OF_TRANSACTIONS:
            MAX_NO_OF_TRANSACTIONS = len(TRANS_OBJECT[_EACH_TRANS])
    _number_of_transactions=1
    while  _number_of_transactions <= MAX_NO_OF_TRANSACTIONS :
        read_trans(_number_of_transactions)
        _number_of_transactions+=1
    print "TRANS_OBJECT"
    pprint(TRANS_OBJECT)
    print "MEMORY_OBJECT"
    pprint(MEMORY_OBJECT)
    print "ONDISK_OBJECT"
    pprint(ONDISK_OBJECT)
