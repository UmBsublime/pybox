#! /usr/bin/env python


from functools import wraps
def tags(tag_name):
	def tags_decorator(func):
		@wraps(func)
		def func_wrapper(*args, **kwargs):
			return '<{0}>{1}</{0}>'.format(tag_name, func(*args, **kwargs))
		return func_wrapper
	return tags_decorator


@tags("p")
@tags("div")
def get_text(name):
    return "Hello "+name


class Person(object):
    def __init__(self):
        self.name = "John"
        self.family = "Doe"

    @tags("div")
    @tags("p")
    def get_fullname(self):
        return self.name+" "+self.family


def main():

	my_person = Person()
	print my_person.get_fullname()
	print get_text("John")

if __name__ == "__main__":
	main()