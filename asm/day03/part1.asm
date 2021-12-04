	.eqv	NEWLINE		0x0a	# ASCII code for newline


	.data

counts:	.space	0x20	# 16 * 2 bytes


	.text

	.globl	part1
####################################################################################################
# part1
#
# Runs part 1 and prints the result.
#
# ARGUMENTS:
# 	$a0	mem addr of buffer containing input (a null-terminated ASCII string)
####################################################################################################
part1:
	#*******************************************************************************************
	# PROCEDURE:
	# 	STEP 1: counting 1s
	# 		`counts` keeps track of the number of 1s for each bit. Each count is a
	#		16-bit signed number. So the total number of 1s for the first bit will be
	# 		stored in `0(count)`, for the second bit in `2(count)`, etc.
	# 	STEP 2: determining the most common bits
	# 		For each count, substract the total number of bitstrings floor divided by 2.
	# 		If 	result > 0	=> #1s > #0s	=> 1 is most common
	# 			result <= 0	=> #1s <= #0s	=> 0 is most common (or it's a tie)
	# 		0 is favored in case of a tie, because it's a floor division.
	# 	STEP 3: generating gamma rate (`gamma`)
	# 		Once the first (i.e. the leftmost) most common bit is determined, set the
	# 		rightmost bit of `gamma` to that bit by ORing both values. Then, left shift
	# 		`gamma` one bit before applying the same for the second bit. Repeat this
	# 		process for all bits (left shift `gamma`, OR next most common bit).
	# 	STEP 4: computing epsilon rate (`epsi`)
	# 		The epsilon rate is computed in the same way as the gamme rate, except that
	# 		each time the *least* most common bit is taken. So `epsi` is the same as
	# 		inverting `gamma` (only invert for the relevant `gamma` bits). The only
	# 		difference is that now 1 is favored in case of a tie.
	# 		So `epsi` is computed by `2^(#input_bits) - 1 - gamma`.
	# 	STEP 5: computing power consumption and printing result
	# 		The power consumption is computed by multiplying the gamma rate by the
	# 		epsilon rate. This is the final answer, so print this value.
	#*******************************************************************************************
	
	# start new frame
	sw	$fp, 0($sp)		# push old frame pointer
	move	$fp, $sp		# set new frame pointer to current stack top
	subu	$sp, $sp, 0x18		# allocate 6 * 4 bytes on the stack

	# store locally used registers
	sw	$s0, -0x04($fp)
	sw	$s1, -0x08($fp)
	sw	$s2, -0x0C($fp)
	sw	$s3, -0x10($fp)
	sw	$s4, -0x14($fp)
	sw	$s5, -0x18($fp)
	
	############################################################################################
	
	move	$s0, $a0		# save memory address of buffer in $s0
	
	#===========================================================================================
	# STEP 1: counting 1s
	#===========================================================================================
	# $s0: memomry address of current byte (char) in buffer
	# $s1: 2 * index of current char in current line
	# $s2: 2 * bit width of the numbers (#chars per line)
	# $s3: total number count (#lines)

read_next_char:
	lb	$t0, 0($s0)		# $t0 = current char
	beq	$t0, NEWLINE, next_line
	beq	$t0, 0, end_of_input
	
	lh	$t1, counts($s1)	# $t1 = previous 1s count for this bit
	andi	$t0, $t0, 1
	add	$t1, $t1, $t0		# $t1 += current bit (1 or 0)
	sh	$t1, counts($s1)	# store $t1

	addi	$s0, $s0, 1		# point to the next char
	addi	$s1, $s1, 2		# increment 2*index
	j	read_next_char

next_line:
	move	$s2, $s1		# 2 * bit width = 2 * current index
	addi	$s3, $s3, 1		# increment #lines
	addi	$s0, $s0, 1		# point to the next char
	li	$s1, 0			# reset index to 0
	j	read_next_char

end_of_input:
	sne	$t0, $s1, 0		# if there was no newline before EOI,
	add	$s3, $s3, $t0		# increment #lines with 1


	#===========================================================================================
	# STEP 2 & 3: determining most common bits and generating gamma rate
	#===========================================================================================
	# $s1 := 2 * index of current bit (0 = leftmost)
	# $s2 == 2 * bit width
	# $s3 :: total number count --> total number count floor divided by two
	# $s4 := gamma rate

	li	$s4, 0			# set gamma to 0
	li	$s1, 0			# set index to 0
	srl	$s3, $s3, 1		# floor divide $s3 by two

next_bit:
	lh	$t0, counts($s1)	# $t0 = number of 1s for this bit
	sub	$t0, $t0, $s3		# $t0 -= #numbers/2
	sgt	$t0, $t0, 0		# $t0 = current most common bit
	sll	$s4, $s4, 1		# push $t0 to $s6 from the right
	or	$s4, $s4, $t0
	
	addi	$s1, $s1, 2		# 2 * index += 2
	
	bltu	$s1, $s2, next_bit
	

	#===========================================================================================
	# STEP 4: computing epsilon rate
	#===========================================================================================
	# $s2 :: 2 * bit width --> bit width
	# $s4 == gamma rate
	# $s5 := epsilon rate

	# $s2 = $s2 / 2
	srl	$s2, $s2, 1

	# $t0 = 2^($s2) - 1
	li	$t0, 1
	sllv	$t0, $t0, $s2
	subi	$t0, $t0, 1

	sub	$s5, $t0, $s4		# $s5 = epsilon = $t0 - gamma

	#===========================================================================================
	# STEP 5: computing power consumption and printing result
	#===========================================================================================
	# $s4 == gamma rate
	# $s5 == epsilon rate

	mul	$a0, $s4, $s5		# $t0 = power consumption	
	li	$v0, 1			# load system code for print int
	syscall				# print power consumption

	############################################################################################

	# restore original registers
	lw	$s5, -0x18($fp)
	lw	$s0, -0x14($fp)
	lw	$s1, -0x10($fp)
	lw	$s2, -0x0c($fp)
	lw	$s3, -0x08($fp)
	lw	$s4, -0x04($fp)

	# return to old frame
	move	$sp, $fp		# reset stack pointer to current frame pointer
	lw	$fp, 0($sp)		# restore old frame pointer

	jr	$ra			# return
####################################################################################################
