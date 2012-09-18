#chain.py

import inspect
import random
from collections import defaultdict

# functions intended for internal use only

def _identity(value):
    """not very interesting, except used as default everywhere"""
    return value

def _arity(f):
    """how many arguments does f take?"""
    return len(inspect.getargspec(f).args)

def _seq(iterable):
    """want dicts to iterate as key-value pairs, so have to convert"""
    if type(iterable) == dict:
        return iterable.iteritems()
    else:
        return iterable

def _iterator_fn(fn):
    """returns a function of (item,idx,lst) that takes into account _arity of f
    if 0: new function returns f()
    if 1: ... returns f(item)
    if 2: ... returns f(item,idx)
    if 3: ... returns f(item,idx,lst)"""
    num_args = _arity(fn)
    if num_args == 0: return (lambda item,idx,lst: fn())
    elif num_args == 1: return (lambda item,idx,lst: fn(item))
    elif num_args == 2: return (lambda item,idx,lst: fn(item,idx))
    elif num_args == 3: return (lambda item,idx,lst: fn(item,idx,lst))
    else: raise NameError("fn can only take 3 arguments")

def length(lst):
    """for chaining"""
    return len(list(lst))

size = length

def each(lst,fn):
    """call fn on each item in lst, then return lst"""
    iterator_fn = _iterator_fn(fn)
    for idx,item in enumerate(_seq(lst)):
        iterator_fn(item,idx,lst)
    return lst

for_each = each

def map(lst,fn=_identity):
    """call fn on each item in lst, lazy return results"""
    iterator_fn = _iterator_fn(fn)
    for idx,item in enumerate(_seq(lst)):
        yield iterator_fn(item,idx,lst)

def append(lst,lst2):
    for item in lst:
        yield item
    for item in lst2:
        yield item

def reduce(lst,fn,memo):
    """set memo = fn(memo,lst[0]), then fn(memo,lst[1]), and so on ...
    returns final value of memo"""
    for item in _seq(lst):
        memo = fn(memo,item)
    return memo

def reduce_right(lst,fn,memo):
    """setmemo = fn(memo,lst[-1]), then fn(memo,lst[-2]), and so on ...
    returns final value of memo"""
    for item in reversed(_seq(lst)):
        memo = fn(memo,item)
    return memo

def rev(lst):
    """return lst in reverse order"""
    return reversed(_seq(list))

def find(lst,fn=_identity):
    """returns the first item in lst satisfying fn
    raises an error if no item satisfies"""
    iterator_fn = _iterator_fn(fn)
    for idx,item in enumerate(_seq(lst)):
        if iterator_fn(item,idx,lst):
            return item
    raise NameError("unable to find")

def collect(lst,fn=_identity):
    """lazy-return the concatenation of fn(lst[0]), fn(lst[1]), ..."""
    iterator_fn = _iterator_fn(fn)
    for idx,item in enumerate(_seq(lst)):
        for sub_item in iterator_fn(item,idx,lst):
            yield sub_item
    
def filter(lst,fn=_identity):
    """lazy-return the values in lst that satisfy fn"""
    iterator_fn = _iterator_fn(fn)
    for idx,item in enumerate(_seq(lst)):
        if iterator_fn(item,idx,lst):
            yield item

def reject(lst,fn=_identity):
    """lazy-return the values in lst that don't satisfy fn"""
    iterator_fn = _iterator_fn(fn)
    for idx,item in enumerate(_seq(lst)):
        if not iterator_fn(item,idx,lst):
            yield item

def all(lst,fn=_identity):
    """True iff all elements of lst satisfy fn"""
    iterator_fn = _iterator_fn(fn)
    for idx,item in enumerate(_seq(lst)):
        if not iterator_fn(item,idx,lst): return False
    return True

def any(lst,fn=_identity):
    """True iff at least one element of lst satisfies fn"""
    iterator_fn = _iterator_fn(fn)
    for idx,item in enumerate(_seq(lst)):
        if iterator_fn(item,idx,lst): return True
    return False

