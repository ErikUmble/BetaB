**Background

In MIT's 6.004 Computation Structures, each student builds a RISC CPU called Beta, following the ISA specified in the class. As a final project, they must optimize their CPU in both speed and size for a high score on the benchmark test. Full credit on the assignment is achieved with a score of 30. I found the optimization process quite fun, and continued to a score just over 60. I named my optimized CPU BetaB, for Better Beta. 
Project details: 
https://ocw.mit.edu/courses/6-004-computation-structures-spring-2009/resources/mit6_004s09_lab_project/

Benchmark score = e^(10/(size in square meters)*time to run in seconds)
Base implementation (from lab6 without multiplier): circuit size = 1676 gates (319770 square microns); time = 15.08 us Benchmark = 7.95
Optimized BetaB: 3201 gates (322903 square microns); time 7.56 us Benchmark 60.126

**How to run

Download all the main directory files. Use `java -jar jsim.jar BetaB.jsim` and click the 'gate level simulation' button in the new window that pops up. Click the green checkmark to verify the results.  

**Implementation Details

Besides the record of my optimization procedure below, I also kept track of implementation details on paper, to more easily find optimizations and ensure compatability between components. The order of these details follows the procedure below. 

**My optimization procedure

Note that early on in the process, my benchmark time took much longer than the CPU required, since I left a time buffer to avoid problems early on. My score began increasing signficantly later on, at which point I was reducing the clock cycle to the abosolute minimum before measuring the score. 

I merged the read/write ports of main memory that use address ma
Size Improvement 1: circuit size = 1676 gates (2883234 square microns); time = 15.08 us Benchmark = 9.98
I reduced ROM size by computing half of the CTL signals with logic and reduced clock cycle to 6.79 ns (from 7.99)
Size Improvement 2: 1761 gates (287680 square microns); time = 15.08 us Benchmark = 15.115

I replaced the adder with a carry-lookahead adder, reducing clock period to 6.29 ns
Time Improvement 1: 2074 gates (290800 square microns); time: 11.71 us Benchmark = 18.81
I found out about using alternating logic in CLA, and implemented it for a smaller size at the cost of a small amount of time.
Size Improvement: 1916 gates (288954 square microns); time: 11.73 us Benchmark = 19.112

I then replaced the CLA with a Kogge-Stone Adder, which took up much more space, but allowed an even faster clock cycle
Time Improvement 2: 2452 gates (294773 square microns); time 11.68 us Benchmark = 18.255
I tried KSA without buffers, which was just as fast (strange), but only 294490 square microns, so Benchmark 18.3
but still, the CLA achieved a higher benchmark score, so I switched back.
I also tried using an alternating inverting logic CLA design, which was 
by far the smallest, but also was slower. 
I'd expect a more significant time improvement from the new adder, so it might need to have the buffers tweaked or something.
I also tried using the CLA for the PC, but it didn't seem worth it for an unpipelined beta.

I then added buffers to the inputs that were split across many devices, especially the ones that were used 32 times.
Time Improvement 3: 1930 gates (289504 square microns); time 11.61 us Benchmark 19.59

I discovered the temporary debug ports I had added to RegFile for lab6, and removed them,
bringing size down to 283288 and Benchmark up to 20.91.

I then considered whether to remove one of the ports to main memory for a size decrease by making two accesses at separate 
halves of the clock period, or to pipeline the Beta. I figured the pipelining had a better score potential and more learning 
opportunity, so I went with that, which I thought would also give me a better chance to find bottlenecks and optimize them.
I started with a two-stage pipeline (instruction fetch and everything else) as mentioned in the handout.
I don't think I fully understood how control hazards should be handled, so my 2-stage pipeline didn't work.
I decided to follow along the lecture 15 and make the 5-stage version, adding elements in the order taught, to gain a better understanding.
Pipelined Unoptimized: 3728 gates (328131 square microns); time 11.2 us Benchmark 15.196

