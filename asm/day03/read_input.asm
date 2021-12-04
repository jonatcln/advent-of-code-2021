	.text

	.globl	read_input
####################################################################################################
# read_input
#
# Reads file contents in buffer.
#
# ARGUMENTS:
# 	$a0	memory address of filename
#	$a1	memory address of buffer
#	$a2	buffer size
####################################################################################################
read_input:
	# save buffer addr and size

	move	$t0, $a1
	move	$t1, $a2

	# open file for reading

	li	$v0, 13		# load system code for open file
				# $a0 already contains filename
	li	$a1, 0		# flag for reading
	li	$a2, 0		# ignore mode
	syscall			# open file
	move	$t2, $v0	# save file descriptor

	# read file contents
	
	li	$v0, 14		# load system code for read file
	move	$a0, $t2	# file descriptor
	move	$a1, $t0	# buffer addr
	move	$a2, $t1	# buffer size
	syscall			# read file contents in buffer
	
	# close file
	
	li	$v0, 16		# load system code for close file
	move	$a0, $t2	# file descriptor
	syscall			# close file

	# return

	jr	$ra
####################################################################################################
