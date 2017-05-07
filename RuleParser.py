import json


class RuleParser(object):
    def __init__(self, rule):
        if isinstance(rule, basestring):
            self.rule = json.loads(rule)
        else:
            self.rule = rule
        self.validate(self.rule)

    class Functions(object):
        def __init__(self, log):
            self.log = log

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

        def eq(self, *args):
            return self.log[args[0]] == args[1]

        def neq(self, *args):
            return self.log[args[0]] != args[1]

        def in_(self, *args):
            return self.log[args[0]] in args[1:]

        def gt(self, *args):
            return self.log[args[0]] > args[1]

        def gte(self, *args):
            return self.log[args[0]] >= args[1]

        def lt(self, *args):
            return self.log[args[0]] < args[1]

        def lte(self, *args):
            return self.log[args[0]] <= args[1]

        def not_(self, *args):
            return not self.log[args[0]]

        def or_(self, *args):
            return any(args)

        def and_(self, *args):
            return all(args)

        def int_(self, *args):
            return int(args[0])

        def str_(self, *args):
            return unicode(args[0])

        def upper(self, *args):
            return args[0].upper()

        def lower(self, *args):
            return args[0].lower()

        def plus(self, *args):
            return sum(args)

        def minus(self, *args):
            return args[0] - args[1]

        def multiply(self, *args):
            return args[0] * args[1]

        def divide(self, *args):
            return float(args[0]) / float(args[1])

        def abs(self, *args):
            return abs(args[0])

    def parseList(self, ruleInList):
        queryStr = ''
        for item in ruleInList:
            queryStr += self.pretreat(item, queryStr)
            if item != ruleInList[-1]:
                queryStr += ','
        return queryStr

    def pretreat(self, rule, queryStr = ''):
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


    @staticmethod
    def validate(rule):
        if not isinstance(rule, list):
            raise RuleEvaluationError(
                'Rule must be a list, got {}'.format(type(rule)))
        if len(rule) < 2:
            raise RuleEvaluationError('Must have at least one argument.')

    def _evaluate(self, rule, fns):

        def _recurse_eval(arg):
            if isinstance(arg, list):
                return self._evaluate(arg, fns)
            else:
                return arg

        r = map(_recurse_eval, rule)
        r[0] = self.Functions.ALIAS.get(r[0]) or r[0]
        func = getattr(fns, r[0])
        return func(*r[1:])

    def evaluate(self, log):
        log = json.loads(log)
        fns = self.Functions(log)
        ret = self._evaluate(self.rule, fns)
        if not isinstance(ret, bool):
            print 'In common usage, a rule must return a bool value,' 'but get {}, please check the rule to ensure it is true'
        return ret

if '__main__' == __name__:
    rule = '''
    ["and", 
        ["=", "name", "liuyang"],
        ["<", "age", 4],
        ["or",
            ["=", "count", 1],
            ["=", "count", 2]
        ]
    ]
    '''

    rule_mongo = '''
    { "$and":[
        {"id":{"eq":1}},
        {"name":{"eq":"liuyang"}},
        {"age":{"eq":3}},
        {"$or":[{"count":{"eq":1}}]}
        ]
    }
    '''

    log = '''
    {"name":"liuyang", "age":4, "count":2, "id":1, "count":1}
    '''

    parse = RuleParser(rule)
    rule = parse.pretreat(json.loads(rule_mongo))
    parse = RuleParser(rule)
    print parse.evaluate(log)  