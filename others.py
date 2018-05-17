# coding: utf-8

"""
@author: 武明辉 
@time: 2018/5/17 10:34
"""

# ****** 嵌套生成器 *******


def gen_one():
    subgen = range(10)
    yield subgen


def gen_two():
    subgen = range(10)
    for item in subgen:
        yield item
# ****** 嵌套生成器 end *******


# ********** 双向交互**********

def gen():
    yield from subgen()


def subgen():
    while True:
        x = yield
        yield x + 1


def main():
    g = gen()
    print(next(g))
    retval = g.send(3)
    print(retval)
    g.throw(StopIteration)


# ********** 双向交互 end **********

if __name__ == '__main__':
    pass
