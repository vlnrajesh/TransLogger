try:
    import re
    import pickle
    import logging
    import json
    import os
except Exception, err:
    print err

class TransLogger:
    def __init__(self):
        pass

    def INPUT(self, X, transaction_ID):
        _data_dir=os.path.join(os.path.dirname(os.getcwd()),'data')
        if not os.path.exists(_data_dir): os.makedirs(_data_dir)
        transaction_file = os.path.join(_data_dir,'data')
        ondisk_dict = {}
        try:
            with open(transaction_file) as fd:
                ondisk_dict=json.load(fd)
            if not X in ondisk_dict:
                ondisk_dict[X]=raw_input("Enter Value for %s of %s: " %(X,transaction_ID))
        except IOError:
            ondisk_dict[X]=raw_input("Enter Value for %s of %s: " %(X,transaction_ID))
        except KeyboardInterrupt:
            _message = "<ABORT %s>" % transaction_ID
            logging.info(_message)
            logging.debug(_message)
        finally:
            json.dump(ondisk_dict,open(transaction_file,'w'))
            return ondisk_dict[X]

    def READ(self, MEMORY_DICT,ONDISK_DICT,transaction_ID, args):
        _db_element = args[0]
        _local_element = args[1]
        if MEMORY_DICT[_db_element] is None:
            MEMORY_DICT[_db_element] = self.INPUT(_db_element, transaction_ID)
            ONDISK_DICT[_db_element] = MEMORY_DICT[_db_element]
        MEMORY_DICT[_local_element] = MEMORY_DICT[_db_element]
        if _db_element not in MEMORY_DICT['in_use']: MEMORY_DICT['in_use'].extend(_db_element)

        return MEMORY_DICT, ONDISK_DICT

    def WRITE(self, MEMORY_DICT,ONDISK_DICT,transaction_ID, args):
        _db_element = args[0]
        _local_element = args[1]
        if MEMORY_DICT[_db_element] is None:
            MEMORY_DICT[_db_element] = self.INPUT(_db_element,transaction_ID)
            ONDISK_DICT[_db_element] = MEMORY_DICT[_db_element]
        if _db_element in MEMORY_DICT['in_use']:
            MEMORY_DICT['in_use'].remove(_db_element)
        undo_disk_values=''
        for _each_key in ONDISK_DICT:
                if _each_key in MEMORY_DICT: undo_disk_values +='%s %s ' %(_each_key,MEMORY_DICT[_each_key])
        undo_message="<%s> %s" %(transaction_ID,undo_disk_values)
        MEMORY_DICT[_db_element] = MEMORY_DICT[_local_element]
        redo_disk_values = ''
        for _each_key in ONDISK_DICT:
            if _each_key in MEMORY_DICT: redo_disk_values+='%s %s ' %(_each_key,MEMORY_DICT[_each_key])
        redo_message = "<%s> %s" %(transaction_ID,redo_disk_values)
        logging.debug(undo_message)
        logging.info(redo_message)

        return MEMORY_DICT,ONDISK_DICT

    def OUTPUT(self, MEMORY_DICT,ONDISK_DICT,transaction_ID, args):
        _db_element=args[0]
        ONDISK_DICT[_db_element]=MEMORY_DICT[_db_element]
        _message="<COMMIT %s>" %(transaction_ID)
        logging.info(_message)
        logging.debug(_message)
        #
        # Intentally commented to qualify for Assignment
        #
        #_data_dir = os.path.join(os.path.dirname(os.getcwd()), 'data')
        # if not os.path.exists(_data_dir): os.makedirs(_data_dir)
        # transaction_file = os.path.join(_data_dir, 'data')
        # json.dump(ONDISK_DICT,open(transaction_file,'w'))
        return MEMORY_DICT,ONDISK_DICT

    def evaluate(self,MEMORY_DICT, ONDISK_DICT,transaction_ID, transaction):
        _func_pattern = r'(\w[\w\d_]*)\((.*)\)$'
        _func_match = re.match(_func_pattern, transaction)
        func_args = []
        if _func_match:
            func_name = _func_match.groups()[0]
            for each_args in re.split('; |, |\*|\n|,', _func_match.groups()[1]):
                if not each_args in MEMORY_DICT:
                    MEMORY_DICT[each_args] = None
                func_args.append(each_args)
            if func_name == 'READ':
                (MEMORY_DICT, ONDISK_DICT) = self.READ(MEMORY_DICT, ONDISK_DICT, transaction_ID, func_args)
            if func_name == 'WRITE':
                (MEMORY_DICT, ONDISK_DICT) = self.WRITE(MEMORY_DICT, ONDISK_DICT, transaction_ID, func_args)
            if func_name == 'OUTPUT':
                (MEMORY_DICT,ONDISK_DICT) = self.OUTPUT(MEMORY_DICT, ONDISK_DICT, transaction_ID, func_args)
        else:
            transaction = transaction.replace(':=', '=')
            _expr_pattern = r'(\w[\w\d_]*) \= (.*)'
            _expr_match = re.match(_expr_pattern, transaction)
            ns = {}
            for _each_key in MEMORY_DICT:
                _code = compile('%s = %s' % (_each_key, MEMORY_DICT[_each_key]), '<string>', 'exec')
                exec _code in ns
            if _expr_match:
                _identifier = _expr_match.groups()[0]
                _code = compile('%s' %transaction, '<string>','exec')
                exec _code  in ns
                MEMORY_DICT[_identifier] = ns[_identifier]

        return MEMORY_DICT,ONDISK_DICT
