"""
When the following test will fail, I could be ready to retry import unicode_literals.

sage: from __future__ import unicode_literals
sage: x=var('x')
sage: f(x)=x**2
sage: f(3)
9
sage: f(x=3)
9
"""
