from datetime import datetime
import time
import string

t1 = datetime.utcnow()
time.sleep(2)
t2 = datetime.utcnow()

print '%d %d' % (1,2)
a = u"234535341"
c = a.encode("utf-8")
print string.atoi(c)