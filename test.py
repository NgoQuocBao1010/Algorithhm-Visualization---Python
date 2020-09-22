# def foo(count):
# 	count += 5

a ={
	'x': 1,
	"y": 2,
	"z": 3,
}

def bar():
	v = [False] * 3
	def foo():
		v[2] = True

	foo()
	return v



print(a[0])