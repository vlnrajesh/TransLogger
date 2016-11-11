try:
    import re
    import pickle
    import logging
    import json
    import os
except Exception, err:
    print err

#TODO: Copy db_elements to global dict
#TODO: Add write to file feature to OUTPUT
class TransLogger:
    def __init__(self):
        pass

    def INPUT(self, X, transaction_ID):
        _data_dir=os.path.join(os.path.dirname(os.getcwd()),'data')
        if not os.path.exists(_data_dir): os.makedirs(_data_dir)
        transaction_file = os.path.join(_data_dir,transaction_ID)
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

    def READ(self, memory_dict, ondisk_dict, args,transaction_ID):
        _db_element = args[0]
        _local_element = args[1]
        if memory_dict[_db_element] is None:
            memory_dict[_db_element] = self.INPUT(_db_element,transaction_ID)
            ondisk_dict[_db_element] = memory_dict[_db_element]
        memory_dict[_local_element] = memory_dict[_db_element]
        return (memory_dict, ondisk_dict)

    def WRITE(self, memory_dict, ondisk_dict, args,transaction_ID,MEMORY_DICT,ONDISK_DICT):
        _db_element = args[0]
        _local_element = args[1]
        if memory_dict[_db_element] is None:
            memory_dict[_db_element] = self.INPUT(_db_element,transaction_ID)
            ondisk_dict[_db_element] = memory_dict[_db_element]
        undo_disk_values=''
        for _each_trans in ONDISK_DICT:
            for _each_key in ONDISK_DICT[_each_trans]:
                undo_disk_values+='%s %s ' %(_each_key,MEMORY_DICT[_each_trans][_each_key])
        undo_message="<%s> %s" %(transaction_ID,undo_disk_values)
        memory_dict[_db_element] = memory_dict[_local_element]
        redo_disk_values = ''
        for _each_trans in ONDISK_DICT:
            for _each_key in ONDISK_DICT[_each_trans]:
                redo_disk_values+='%s %s ' %(_each_key,MEMORY_DICT[_each_trans][_each_key])
        redo_message = "<%s> %s" %(transaction_ID,redo_disk_values)
        logging.debug(undo_message)
        logging.info(redo_message)
        return (memory_dict, ondisk_dict)

    def OUTPUT(self, memory_dict, ondisk_dict, args,transaction_ID,MEMORY_DICT,ONDISK_DICT):
        _db_element=args[0]
        ondisk_dict[_db_element]=memory_dict[_db_element]
        _message="<COMMIT %s>" %(transaction_ID)
        logging.info(_message)
        logging.debug(_message)

        return (memory_dict, ondisk_dict)

    def evaluate(self, memory_dict, ondisk_dict, transaction, transaction_ID, MEMORY_DICT, ONDISK_DICT):
        _func_pattern = r'(\w[\w\d_]*)\((.*)\)$'
        _func_match = re.match(_func_pattern, transaction)
        func_args = []
        if _func_match:
            func_name = _func_match.groups()[0]
            for each_args in re.split('; |, |\*|\n|,', _func_match.groups()[1]):
                if not each_args in memory_dict:
                    memory_dict[each_args] = None
                func_args.append(each_args)
            if func_name == 'READ':
                (memory_dict, ondisk_dict) = self.READ(memory_dict, ondisk_dict, func_args, transaction_ID)
            if func_name == 'WRITE':
                (memory_dict, ondisk_dict) = self.WRITE\
                    (memory_dict, ondisk_dict, func_args, transaction_ID,MEMORY_DICT,ONDISK_DICT)
            if func_name == 'OUTPUT':
                (memory_dict, ondisk_dict) = self.OUTPUT\
                    (memory_dict, ondisk_dict, func_args, transaction_ID,MEMORY_DICT,ONDISK_DICT)
        else:
            transaction = transaction.replace(':=', '=')
            _expr_pattern = r'(\w[\w\d_]*) \= (.*)'
            _expr_match = re.match(_expr_pattern, transaction)
            ns = {}
            for _each_key in memory_dict:
                _code = compile('%s = %s' % (_each_key, memory_dict[_each_key]), '<string>', 'exec')
                exec _code in ns
            if _expr_match:
                _identifier = _expr_match.groups()[0]
                _code = compile('%s' %transaction, '<string>','exec')
                exec _code  in ns
                memory_dict[_identifier] = ns[_identifier]
        return (memory_dict, ondisk_dict)
