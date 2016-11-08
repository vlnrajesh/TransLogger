try:
    import re
    import pickle
except Exception, err:
    print err


class TransLogger:
    def __init__(self):
        pass

    def INPUT(self, X):
        return raw_input('Enter Value  for %s: ' % X)

    def READ(self, memory_dict, ondisk_dict, args):
        _db_element = args[0]
        _local_element = args[1]
        if memory_dict[_db_element] is None:
            memory_dict[_db_element] = self.INPUT(_db_element)
            ondisk_dict[_db_element] = memory_dict[_db_element]
        memory_dict[_local_element] = memory_dict[_db_element]
        return (memory_dict, ondisk_dict)

    def WRITE(self, memory_dict, ondisk_dict, args):
        _db_element = args[0]
        _local_element = args[1]
        if memory_dict[_db_element] is None:
            memory_dict[_db_element] = self.INPUT(_db_element)
            ondisk_dict[_db_element] = memory_dict[_db_element]
        memory_dict[_db_element] = memory_dict[_local_element]
        return (memory_dict, ondisk_dict)

    def OUTPUT(self, memory_dict, ondisk_dict, args):
        _db_element=args[0]
        ondisk_dict[_db_element]=memory_dict[_db_element]
        return (memory_dict, ondisk_dict)

    def evaluate(self, MEMORY_DICT, ONDISK_DICT, transaction):
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
                (MEMORY_DICT, ONDISK_DICT) = self.READ(MEMORY_DICT, ONDISK_DICT, func_args)
            if func_name == 'WRITE':
                (MEMORY_DICT, ONDISK_DICT) = self.WRITE(MEMORY_DICT, ONDISK_DICT, func_args)
            if func_name == 'OUTPUT':
                (MEMORY_DICT, ONDISK_DICT) = self.OUTPUT(MEMORY_DICT, ONDISK_DICT, func_args)
        else:
            transaction = transaction.replace(':=', '=')
            _expr_pattern = r'(\w[\w\d_]*) \= (.*)'
            _expr_match = re.match(_expr_pattern, transaction)
            for _each_key in MEMORY_DICT:
                exec ('%s = %s' % (_each_key,int(MEMORY_DICT[_each_key])))
            if _expr_match:
                _identifier = _expr_match.groups()[0]
                exec ("%s" % (transaction), globals(), locals())
                MEMORY_DICT[_identifier] = locals()[_identifier]
        return (MEMORY_DICT, ONDISK_DICT)
