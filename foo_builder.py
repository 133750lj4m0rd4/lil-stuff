#
# "+ 1 - 5 + 10 * 3" -> foo(n)
#

def foo_builder(s:str):
    a = s.split(" ")
    assert len(a)%2==0, "stuff's not in pairs :^("
    
    foo = lambda num: num
    buffer = None
    
    for i in range(int(len(a)/2)):
        new_num = float(a[i*2+1])
        
        if (a[i*2] == "+"):
            buffer = lambda num, new_num=new_num, foo=foo: foo(num) + new_num
            
        elif (a[i*2] == "-"):
            buffer = lambda num, new_num=new_num, foo=foo: foo(num) - new_num
            
        elif (a[i*2] == "/"):
            buffer = lambda num, new_num=new_num, foo=foo: foo(num) / new_num
            
        elif (a[i*2] == "*"):
            buffer = lambda num, new_num=new_num, foo=foo: foo(num) * new_num
            
        else:
            raise Exception(f"such operation as {a[i*2]} not supported :^(")

        foo = buffer
    return foo

