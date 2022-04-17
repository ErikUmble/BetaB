from math import log2

GPC_subckt = """
// Computes the group propagate and generate values
.subckt GPC gh ph gl pl ci ghl phl ch cl
Xgpc_inv_0 gh n_gh inverter
Xgpc_nand2_0 ph gl ph_nand_gl nand2
Xgpc_nand2_1 n_gh ph_nand_gl ghl nand2
Xgpc_nand2_2 ph pl ph_nand_pl nand2
Xgpc_inv_1 ph_nand_pl phl inverter
Xgpc_inv_2 gl n_gl inverter
Xgpc_nand2_3 pl ci plnandci nand2
Xgpc_nand2_4 plnandci n_gl ch nand2
.connect ci cl
.ends
"""


FA_subckt = """
.subckt FA_CLA a b ci g p s
Xfa_xor2_0 a b axorb xor2
Xfa_xor2_1 axorb ci s xor2
Xfa_inv_0 a n_a inverter
Xfa_inv_1 b n_b inverter
Xfa_nand_0 n_a n_b p nand2
Xfa_nand_1 a b anandb nand2
Xfa_inv_2 anandb g inverter
.ends
"""

_CLA = [".subckt CLA32 A[31:0] B[31:0] ci S[31:0] co"]

# FA layer
_CLA.append("Xcla_fa A[31:0] B[31:0] C_0_[31:0] G_1_[31:0] P_1_[31:0] S[31:0] fa_cla")


for tier in range(1, int(log2(32))+1):
    for i in range(31, 0, -2**(tier)):
        cur_rng = 2**(tier-1)
        c_in = "ci" if tier == int(log2(32)) else f"C_{tier}_[{i}]"
        _CLA.append(f'Xcla_gpc_{tier}_{i} G_{tier}_[{i}] P_{tier}_[{i}] G_{tier}_[{i-cur_rng}] P_{tier}_[{i-cur_rng}] {c_in} G_{tier+1}_[{i}] P_{tier+1}_[{i}] C_{tier-1}_[{i}] C_{tier-1}_[{i-cur_rng}] gpc')
_CLA.append("\n// ignore overflow")
_CLA.append("Xignore_overflow co constant0")
_CLA.append(".ends")
CLA_subckt = '\n'.join(_CLA)

if __name__ == "__main__":
    if input("Write CLA code to file CLA.jsim? (y/n): ").lower() == "y":
        with open("CLA.jsim", "w") as file:
            file.write(GPC_subckt + '\n' + FA_subckt + '\n' + CLA_subckt)
