# def foo(count):
# 	count += 5


def bar():
	v = [False] * 3
	def foo():
		v[2] = True

	foo()
	return v


a = bar()
print(a)