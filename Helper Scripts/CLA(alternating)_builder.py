from math import log2

GPC_inv_pn = """
// Computes the negate group propagate and generate values from positive inputs
.subckt GPC_pn gh ph gl pl ci n_ghl n_phl n_ch n_cl
Xgpc_pn_aoi_0 ph gl gh n_ghl aoi21
Xgpc_pn_aoi_1 pl ci gl n_ch aoi21
Xgpc_pn_nand2 pl ph n_phl nand2
Xgpc_pn_inv ci n_cl inverter
.ends
"""

GPC_inv_np = """
// Computes the positive group propagate and generate values from negative inputs
.subckt GPC_np n_gh n_ph n_gl n_pl n_ci ghl phl ch cl
Xgpc_np_oai_0 n_ph n_gl n_gh ghl oai21
Xgpc_np_oai_1 n_pl n_ci n_gl ch oai21
Xgpc_np_nor2 n_pl n_ph phl nor2
Xgpc_np_inv n_ci cl inverter
.ends
"""

GPC_inv_np_ = """
// Computes the positive group propagate and generate values from negative inputs (except that ci is positive input). For highest tier that recieves Cin directly
.subckt GPC_np_ n_gh n_ph n_gl n_pl ci ghl phl ch cl
Xgpc_np_oai_0 n_ph n_gl n_gh ghl oai21
Xgpc_np_oai_1 n_pl n_ci n_gl ch oai21
Xgpc_np_nor2 n_pl n_ph phl nor2
Xgpc_np_inv ci n_ci inverter
.connect ci cl
.ends
"""

FA_inv = """
.subckt FA_CLA_inv a b ci n_g n_p s
Xfa_xor2_0 a b axorb xor2
Xfa_xor2_1 axorb ci s xor2
Xfa_nor2 a b n_p nor2
Xfa_nand_1 a b n_g nand2
.ends
"""

_CLA = [".subckt CLA32 A[31:0] B[31:0] ci S[31:0] co"]

# FA layer
_CLA.append("Xcla_fa A[31:0] B[31:0] C_0_[31:0] G_1_[31:0] P_1_[31:0] S[31:0] fa_cla_inv")


for tier in range(1, int(log2(32))+1):
    for i in range(31, 0, -2**(tier)):
        cur_rng = 2**(tier-1)
        c_in = f"C_{tier}_[{i}]"
        if tier == int(log2(32)):
            c_in = "ci"
            subckt = "gpc_np_" if tier % 2 == 1 else "gpc_pn"
        elif tier % 2 == 1:
            # odd tiers take negative inputs
            subckt = "gpc_np"
        else:
            # even tiers take positive inputs
            subckt = "gpc_pn"
        
        _CLA.append(f'Xcla_gpc_{tier}_{i} G_{tier}_[{i}] P_{tier}_[{i}] G_{tier}_[{i-cur_rng}] P_{tier}_[{i-cur_rng}] {c_in} G_{tier+1}_[{i}] P_{tier+1}_[{i}] C_{tier-1}_[{i}] C_{tier-1}_[{i-cur_rng}] {subckt}')
_CLA.append("\n// ignore overflow")
_CLA.append("Xignore_overflow co constant0")
_CLA.append(".ends")
CLA_subckt = '\n'.join(_CLA)

if __name__ == "__main__":
    if input("Write CLA code to file CLA.jsim? (y/n): ").lower() == "y":
        with open("CLA.jsim", "w") as file:
            file.write(GPC_inv_pn + '\n' + GPC_inv_np + '\n' + GPC_inv_np_ + '\n' + FA_inv + '\n' + CLA_subckt)
