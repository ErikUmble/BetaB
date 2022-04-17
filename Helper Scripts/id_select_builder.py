NOP = "10000011111111111111100000000000"
BNE = "01111011110111110000000000000000"

# note that NOP and BNE are written in binary, so the actual indecies are 31-i for correct endianess



if __name__ == "__main__":
    # I did a bunch of trials to determine these buffering amounts
    print(".subckt id_select32 IRSrc[1:0] id[31:0] out[31:0]")
    print("XnIRSrc_inv b_IRSrc[1:0] b_n_IRSrc[1:0] inverter")
    print("XnorIRS IRSrc[1:0] norIRS nor2")
    print("Xbuff_norIRS norIRS b_norIRS buffer_2")
    print("Xbuffer IRSrc[1:0] b_IRSrc[1:0] buffer")
    #print("Xtrue 1 constant1")
    #print("Xfalse 0 constant0")
    for i in range(32):
        if NOP[31-i] == "1":
            if BNE[31-i] == "1":
                print(f"X11_{i}_inv id[{i}] n_id[{i}] inverter")
                print(f"X11_{i}_nand2 n_id[{i}] b_norIRS out[{i}] nand2")
                #print(f"X11tmp{i} IRSrc[0:1] id[{i}] 1 1 1 out[{i}] mux4")
            else:
                print(f"X10_{i}_nor2_0 id[{i}] b_IRSrc[0] nor_IRS_id{i} nor2")
                print(f"X10_{i}_nor2_1 nor_IRS_id{i} b_IRSrc[1] out[{i}] nor2")
                #print(f"X10tmp{i} IRSrc[0:1] id[{i}] 1 0 0 out[{i}] mux4")
        else:
            if BNE[31-i] == "1":
                print(f"X01_{i}_nand2_0 id[{i}] b_n_IRSrc[0] tmp{i} nand2")
                print(f"X01_{i}_nand2_1 tmp{i} b_n_IRSrc[1] out[{i}] nand2")
                #print(f"X01tmp{i} IRSrc[0:1] id[{i}] 0 1 1 out[{i}] mux4")
            else:
                print(f"X00_{i}_and2 b_norIRS id[{i}] out[{i}] and2")
                #print(f"X00tmp{i} IRSrc[0:1] id[{i}] 0 0 0 out[{i}] mux4")

    print(".ends")
