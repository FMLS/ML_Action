import json
import pymongo


class RuleParser(object):

    def __init__(self, rule, log):
        if isinstance(rule, basestring):
            self.rule = json.loads(rule)
        else:
            self.rule = rule
        self.log = log
        self.validate(self.rule)

    class Functions(object):

        ALIAS = {
            '=': 'eq',
            '!=': 'neq',
            '>': 'gt',
            '>=': 'gte',
            '<': 'lt',
            '<=': 'lte',
            'and': 'and_',
            'in': 'in_',
            'or': 'or_',
            'not': 'not_',
            'str': 'str_',
            'int': 'int_',
            '+': 'plus',
            '-': 'minus',
            '*': 'multiply',
            '/': 'divide'
        }

        def eq(self, left, right):
            return left == right

        def neq(self, left, right):
            return left != right

        def in_(self, left, right):
            return args[0] in right

        def gt(self, *args):
            return args[0] > args[1]

        def gte(self, *args):
            return args[0] >= args[1]

        def lt(self, *args):
            return args[0] < args[1]

        def lte(self, *args):
            return args[0] <= args[1]

        def not_(self, *args):
            return not args[0]

        def or_(self, *args):
            return any(args)

        def and_(self, *args):
            return all(args)

    @staticmethod
    def validate(rule):
        if not isinstance(rule, dict):
            raise RuleEvaluationError('Rule must be a dict, got {}'.format(type(rule)))
        if len(rule) < 1:
            raise RuleEvaluationError('Must have at least one argument.')

    def deal_sample_obj(fns, log, k, v):
        operater = v.items()[0][0]
        right = v.items()[0][1]
        key = k
        left = log[key]
        func = getattr(fns, v.items()[0][0])
        return func(left, right)

    def deal_list(m_list):
        return any(map(deal_sample_obj, m_list))

    def _evaluate(self, rule, fns):

        def _recurse_eval(arg):
            if isinstance(arg[1], list):
                return self._evaluate(arg[1], fns)
            else:
                print arg
                arg = [arg.items()[0], arg.items()[1][0], arg.items()[1][1]]
                print arg
                exit()
                return arg

        r = map(_recurse_eval, rule)
        func = getattr(fns, r.items()[0][1])
        return func(*r[1:])

    def parseList(self, ruleInList):
        queryStr = ''
        for item in ruleInList:
            queryStr += self.parseRule(item, queryStr)
            if item != ruleInList[-1]:
                queryStr += ','
        return queryStr

    def parseRule(self, rule, queryStr):
        for k, v in rule.items():
            if k == '$and':
                queryStr = '["and", %s]' % self.parseList(v) 
            elif k == '$or':
                queryStr = '["or", %s]' % self.parseList(v)
            else:
                if v.items()[0][0] == 'eq':
                    if isinstance(v.items()[0][1], basestring):
                        queryStr = '["=", "%s", "%s"]' % (k, v.items()[0][1]) 
                    else:
                        queryStr = '["=", "%s", %s]' % (k, v.items()[0][1])

        return queryStr 

    def evaluate(self, queryStr):
        fns = self.Functions()
        print self.parseRule(self.rule, '')

        #rule_items = self.rule.items()
        # ret = self._evaluate(rule_items, fns)
        # print rule_items
        # print type(rule_items[0][1][0].items())
        # print rule_items[0][1][0].items()

if '__main__' == __name__:
    mongo_client = pymongo.MongoClient('127.0.0.1', 27017)
    db = mongo_client['hsmp']
    collection = db['test']
    for item in collection.find({"$and":[{"test":{"$eq":"test"}}]}):
        print item

    rule = '''
    { "$and":[
        {"id":{"eq":1}},
        {"name":{"eq":"liuyang"}},
        {"age":{"eq":3}},
        {"$or":[{"count":{"eq":1}}]}
        ]
    }
    '''
    rule_parser = RuleParser(rule, {"id": 1, "name": "liuyang"})
    rule_parser.evaluate('')
