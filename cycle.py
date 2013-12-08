from time import sleep
import sys

from cyberoam import *


# Check login status after this interval.
STATUS_INTERVAL = 60 * 2


def load_pool(poolfile):
	# Load username/password combinations from file.
	pooltxt = open(poolfile).read()
	lines = pooltxt.split('\n')
	pool = map(lambda x: x.split(' '), lines)
	return pool


def cycle(pool):
	# Cycle through a set of username/password combinations,
	# while checking the live login status periodically.
	success = False

	for cred in pool:
		if sendLoginRequest(cred[0], cred[1]):
			print 'Logged in with %s' % cred[0]
			success = True

			while True:
				sleep(STATUS_INTERVAL)
				print 'Checking status of %s' % cred[0]

				if not checkLiveStatus(cred[0]):
					success = False
					break

	if not success:
		print 'Damn! All combinations failed.'
	else:
		cycle()

if __name__ == '__main__':
	cycle(load_pool(sys.argv[1]))
