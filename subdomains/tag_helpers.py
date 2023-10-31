import functools

from django.template.library import SimpleNode, parse_bits
from django.utils.inspect import getargspec


def silly_tag(register, takes_context=None, name=None):
    """Register a callable as a compiled template tag.

    Basically the same as Django's simple_tag, except that if the result of the
    tag is saved in the context, then there is an additional keyword argument:
    _asvar=True.

    """
    def dec(func):
        params, varargs, varkw, defaults = getargspec(func)
        function_name = (name or getattr(func, '_decorated_function', func).__name__)

        @functools.wraps(func)
        def compile_func(parser, token):
            bits = token.split_contents()[1:]
            target_var = None
            if len(bits) >= 2 and bits[-2] == 'as':
                target_var = bits[-1]
                bits = bits[:-2] + ["_asvar=True"]
            args, kwargs = parse_bits(
                parser, bits, params, varargs, varkw, defaults,
                takes_context, function_name
            )
            return SimpleNode(func, takes_context, args, kwargs, target_var)
        register.tag(function_name, compile_func)
        return func

    return dec
