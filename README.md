# 8-Bit CPU Simulator

An 8-bit CPU simulator written from scratch in Python. The project includes a custom instruction set, assembler, debugger, and stack-based subroutine support. The CPU uses a 256-byte memory space and implements a basic fetch-decode-execute cycle, allowing assembly programs to be loaded and executed instruction by instruction. The next goal is to port this CPU simulator onto SystemVerilog. 

See the research and design notes for further design choices. 

## Architecture

Von Neumann architecture with a single 256-byte memory space shared between instructions and data.

```
┌────────────────────────────────────────────────────┐
│                        CPU                         │
│                                                    │
│  Registers          ALU            Control Unit    │
│  R0 (ACC), R1      ADD, SUB        Fetch           │
│  R2, R3            AND, OR, XOR    Decode          │
│  PC, IR            NOT, SHL, SHR   Execute         │
│  SP, FLAGS         CMP                             │
│                                                    │
├────────────────────────────────────────────────────┤
│                    Memory (256 bytes)              │
│  0x00 ─── Program instructions (grows upward)      │
│  ...                                               │
│  0x80 ─── Data storage                             │
│  ...                                               │
│  0xFF ─── Stack (grows downward)                   │
└────────────────────────────────────────────────────┘
```

## Features

- **Fetch-Decode-Execute Cycle**: Instructions are fetched from memory, decoded via opcode lookup, and executed. 
- **Custom Assembler**: Translates human-readable assembly into machine code using a two-pass algorithm. First pass resolves label addresses, second pass generates bytecode.
- **Label Support**: Write `JMP loop` instead of manually calculating `JMP 6`. The assembler handles address resolution automatically.
- **Debugger**: Execute one instruction at a time, inspecting registers, flags, and memory state at each step.
- **Stack operations**: PUSH/POP for saving and restoring register values, CALL/RET for reusable subroutine calls with automatic return address management.
- **CLI Interface**: Load `.asm` files from the command line with an optional debug mode.

## Instruction Set
The CPU currently supports 22 instructions, including arithmetic, bitwise operations, memory access, branching, and stack operations.

| Opcode | Instruction | Arguments | Description |
|--------|------------|-----------|-------------|
| 0x00 | NOP | N/A | No operation |
| 0x01 | LOAD | Rn, value | Load immediate value into register |
| 0x02 | MOV | Rn, Rm | Copy value from Rm to Rn |
| 0x03 | STORE | Rn, addr | Store register value to memory address |
| 0x04 | ADD | Rn, Rm | Add Rn + Rm, stores the result in R0 |
| 0x05 | SUB | Rn, Rm | Subtract Rn - Rm, stores the result in R0 |
| 0x06 | CMP | Rn, Rm | Compare (subtract without storing), updates flags only |
| 0x07 | JMP | addr | Unconditional jump |
| 0x08 | JZ | addr | Jump if zero flag is set |
| 0x09 | JNZ | addr | Jump if zero flag is not set |
| 0x0A | AND | Rn, Rm | Bitwise AND, result in R0 |
| 0x0B | OR | Rn, Rm | Bitwise OR, result in R0 |
| 0x0C | XOR | Rn, Rm | Bitwise XOR, result in R0 |
| 0x0D | NOT | Rn | Bitwise NOT, result in R0 |
| 0x0E | SHL | Rn | Shift left by 1, result in R0 |
| 0x0F | SHR | Rn | Shift right by 1, result in R0 |
| 0x20 | LOAD_MEM | Rn, addr | Load value from memory address into register |
| 0x21 | PUSH | Rn | Push register value onto stack |
| 0x22 | POP | Rn | Pop top of stack into register |
| 0x23 | CALL | addr | Push return address, jump to subroutine |
| 0x24 | RET | N/A | Pop return address, jump back to caller |
| 0xFF | HLT | N/A | Halt execution |

## Flags

| Flag | Name | Set When |
|------|------|----------|
| Z | Zero | Result of last ALU operation was 0 |
| C | Carry | Unsigned overflow (above 255) or underflow (below 0) |
| N | Negative | Bit 7 of the result is set |

## Usage

Run a program:
```
python main.py programs/countdown.asm
```

Run with step-through debugger:
```
python main.py programs/countdown.asm --debug
```

Debugger controls:
- `Enter`: Execute next instruction
- `r`: Run to completion
- `q`: Quit
- `m`: Show full memory dump

## Example Programs

### Countdown (programs/countdown.asm)
Counts down from 5 to 0 using SUB and conditional branching.

```
LOAD R0, 5
LOAD R1, 1
loop:
SUB R0, R1
JZ end
JMP loop
end:
HLT
```

### Multiplication (programs/multiply.asm)
Multiplies 3 × 4 through repeated addition, demonstrating PUSH/POP for register preservation when the accumulator is required for multiple operations.

```
LOAD R0, 0
LOAD R1, 3
LOAD R2, 4
LOAD R3, 1
loop:
ADD R0, R1
PUSH R0
SUB R2, R3
MOV R2, R0
POP R0
JZ done
JMP loop
done:
STORE R0, 0x80
HLT
```

### Fibonacci (programs/fibonacci.asm)
Computes the first 7 Fibonacci numbers and stores them sequentially in memory starting at address 0x80. Uses LOAD_MEM and STORE to read computed values back from memory for the next computation.

### Subroutine Call (programs/subroutine.asm)
Demonstrates CALL/RET by defining a reusable `add_r1` subroutine that adds R1 to R0. The subroutine is called twice from different points in the program, with RET correctly returning to each call site.

## Project Structure

```
├── main.py          Entry point and CLI interface
├── CPU.py           Fetch-decode-execute cycle and instruction execution
├── ALU.py           Arithmetic and bitwise operations with flag updates
├── Memory.py        256-byte RAM with read/write validation
├── Registers.py     General purpose and special registers with flags
├── assembler.py     Two-pass assembler with label resolution
└── programs/        Example assembly programs
```

## Design Decisions

- **Von Neumann over Harvard**: Single memory space for both instructions and data. Simpler implementation and matches how most real CPUs work. Harvard's parallel access advantage doesn't apply in a sequential simulation.
- **Fixed 3-byte instructions**: Every instruction is exactly 3 bytes (opcode + arg1 + arg2). Wastes some memory on padding but simplifies the fetch cycle, PC always increments by 3.
- **R0 as accumulator**: All ALU results go to R0 by default, eliminating the need for a separate ACC register. Tradeoff is that programs must save R0 (via PUSH) before operations that would overwrite it.
- **8-bit data, 8-bit addresses**: Keeps the address space small (256 bytes) for easy debugging and memory inspection. Real 8-bit CPUs typically used 16-bit addresses for more memory.

## Built With

Python 3 without any external dependencies. All components (CPU, ALU, memory, registers, assembler) are implemented from scratch within the project.
