chain-py

Fluent sequence operations in Python

========

*chain-py* is a Python library that allows you to fluently chain together sequence operations.  It is heavily inspired by the `chain` functionality in [underscore.js](http://underscorejs.org/), and also by the [Seq module](http://msdn.microsoft.com/en-us/library/ee353635.aspx) in F#.  (Before building this I found the similar [Moka](http://www.phzbox.com/moka/index.html), which didn't really do what I needed, hence chain)

To use chain, you wrap a collection in a `Chain()` object, call sequence operations on it, and end with a call to `value()`.  It is helpful to wrap the entire call in parentheses so you can abuse whitespace.

# Examples

Imagine the following dataset representing an unpopular blog:

    Post = namedtuple("Post","subject num_comments tags")
    blog = [ Post("First post!",               0,  ["blogging","about me"]),
             Post("Why is no one commenting?", 1,  ["blogging","gripes","complaints"]),
             Post("Hello?",                    0,  ["blogging","hello"]),
             Post("I quit!",                   10, ["not blogging","goodbye"]) ]

Start with

    from chain import Chain
             
Then you can count the number of posts with no comments with

    (Chain(blog)
        .filter(lambda post: post.num_comments == 0)
        .length()
        .value())
        
Of course you could do this easily with list comprehensions:

    len([post for post in blog if post.num_comments == 0])
    
But the fluent way is (for me) easier to read.  And it allows much more complicated operations.  For instance, you could compute a histogram of comment counts for posts tagged "blogging":

    (Chain(blog)
        .filter(lambda post: "blogging" in post.tags)
        .count_by(lambda post: post.num_comments)
        .value())
        
Or the total number of comments per tag:

    (Chain(blog)
        .collect(lambda post: [(tag, post.num_comments) for tag in post.tags])
        .group_by(lambda (tag, num_comments): tag)
        .map(lambda (tag,pairs): (tag,sum([num_comments for t,num_comments in pairs])))
        .value())
        
Internally, `dict`s are always treated as sequences of key-value pairs.  However, you can return a dictionary by calling `to_dict()` right before `value()`:        

    (Chain(blog)
        .collect(lambda post: [(tag, post.num_comments) for tag in post.tags])
        .group_by(lambda (tag, num_comments): tag)
        .map(lambda (tag,pairs): (tag,sum([num_comments for t,num_comments in pairs])))
        .to_dict()
        .value())
        
# Functionality

The code is pretty self-explanatory.  In general, operations are lazy wherever possible, so that (e.g.)

    (Chain(collection)
        .map(map_function)
        .take(10)
        .value())
        
will only ever look at the first 10 elements of `collection`.

Most of the chain operators accept functions of either one, two, or three arguments.  A function of one argument gets each element in turn.  A function of two arguments gets each element and its index.  And a function of three arguments also gets the entire collection.

In almost every case, if the function `fn` is omitted, it defaults to the identity function.  This is not particularly interesting for (e.g.) `map`, but is often useful in (e.g.) `sort_by`.

# Operators

In all of the below, "returns..." really means "replaces the collection stored in Chain with..."

### `length()` (alternatively `size`)

returns the length of the collection.  You'd probably only ever use this as your last call before `value()`.

### `each(fn)` (alternatively `for_each`)

invokes `fn` on each element of the collection, leaving the collection unchanged

### `map(fn)`

applies `fn` to each element and returns the resulting collection

### `append(second_collection)`

appends the `second_collection` to the end of the currently stored collection

### `reduce(fn,memo)`

sets memo to `fn(memo,first_element)` then `fn(memo,second_element)`, and so on, returning the final value of `memo`.

### `reduce_right(fn,memo)`

same as above, but works right-to-left

### `rev()`

reverses the collection

### `find(fn)`

returns the first element for which `fn` produces a truthy value.  Raises an error if no such element exists.

### `collect(fn)`

returns the concatenation of `fn(first_element)`, `fn(second_element)`, etc...

### `filter(fn)`

returns the elements for which `fn` produces a truthy value

### `reject(fn)`

returns the elements for which `fn` produces a falsy value

### `sort_by(fn)`

sorts the collection by the values of `fn`.

### `sort_by_descending(fn)`

sorts the collection by the values of `fn` descending

### `group_by(fn)`

returns pairs where the first element is a value achieved by `fn` and the second element is the elements in the collection that `fn` maps to that value.  

### `count_by(fn)`

returns pairs where the fist element is a value achieved by `fn` and the second element is the number of elements in the collection that `fn` maps to that value

### `distinct_by(fn)`

returns the subset of collection consisting of the first time each value of `fn` appears.  

### `max(fn)`

returns the *element* for which `fn` achieves its largest value (not the value itself)

### `min(fn)`

returns the *element* for which `fn` achieves its smallest value (not the value itself)

### `sum_by(fn)` (also `sum`)

returns the sum of `fn(item)` for each item in the collection

### `shuffle()`

randomly shuffles the elements in the collection

### `first(n)` (also `take(n)`)

returns only the first `n` items. 

### `rest(n)` (also `skip(n)`)

returns all but the first `n` items

### `head()`

returns the first item itself (whereas `first()` would return a collection containing just the first item)

### `to_list()`

if possible, `value()` will return a generator.  Calling `to_list()` immediately before forces it to manifest a list.

### `to_dict()`

as mentioned above, dicts are treated as collections of key-value pairs.  `to_dict()` coerces the collection to an actual Python `dict`.

### `value()`

you must always call `value()` last to return the Chain's value rather than the Chain itself.

# License

Do whatever you want with this code.

# Feedback

I'm sure there's all sorts of stupid design decisions I've made.  Let me know about them!  Or, if you find this useful, let me know that too!

