# main.asm - AoC day 3
#
# Runs AoC day 3 part 1 on the given input and prints the result.
#
# ARGUMENTS:
# 	<input_filename>
#		The path to the file containing the input.
#
# INPUT CONSTRAINTS:
# 	The input cannot contain more than 16*1024 bytes (ASCII chars), including newlines!
# 	Anything longer will simply not be read.
# 	The length of the bitstrings (one per line, without newline) can be at most 16 chars.


	.eqv	BUFFER_SIZE	0x4000	# capacity of 16*1024 bytes


	.data

buffer:	.space	BUFFER_SIZE

err_msg_no_input:
	.asciiz	"ERROR: missing required argument <input_filename>"


	.text

	.globl	main
####################################################################################################
# main
#
# Program entry point: runs AoC day 3 part 1.
#
# ARGUMENTS:
# 	$a0	argc
# 	$a1	argv
####################################################################################################
main:
	# retrieve input filename from command line argument and read file contents

	bne	$a0, 1, err_no_input	# error if there are no command line arguments
	lw	$a0, 0($a1)		# get first command line argument (the filename) and store
					# its memory address in the first argument for read_input
	la	$a1, buffer
	li	$a2, BUFFER_SIZE
	jal	read_input		# read the contents of input file in buffer
	
	# run part 1

	la	$a0, buffer
	jal	part1

exit:
	li	$v0, 10
	syscall

err_no_input:
	li	$v0, 4
	la	$a0, err_msg_no_input
	syscall
	j	exit