def sort_by(lst,fn=_identity):
    """returns the elements of lst sorted by fn"""
    value_pairs = [(fn(item),item) for item in _seq(lst)]
    return [z[1] for z in sorted(value_pairs)]

def sort_by_descending(lst,fn=_identity):
    """returns the elements of lst sorted by fn in descending order"""
    value_pairs = [(fn(item),item) for item in _seq(lst)]
    return [z[1] for z in sorted(value_pairs,reverse=True)]


def group_by(lst,fn=_identity):
    """returns a generator of key-value pairs
    where the key is fn applied to each item
    and the value is a list of the corresponding items"""
    iterator_fn = _iterator_fn(fn)
    group_dict = defaultdict(list)
    for idx,item in enumerate(_seq(lst)):
        key = iterator_fn(item,idx,lst)
        group_dict[key].append(item)
    return group_dict.iteritems()

def count_by(lst,fn=_identity):
    """returns a generator of key-value pairs
    where the key is fn applied to each item
    and the value is the number of items corresponding to the key"""
    iterator_fn = _iterator_fn(fn)
    count_dict = defaultdict(int)
    for idx,item in enumerate(_seq(lst)):
        key = iterator_fn(item,idx,lst)
        count_dict[key] += 1
    return count_dict.iteritems()

def distinct_by(lst,fn=_identity):
    """returns a generator where each fn(item) can only appear once"""
    iterator_fn = _iterator_fn(fn)
    seen = set()
    for idx,item in enumerate(_seq(lst)):
        key = iterator_fn(item,idx,lst)
        if not key in seen:
            seen.add(key)
            yield item

distinct = distinct_by

def max(lst,fn=_identity):
    """returns the item in lst for which fn is largest
    in case of a tie, returns the first such item"""
    iterator_fn = _iterator_fn(fn)
    max_value,max_item = None,None
    for idx,item in enumerate(_seq(lst)):
        cur_value = iterator_fn(item,idx,lst)
        if not max_value or cur_value > max_value:
            max_value,max_item = cur_value,item
    return max_item

def min(lst,fn=_identity):
    """returns the item in lst for which fn is smallest
    in case of a tie, returns the first such item"""
    iterator_fn = _iterator_fn(fn)
    min_value,min_item = None,None
    for idx,item in enumerate(_seq(lst)):
        cur_value = iterator_fn(item,idx,lst)
        if not min_value or cur_value < min_value:
            min_value,min_item = cur_value,item
    return min_item  

def sum_by(lst,fn=_identity):
    """returns the sum of fn applied to each item in lst"""
    return sum(map(lst,fn))

sum = sum_by

def shuffle(lst):
    """returns the items in lst in random order"""
    return random.shuffle([item for item in _seq(lst)])

def to_list(lst):
    return list(lst)

def to_dict(kvps):
    return dict(kvps)

# array functions

def first(array,n=1):
    """lazy returns the first n items in array"""
    for idx,item in enumerate(array):
        if idx < n:
            yield item
        else:
            break

take = first

def rest(array,n=1):
    """skips the first n items in array
    lazy returns the rest"""
    for idx,item in enumerate(array):
        if idx >= n:
            yield item

skip = rest

def head(lst):
    if inspect.isgenerator(lst):
        return lst.next()
    else:
        return lst[0]

# chaining

class Chain:
    def __init__(self,obj):
        self.obj = obj
    def __repr__(self):
        return "Chain(%s)" % self.obj.__repr__()
    def value(self,generator_to_list=True):
        if type(self.obj) == dict:
            return self.obj
        elif generator_to_list and (inspect.isgenerator(self.obj) or
                                  type(self.obj) == type({}.iteritems())):
            return list(self.obj)
        else:
            return self.obj
    def __getattr__(self,name):
        def method_missing(*args):
            self.obj = globals()[name](self.obj,*args)
            return self
        return method_missing