The first pipelined version that I could get working used partial bypassing, and had some unoptimized logic. 
It had an overall lower benchmark due to the size increase without much time improvement. 
I then cleaned things up a bit with buffers for the following time improvement.
Time Improvement 4: 3741 gates (328638 square microns); time 9.51 us Benchmark 24.523

My first implementation of fully bypassed pipeline had a bug in it,
but it has the potential for a fairly large time gain for the Benchmark test,
so would be worth trying again sometime. 

I then started adding the Exception/Interruption handling for the pipelined implementation. This is not necessary
for the benchmark, and even lowers my score by slowing it down and increasing size slightly, but is important for an
actual implementation, so I did it anyway. (Since I already had the id_select muxes in place, the exception handling did not 
add much to the size or time, and by enabling me to remove several IRQ dependencies as well as the wasel mux in RegFile, 
this version turned out to have a slightly higher benchmark).

Fully Functional Version: 3599 gates (328461 square microns); time 9.31 us Benchmark 26.315

Now I could focus on optimizing the critical path. The id_IF_store involved the bottleneck values. Tracing back the 
signals at the min setup time, I realized Z was a bottleneck, which depends on bp1_out, so we have to optimize the 
bypassing for any improvements here. I considered computing Z for the different stages and muxing, but this would 
have the same tpd. I tried the other partially bypassed implementations, but since alu_out is the bottleneck input,
the previous implementation remained the best. But in the min setup case, the rate is limited by r1d, the regfile output,
so we cannot improve performance with a faster alu. I was able to optimize pcsel computation and pull branch_taken from 
slightly earlier signals. This ended up providing a larger speed boost than I had expected.

Time Improvement 5: 3600 gates (328458 square microns); time 8.91 us Benchmark 30.477
That score is enough for full credit on the assignment. At this point, the critical path now includes the alu_out,
so I could potentially squeeze a little more speed with a better adder or alu logic. I could alternatively try using
full bypassing and see if that performs better.

I tried full bypassing again, and after a little while of debugging, realized a mistake in my computation of bp1sel[0].
I changed this, and now full bypassing works, and my benchmark skyrocketed.

Time Improvement 6: 3738 (331186 square microns); time 7.9288 us Benchmark 45.07
The small additional cost saved many stall cycles in the benchmark test and is well worth it.
Now, all that is left is to clean up the code, look for a few more critical path optimizations, and possibly make
non critical paths slower but smaller. 

Looking at the min setup location, I noticed that the pcsel values are bottleneck. I noticed an inefficiency in the 
computation of pcsel, and fixed it. Just for fun, I left out the logic for forcing pcsel to 0x3 or 0x4 on exception,
since these are not necessary in the benchmark test, and was able to squeeze the clock cycle even smaller. The logic
to fix the exception handling was small, and adding it kept the performance nearly identical. (I still have
not added the checks to find exceptions besides ILLOP and interrupt, but now the ctl can handle those when I do)

Time Improvement 7: 3701 gates (330258 square microns); time 7.556 us Benchmark 54.996
Functionality Improvement: 3706 (330311 square microns); time 7.556 us Benchmark 54.964

Now the critical path is back to the stalldregs, which has bp1_out as the essential bottleneck, which cannot be improved
as far as I can tell, without some large change to the architecture. 

I optimized id_select32.
Size Improvement: 3290 gates (324035 square microns); time 7.531 us Benchmark 60.21

I also similarly optimized the size of PC. At this point, critical path optimization could possibly squeeze another
point or two from the benchmark score, but I'm happy with ending with a score > 60, which is twice the necessary 
for full credit. I reduced the transient analysis time for a more accurate timing of the final Benchmark test.

Optimized BetaB: 3201 gates (322903 square microns); time 7.56 us Benchmark 60.126

**Future improvement possibilities

BetaB could be further improved with branch prediction, logic to generate exceptions for illegal memory/instruction addresses, and more pipeline stages. Caches could be added to enable larger main memory and faster memory accesses. Though beyond the scope of the course, further performance gains could be achieved by combining multiple BetaB CPUs into a multi-core processor. 
