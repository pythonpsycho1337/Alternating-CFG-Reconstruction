SECTION .bss
buf      resb 1

SECTION .text

global _start

increment:
        add ebx, 1
        jmp continue

_start:
        mov  edx, 1             ; max length
        mov  ecx, buf           ; pointer to buffer
        mov  ebx, 0             ; stdin
        mov  eax, 3             ; sys_read
        int  80h                ; perform syscall

        movzx eax, word [buf]   ; x = T (Assume eax is x)

        mov ebx,0

        cmp eax,1
        je increment
continue:
        add ebx, exit
        jmp ebx

exit:
        nop
        mov ebx, 0
        mov eax, 1
        int 0x80

