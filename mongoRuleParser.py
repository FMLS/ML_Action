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
        if len(rule) < 2:
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

    def evaluate(self):
        fns = self.Functions()
        for k, v in self.rule.items():
            if isinstance(v, list) and k == '$or':
                pass
            else:
                self.deal_sample_obj(fns, self.log, k, v)

if '__main__' == __name__:
    # mongo_client = pymongo.MongoClient('127.0.0.1', 27017)
    # db = mongo_client['hsmp']
    # collection = db['log_host_process']
    # for item in collection.find({"uid": {"$gt": 1}}):
    #     print item

    rule = '''
    {
        "id":{"eq":1},
        "name":{"eq":"liuyang"}
    }
    '''
    print rule
    rule_parser = RuleParser(rule, {"id": 1, "name": "liuyang"})
    print rule_parser.evaluate()
