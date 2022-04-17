from math import log2
"""
JSIM code for Kogge-Stone Adder block
Does not pack many devices per line of code, in order to preserve naming convention
and modular generator code.
"""

BITS = 32
IGNORE_OVERFLOW = True
ADD_BUFFERS = False


BPG_subckt = """
// Computes the bit propagate and generate values
.subckt BPG a b p g
Xbpg_xor2 a b p xor2
Xbpg_nand2 a b anandb nand2
Xbpg_inv anandb g inverter
.ends
"""


GPG_subckt = """
// Computes the group propagate and generate values
.subckt GPG gh ph gl pl ghl phl
Xgpg_inv_0 gh n_gh inverter
Xgpg_nand2_0 ph gl ph_nand_gl nand2
Xgpg_nand2_1 n_gh ph_nand_gl ghl nand2
Xgpg_nand2_2 ph pl ph_nand_pl nand2
Xgpg_inv_1 ph_nand_pl phl inverter
.ends
"""

GG_subckt = """
// Computes the group generate value
.subckt GG gh ph gl ghl
Xgg_inv_0 gh n_gh inverter
Xgg_nand2_0 ph gl ph_nand_gl nand2
Xgg_nand2_1 n_gh ph_nand_gl ghl nand2
.ends
"""

_KSA_subckt = [f".subckt KSA{BITS} A[{BITS-1}:0] B[{BITS-1}:0] ci S[{BITS-1}:0] co"]

# Add Bit Propagete and Generate layer
_KSA_subckt.append("// Computes the Bit Propagate and Generate layer")
for i in range(BITS):
    _KSA_subckt.append(f"Xksa_bpg_{i} A[{i}] B[{i}] ohl_P{i}:{i} ohl_G{i}:{i} bpg")
    

# Add GPG layers
_KSA_subckt.append("\n// Computes the GPG layer")
max_col = BITS - 1 if IGNORE_OVERFLOW else BITS
for tier in range(int(log2(BITS))):
    for i in range(2**tier, max_col):
# note that the wire names involve the range that grows like the binary number with as many ones as the tier
        in_rng = int("0"+"1"*tier, 2) 
        o_rng = in_rng + 2**tier
        _KSA_subckt.append(f"Xksa_gpg_{tier}_{i} inh_G{i}:{i-in_rng} inh_P{i}:{i-in_rng} inl_G{i-in_rng-1}:{max(i-1-2*in_rng, 0)} inl_P{i-in_rng-1}:{max(i-1-2*in_rng, 0)} ohl_G{i}:{max(i-o_rng,0)} ohl_P{i}:{max(i-o_rng, 0)} gpg")

# Add GG layer
_KSA_subckt.append("\n// Computes the GG layer")
for i in range(max_col):
    gg_out = "co" if i+1 == BITS else "gg_out"+str(i)
    _KSA_subckt.append(f"Xksa_gg_{i} inh_G{i}:0 inh_P{i}:0 _ci {gg_out} gg")

# Add constant0 carry out if ignoring overflow
if IGNORE_OVERFLOW:
    _KSA_subckt.append("X_ignore_overflow co constant0")

# Add XOR layer
_KSA_subckt.append("\n// Computes the XOR layer")
for i in range(BITS):
    g_in = "ci" if i == 0 else "gg_out" +str(i-1)
    _KSA_subckt.append(f"Xksa_xor_{i} P{i}:{i} {g_in} S[{i}] xor2")



# Add buffers if desired (only supported for large adder blocks)
if ADD_BUFFERS and BITS >= 16: 
    _KSA_subckt.append("\n// Buffering high load inputs")
    _KSA_subckt.append("Xbuff_ci ci _ci buffer_8")
    
    for j in range(int(log2(BITS))-1):
            _KSA_subckt.append(f"Xbuff_P{j}:0 P{j}:0 _P{j}:0 buffer_4")
            _KSA_subckt.append(f"Xbuff_G{j}:0 G{j}:0 _G{j}:0 buffer_4")
            
    for i in range(len(_KSA_subckt)):
        line = _KSA_subckt[i]
        # buffer P0:0, G0:0, P1:0, G1:0, P2:0, G2:0, etc, for the inputs that are used many times
        for j in range(int(log2(BITS))-1):
            line = line.replace(f'ohl_P{j}:0',f'P{j}:0').replace(f'ohl_G{j}:0', f'G{j}:0').replace(f'inl_P{j}:0', f'_P{j}:0').replace(f'inl_G{j}:0', f'_G{j}:0').replace(f'inh_P{j}:0', f'_P{j}:0').replace(f'inh_G{j}:0', f'_G{j}:0')
        # clear other temporary names
        line = line.replace('inh_', '').replace('inl_', '').replace('ohl_', '')
        _KSA_subckt[i] = line
else:
    for i in range(len(_KSA_subckt)):

        _KSA_subckt[i] = _KSA_subckt[i].replace('_ci', 'ci').replace('inh_', '').replace('inl_', '').replace('ohl_', '')
        
_KSA_subckt.append(".ends")
KSA_subckt = '\n'.join(_KSA_subckt)

if __name__ == "__main__":
    if input("Write KSA code to file KSA.jsim? (y/n): ").lower() == "y":
        with open("KSA.jsim", "w") as file:
            file.write(BPG_subckt + '\n' + GPG_subckt + '\n' + GG_subckt + '\n' + KSA_subckt)


                       
