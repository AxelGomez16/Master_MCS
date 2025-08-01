U = { "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" }

I =  {"a", "e", "i", "o", "u" }
I_ =  { "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"  } 

II =  { "h", "j", "p", "q", "r", "s"   }
II_ =  { "a", "b", "c", "d", "e", "f", "g", "i", "k", "l", "m", "n", "o", "t", "u", "v", "w", "x", "y", "z"  } 

III =  { "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "o", "u"   }       
III_ =  { "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"  }

IV = { "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s"   }
IV_ = { "a", "b", "c", "d", "e", "i", "o", "t", "u", "v", "w", "x", "y", "z"  } 


# C)
# a = III.union(II)
# b = II_.intersection(IV)
# b_ = U.difference(II_.intersection(IV)) 
# ab_ = a.intersection(b_)


# d)
# a = II.intersection(III)
# a_ = U.difference(a)
# b = I.union(II_)
# b_ = U.difference(b) 
# ab = a_.intersection(b_)


# e)
# a = III.union(II)
# a_ = U.difference(a)
# b = II_.intersection(I)
# b_ = U.difference(b) 
# ab = a_.intersection(b_)


# f)
a = III_.union(II_)
b = II_.intersection(I)
b_ = U.difference(b)
b = II_.intersection(I)
c = IV_.difference(III) 
ab = a.intersection(b_)
abc = ab.difference(c)



print(sorted( abc ))

