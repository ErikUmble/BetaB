Xaddr = "10000000000000000000000000001000"
reset_addr = "10000000000000000000000000000000"
ILLOP_addr = "10000000000000000000000000000100"

n_Xaddr = ''.join(['0' if i == '1' else '1' for i in Xaddr])
n_reset_addr = ''.join(['0' if i == '1' else '1' for i in reset_addr])


def F1():
    print(".subckt F1 restart stall n_stall stall_val[31:0] n_tmp[31:0]")
    print("Xnstall_val stall_val[31:0] n_stall_val[31:0] inverter")
    print("Xinv restart b_n_restart inverter_2")
    print("Xnor2 n_stall restart norSR nor2")
    print("Xbuff_0 norSR b_norSR buffer_2")
    print("Xbuff_1 n_stall b_n_stall buffer")
    print("Xbuff_2 stall b_stall buffer")
    print("Xbuff_3 restart b_restart buffer")
    
    #print("Xtrue 1 constant1")
    for i in range(32):
        if n_Xaddr[31-i] == "1":
            if n_reset_addr[31-i] == "1":
                print(f"X11_{i}_nand2 stall_val[{i}] b_norSR n_tmp[{i}] nand2")
                #print(f"X11tmp{i} n_stall restart n_stall_val[{i}] 1 1 1 n_tmp[{i}] mux4")
            else:
                print(f"X10_{i}_nor2_0 n_stall_val[{i}] b_n_stall nor_nS_sv{i} nor2")
                print(f"X10_{i}_nor2_1 nor_nS_sv{i} b_restart[1] n_tmp[{i}] nor2")
                #print(f"X10tmp{i} n_stall restart n_stall_val[{i}] 1 0 0 n_tmp[{i}] mux4")
        else:
            if n_reset_addr[31-i] == "1":
                print(f"X01_{i}_nand2_0 n_stall_val[{i}] b_stall _tmp{i} nand2")
                print(f"X01_{i}_nand2_1 _tmp{i} b_n_restart n_tmp[{i}] nand2")
                #print(f"X01tmp{i} n_stall restart n_stall_val[{i}] 0 1 1 n_tmp[{i}] mux4")
            else:
                print(f"X00_{i}_and2 b_norSR n_stall_val[{i}] n_tmp[{i}] and2")
                #print(f"X00tmp{i} n_stall restart n_stall_val[{i}] 0 0 0 n_tmp[{i}] mux4")

    print(".ends")


def F2():
    print(".subckt F2 is_ILLOP n_is_ILLOP n_tmp[31:0] extmp[31:0]")
    print("Xbuff_0 is_ILLOP b_is_ILLOP buffer_4")

    for i in range(32):
        if ILLOP_addr[31-i] == "1":
            print(f"X1_{i}_nand2 n_tmp[{i}] n_is_ILLOP extmp[{i}] nand2")
        else:
            print(f"X0_{i}_nor2 n_tmp[{i}] b_is_ILLOP extmp[{i}] nor2")

    
    print(".ends")

def F3():
    print(".subckt F3 pcsel[2:0] stall restart finalsel[1:0]")
    print("Xinv pcsel[1:0] n_pcsel[1:0] inverter")
    print("Xnor3 pcsel[2] stall restart nor3out nor3")
    print("Xnand2_0 n_pcsel[0] nor3out finalsel[0] nand2")
    print("Xnand2_1 n_pcsel[1] nor3out finalsel[1] nand2")
    print(".ends")

if __name__ == "__main__":
    F1()
