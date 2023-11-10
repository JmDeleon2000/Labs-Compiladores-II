.data 
request: .asciiz "A number please: \n"

.text 
main: 
        li $v0,  4
        la $a0,  request
        syscall       
        li $v0,  5
        syscall             
        move $5, $v0   

        li $v0,  4
        la $a0,  request
        syscall       
        li $v0,  5
        syscall             
        move $6, $v0  

        addi $sp, $sp, -24
        sw $5, 12($sp)
        sw $6, 16($sp)
        jal gcd

        lw $a0, 20($sp) #read returned value
        addi $sp, $sp, 24

        li $v0, 1
        syscall
        

        li $v0, 10
        syscall

# algo from https://www.tutorialspoint.com/cplusplus-program-to-find-g-c-d-using-recursion
gcd:
        sw $ra, 0($sp)
        sw $s0, 4($sp)
        sw $s1, 8($sp)
        lw $5, 12($sp)
        lw $6, 16($sp)

        ### if (a == 0 || b == 0) return 0;
        li $7, 1
        beq $5, $zero, return
        beq $6, $zero, return

        ### if (a == b) return a;
        move $7, $5
        beq $5, $6, return

#if (a < b) 
#      return gcd(a, b-a); 
#else  return gcd(a-b, b); 

        blt $5, $6, lesser

        sub $5, $5, $6
        j recursion
lesser:
        sub $6, $6, $5

recursion:
        addi $sp, $sp, -24      # push

        sw $5, 12($sp)
        sw $6, 16($sp)
        jal gcd
        lw $7, 20($sp)

        addi $sp, $sp, 24      # bring back stack pointer
return:
        lw $ra, 0($sp)        # read registers from stack
        lw $s0, 4($sp)
        lw $s1, 8($sp)
        sw $7, 20($sp)

        jr $ra



