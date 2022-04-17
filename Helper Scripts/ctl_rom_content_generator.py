# op2alu takes operations to ALUFN[5:0]
op2alu = {"ADD": 0b000000,
          "SUB": 0b000001,
          "AND": 0b011000,
          "OR": 0b011110,
          "XOR": 0b010110,
          "A": 0b011010,
          "LDR": 0b011010,
          "SHL": 0b100000,
          "SHR": 0b100001,
          "SRA": 0b100011,
          "CMPEQ": 0b110011,
          "CMPLT": 0b110101,
          "CMPLE": 0b110111
          }
# code2op takes an opcode to an operation
code2op ={0b100000: "ADD",
          0b100001: "SUB",
          0b101000: "AND",
          0b101001: "OR",
          0b101010: "XOR",
          0b101100: "SHL",
          0b101101: "SHR",
          0b101110: "SRA",
          0b100100: "CMPEQ",
          0b100101: "CMPLT",
          0b100110: "CMPLE",
          0b011000: "LD",
          0b011001: "ST",
          0b011011: "JMP",
          0b011101: "BEQ",
          0b011110: "BNE",
          0b011111: "LDR",
          0b110000: "ADDC",
          0b110001: "SUBC",
          0b110100: "CMPEQC",
          0b110101: "CMPLTC",
          0b110110: "CMPLEC",
          0b111000: "ANDC",
          0b111001: "ORC",
          0b111010: "XORC",
          0b111100: "SHLC",
          0b111101: "SHRC",
          0b111110: "SRAC"
          }

def ctl_mapper(sigs):
    assert len(sigs) == 10
    #assign don't care values to 0
    for i in range(10):
        if sigs[i] is None:
            sigs[i] = 0
    
    ctl = {}
    ctl["alufn"] = '{0:06b}'.format(op2alu.get(sigs[0], 0b000000))
    ctl["asel"] = '{0:01b}'.format(sigs[1])
    ctl["bsel"] = '{0:01b}'.format(sigs[2])
    ctl["moe"] = '{0:01b}'.format(sigs[3])
    ctl["mwr"] = '{0:01b}'.format(sigs[4])
    
    ctl["ra2sel"] = '{0:01b}'.format(sigs[6])
    ctl["ILLOP"] = '{0:01b}'.format(sigs[7])
    ctl["wdsel"] = '{0:02b}'.format(sigs[8])
    ctl["werf"] = '{0:01b}'.format(sigs[9])

    # add the variable dependent ctls
    if sigs[5] == "Z" or sigs[5] == "NotZ":
        ctl["pcsel"] = "00" + sigs[5]
    else:
        ctl["pcsel"] = '{0:03b}'.format(sigs[5])
    return ctl

print("contents=(")
for opcode in range(64):
    ctl = {}
    # classify the opcode
    operation = code2op.get(opcode, None)
    if operation is None:
        # handle ILLOP
        ctl = ctl_mapper([None, None, None, None, 0, 3, None, 1, 0, 1])
    
    elif operation.endswith("C"):
        ctl = ctl_mapper([operation[:-1], 0, 1, None, 0, 0, None, 0, 1, 1])
    elif operation == "ST":
        ctl = ctl_mapper(["ADD", 0, 1, 0, 1, 0, 1, None, None, 0])
    elif operation == "JMP":
        ctl = ctl_mapper([None, None, None, None, 0, 2, None, 0, 0, 1])
    elif operation == "LDR":
        ctl = ctl_mapper(["A", 1, None, 1, 0, 0, None, 0, 2, 1])
        '''ctl["alufn"] = "101010"
        ctl["asel"] = "1"
        ctl["bsel"] = "0"
        ctl["moe"] = "1"
        ctl["mwr"] = "0"
        ctl["pcsel"] = "000"
        ctl["ra2sel"] = "0"
        ctl["wasel"] = "0"
        ctl["wdsel"] = "10"
        ctl["werf"] = "1"
        '''

    elif operation == "LD":
        ctl = ctl_mapper(["ADD", 0, 1, 1, 0, 0, None, 0, 2, 1])
    elif operation == "BNE":
        ctl = ctl_mapper([None, None, None, None, 0, "NotZ", None, 0, 0, 1])
    elif operation == "BEQ":
        ctl = ctl_mapper([None, None, None, None, 0, "Z", None, 0, 0, 1])
    elif op2alu.get(operation, None) is not None:
        ctl = ctl_mapper([operation, 0, 0, None, 0, 0, None, 0, 1, 1])
        
    print(f"+ 0b{ctl['ILLOP']}{ctl['alufn']}{ctl['wdsel']}    // opcode={'{0:06b}'.format(opcode)} = {operation or '----ILLOP'}")
print(")")
# reminder, wasel changed to ILLOP, since wasel = ILLOP or Interrupt, but this
# only checks ILLOP, so circuit must check Interrupt.
# also, wdsel is not finalized
