from constans import TYPE_ERROR_TEXT

def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__

        for i, (arg_name, type_name) in enumerate(annotations.items()):
            if i < len(args):
                if type_name and not isinstance(args[i], type_name):
                    raise TypeError(
                        TYPE_ERROR_TEXT.format(
                            argument=arg_name,
                            correct_type=type_name.__name__,
                            wrong_type=type(args[i]).__name__
                            )
                    )
                
        for arg_name, value in kwargs.items():
            type_name = annotations.get(arg_name)
            if type_name and not isinstance(value, type_name):
                raise TypeError(
                    TYPE_ERROR_TEXT.format(
                        argument=arg_name,
                        correct_type=type_name.__name__,
                        wrong_type=type(value).__name__
                        )
                )
        
        return func(*args, **kwargs)
    return wrapper

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

def main() -> int:
    print(sum_two(1, 2))
    print(sum_two(a=1, b=2))
    print(sum_two(1.1, "str"))

if __name__ == '__main__':
    main()
