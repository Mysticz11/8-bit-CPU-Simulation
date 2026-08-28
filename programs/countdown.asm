LOAD R0, 5
LOAD R1, 1
loop:
SUB R0, R1
JZ end
JMP loop
end:
HLT
