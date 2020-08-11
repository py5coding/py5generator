from string import Template


class MyTemplate(Template):

    # default
    # idpattern = r'(?a:[_a-z][_a-z0-9]*)'

    # look for quotes
    # idpattern = r'(?a:[^"]*)'

    idpattern = r'(?a:[_a-z][_a-z0-9\|+:]*)'




class EchoDict:

    def __getitem__(self, item):
        print(f'getting {item}')
        return f'[{item}]'


test = """

\"\"\"$class_Sketch_apply_matrix|float:a+float:mouse_x+float:mouse_y\"\"\"


"""

print(MyTemplate(test).substitute(EchoDict()))
