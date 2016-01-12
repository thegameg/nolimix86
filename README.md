# nolimia32
x86 virtual machine with unlimited registers

# Build

## Dependencies

* CMake (2.6+)
* Boost (1.58+)
* LLVM  (3.8local)

### Building

```
mkdir build
cd build
cmake .. -G Ninja # if you want to use ninja
ninja nolimia32
```

A binary `nolimia32` is built in `build/bin`.

### Usage
`nolimia32 [options] <input file>`

`nolimia32 --help` for more options.

# Goal
The goal of `nolimia32` is to simulate a virtual machine with unlimited
registers, called `temporaries` or `temps`.

So this is actually a pseudo x86 assembly, `%t0`, `%t1`, etc. as a register.

## Support

### Instructions
* `addl`
* `call`
* `cltd`
* `cmp`
* `cmpl`
* `idvl`
* `imull`
* `ja`
* `jae`
* `jb`
* `jbe`
* `je`
* `jg`
* `jge`
* `jl`
* `jle`
* `jmp`
* `jne`
* `js`
* `lea`
* `leal`
* `leave`
* `movl`
* `movzbl`
* `negl`
* `pushl`
* `ret`
* `sall`
* `sete`
* `subl`
* `testl`

### Registers
* `eax`
* `ebp`
* `ebx`
* `ecx`
* `edi`
* `edx`
* `esi`
* `esp`
* `t[0-9]+`
