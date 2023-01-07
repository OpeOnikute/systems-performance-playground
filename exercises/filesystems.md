1. List all filesystems, their block types and some features
    - Can list all filesystems qwith the mount option, but for the features you can inspect the type and get it's features. e.g. ext4, tmpfs, securityfs etc
        ```
        vagrant@vagrant:~$ mount 
        sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
        proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
        udev on /dev type devtmpfs (rw,nosuid,relatime,size=473252k,nr_inodes=118313,mode=755)
        devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
        tmpfs on /run type tmpfs (rw,nosuid,noexec,relatime,size=100912k,mode=755)
        /dev/mapper/vagrant--vg-root on / type ext4 (rw,relatime,errors=remount-ro,data=ordered)
        securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
        ```

    - You can also list mounted file systems by type, and add labels with the -l flag
        ```
        vagrant@vagrant:~$ sudo mount -l --types ext4
        /dev/mapper/vagrant--vg-root on / type ext4 (rw,relatime,errors=remount-ro,data=ordered)
        vagrant@vagrant:~$ sudo mount -l --types tmpfs
        tmpfs on /run type tmpfs (rw,nosuid,noexec,relatime,size=100912k,mode=755)
        tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
        tmpfs on /run/lock type tmpfs (rw,nosuid,nodev,noexec,relatime,size=5120k)
        tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,mode=755)
        tmpfs on /run/user/1000 type tmpfs (rw,nosuid,nodev,relatime,size=100908k,mode=700,uid=1000,gid=1000)
        ```

2. Find the root filesystem and it’s info
    - You can list the root "/" directory as you normally would with df
        ```
        vagrant@vagrant:~$ df -h /
        Filesystem                    Size  Used Avail Use% Mounted on
        /dev/mapper/vagrant--vg-root   62G  2.0G   57G   4% /
        ```
    - lsblk lists the block devices but if you pass the --fs option, it gives filesystem-related info. The root will be there as well
        ```
        vagrant@vagrant:~$ lsblk  --fs
        NAME                   FSTYPE      LABEL UUID                                   MOUNTPOINT
        sda                                                                             
        └─sda1                 LVM2_member       t2mdkA-YYUs-YGO6-LDxu-I8rk-DdPc-dWScXR 
        ├─vagrant--vg-root   ext4              2380b918-859a-4c05-94dd-112699668ce6   /
        └─vagrant--vg-swap_1 swap              f22638ad-4e42-48f2-8895-2d31935ef112   [SWAP]
        ```
    - To inspect the root filesystem more, you can use the mount commands to see the mount flags as well. Not sure that there's more to find beyond the size, type and mount flags. For capacity, you can micro-benchmark for throughput ability, latency etc 
        ```
        vagrant@vagrant:~$ mount -l | grep root
        /dev/mapper/vagrant--vg-root on / type ext4 (rw,relatime,errors=remount-ro,data=ordered)
        ```

3. *Create a new filesystem

- Create a disk partition. This is what houses the filesystem. Unfortunately, the primary partition in vagrant has no more space for a new partition, so I'll skip this for now. https://opensource.com/article/19/4/create-filesystem-linux-partition

- List all the available filesystem types with `mkfs.<tab><tab>`
    ```
    vagrant@vagrant:~$ mkfs.
    mkfs.bfs     mkfs.btrfs   mkfs.cramfs  mkfs.ext2    mkfs.ext3    mkfs.ext4    mkfs.fat     mkfs.minix   mkfs.msdos   mkfs.ntfs    mkfs.vfat    mkfs.xfs 
    ```

4. Do some micro-benchmarking of the root filesystem latency. Is the disk storage latency significant?

- Use fio so simulate an I/O workload. In the example below we simulate random reads of a 5G file, leading to 90th percentile clat (completion latency) of 460800 nanoseconds. Bandwidth is a max of 137408 KiB/s and average of 74000 KiB/s.

    ```
    root@vagrant:/home/vagrant# fio --runtime=60 --time_based --clocksource=clock_gettime --name=randread --numjobs=1 --rw=randread --random_distribution=pareto:0.9 --bs=8k --size=5g --filename=fio.tmp
    randread: (g=0): rw=randread, bs=(R) 8192B-8192B, (W) 8192B-8192B, (T) 8192B-8192B, ioengine=psync, iodepth=1
    fio-3.1
    Starting 1 process
    randread: Laying out IO file (1 file / 5120MiB)
    Jobs: 1 (f=1): [r(1)][100.0%][r=129MiB/s,w=0KiB/s][r=16.5k,w=0 IOPS][eta 00m:00s]
    randread: (groupid=0, jobs=1): err= 0: pid=15819: Wed Jan  4 22:32:37 2023
    read: IOPS=9250, BW=72.3MiB/s (75.8MB/s)(4336MiB/60001msec)
        clat (nsec): min=1015, max=23810k, avg=105730.13, stdev=198561.71
        lat (nsec): min=1405, max=23811k, avg=106198.96, stdev=198571.93
        clat percentiles (nsec):
        |  1.00th=[   1704],  5.00th=[   1800], 10.00th=[   1880],
        | 20.00th=[   1992], 30.00th=[   2128], 40.00th=[   2288],
        | 50.00th=[   2480], 60.00th=[   2704], 70.00th=[   3344],
        | 80.00th=[ 329728], 90.00th=[ 460800], 95.00th=[ 501760],
        | 99.00th=[ 602112], 99.50th=[ 692224], 99.90th=[ 872448],
        | 99.95th=[ 978944], 99.99th=[3063808]
    bw (  KiB/s): min=18592, max=137408, per=100.00%, avg=74021.58, stdev=39620.08, samples=120
    iops        : min= 2324, max=17176, avg=9252.65, stdev=4952.50, samples=120
    lat (usec)   : 2=20.57%, 4=52.22%, 10=2.22%, 20=0.17%, 50=0.28%
    lat (usec)   : 100=0.03%, 250=0.02%, 500=19.44%, 750=4.73%, 1000=0.27%
    lat (msec)   : 2=0.03%, 4=0.01%, 10=0.01%, 20=0.01%, 50=0.01%
    cpu          : usr=2.50%, sys=6.38%, ctx=136325, majf=7, minf=30
    IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
        submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
        complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
        issued rwt: total=555017,0,0, short=0,0,0, dropped=0,0,0
        latency   : target=0, window=0, percentile=100.00%, depth=1

    Run status group 0 (all jobs):
    READ: bw=72.3MiB/s (75.8MB/s), 72.3MiB/s-72.3MiB/s (75.8MB/s-75.8MB/s), io=4336MiB (4547MB), run=60001-60001msec

    Disk stats (read/write):
        dm-0: ios=135891/5, merge=0/0, ticks=59340/0, in_queue=59348, util=94.91%, aggrios=136261/41, aggrmerge=57/218, aggrticks=57968/1660, aggrin_queue=59628, aggrutil=95.02%
    sda: ios=136261/41, merge=57/218, ticks=57968/1660, in_queue=59628, util=95.02%
    ```

5. What is the file system cache hit ratio? Miss rate?
    - Can't find a traditional tool for this, but the cachestat bcc tool provides information about page cache hits/misses. Under the hood, it gets misses by counting the "add_to_page_cache_lru" and "account_page_dirtied" events using BPF, and gets hits by counting the "mark_page_accessed" and "mark_buffer_dirty" events. Not sure why it uses those events specifically yet. THe read hit % is the ratio of mark_page_accessed over hits + misses and write hit % is the ratio of add_to_page_cache_lru to hits + misses.
        ```
        root@vagrant:/home/vagrant# cachestat-bpfcc 
        HITS   MISSES  DIRTIES  READ_HIT% WRITE_HIT%   BUFFERS_MB  CACHED_MB
        45       48        0      48.4%      51.6%            9        626
        102      128       98       1.7%      13.0%            9        626
        2        0        0     100.0%       0.0%            9        626
        ```

        This tool has some overhead so it's better to use it when there's less activity or degradation is acceptable https://www.brendangregg.com/blog/2014-12-31/linux-page-cache-hit-ratio.html

    - Other approaches are discussed in the blog post above.
        - Use iostat to measure disk reads/writes and assume these are cache misses
        - Drop the page cache (echo 1 > /proc/sys/vm/drop_cache) and measure how performance gets worse
        - Use the cache-hit-rate.stp  SystemTap script.

6. What are the file system cache capacity and current usage?
    - Current usage should be pretty straightforward. Most tools show you the size in memory of the buffer and page cache (free, top, vmstat, sar). You can see the different usages with free:
        ```
        root@vagrant:/home/vagrant# free -mw
                    total        used        free      shared     buffers       cache   available
        Mem:            985          64         248           0           9         662         778
        Swap:           979          11         968
        ```

    - Capacity hm. The "available" field shows you the amount of memory available for starting new applications. It takes into account the page cache and other factors. I will assume that this represents the available capacity for use by the page/buffer caches (amongst other things).

7. What other caches are present, and what are their statistics?
    - The slabtop command lists kernel slab caches, and fs caches are included. In the output below, we can see that there are the dentry, inode, ext4_inode_cache, buffer_head (buffer cache), proc_inode_cache caches etc. It also has their statistics in the output. 
        ```
        root@vagrant:/home/vagrant# slabtop -o
        Active / Total Objects (% used)    : 206209 / 217305 (94.9%)
        Active / Total Slabs (% used)      : 9042 / 9042 (100.0%)
        Active / Total Caches (% used)     : 80 / 118 (67.8%)
        Active / Total Size (% used)       : 52470.83K / 58496.27K (89.7%)
        Minimum / Average / Maximum Object : 0.01K / 0.27K / 8.00K

        OBJS ACTIVE  USE OBJ SIZE  SLABS OBJ/SLAB CACHE SIZE NAME                   
        54660  52716   0%    0.13K   1822       30      7288K kernfs_node_cache      
        26565  25658   0%    0.19K   1265       21      5060K dentry                 
        17080  16818   0%    0.57K   1220       14      9760K radix_tree_node        
        16302  16209   0%    0.59K   1254       13     10032K inode_cache            
        10496  10496 100%    0.03K     82      128       328K kmalloc-32             
        8576   8478   0%    0.06K    134       64       536K pid                    
        8448   8389   0%    0.06K    132       64       528K kmalloc-64             
        7485   3698   0%    1.06K    499       15      7984K ext4_inode_cache       
        7225   6135   0%    0.05K     85       85       340K ftrace_event_field     
        5776   5578   0%    0.20K    304       19      1216K vm_area_struct         
        4608   4608 100%    0.01K      9      512        36K kmalloc-8              
        4352   4352 100%    0.02K     17      256        68K kmalloc-16             
        4232   4232 100%    0.09K     92       46       368K anon_vma               
        3616   2596   0%    0.25K    226       16       904K filp                   
        3366   3169   0%    0.04K     33      102       132K ext4_extent_status     
        2898   2898 100%    0.09K     69       42       276K kmalloc-96             
        2652   2652 100%    0.10K     68       39       272K buffer_head            
        2646   2646 100%    0.19K    126       21       504K cred_jar               
        2508   2198   0%    0.70K    228       11      1824K shmem_inode_cache      
        2448   2391   0%    0.66K    204       12      1632K proc_inode_cache       
        1680   1680 100%    0.19K     80       21       320K kmalloc-192            
        1568   1568 100%    0.07K     28       56       112K Acpi-Operand           
        1552   1080   0%    0.25K     97       16       388K kmalloc-256            
        1426   1426 100%    0.09K     31       46       124K trace_event_file       
        1360   1360 100%    0.02K      8      170        32K lsm_file_cache         
        1312   1312 100%    0.12K     41       32       164K kmalloc-128  
        ```

8. Which applications or users are using the filesystem?
    - The ext4slower bcc tool can show all the filesystem operations if you set the threshold to 0. It lists the process name and PID, and you can get the user from the PID (ps -u -p <pid>)
        ```
        root@vagrant:/home/vagrant# ext4slower-bpfcc 0
        Tracing ext4 operations
        TIME     COMM           PID    T BYTES   OFF_KB   LAT(ms) FILENAME
        22:03:46 check-new-rele 15978  O 0       0           0.00 meta-release
        22:03:46 check-new-rele 15978  R 235     0           1.18 meta-release
        22:03:46 check-new-rele 15978  R 0       0           0.00 meta-release
        22:03:46 check-new-rele 15978  O 0       0           0.00 release-upgrades
        22:03:46 check-new-rele 15978  R 809     0           0.87 release-upgrades
        ```

    - filetop can show the most frequently accessed files. Shows the process name, ID, number and quantity of reads+writes as well.
        ```
        TID    COMM             READS  WRITES R_Kb    W_Kb    T FILE
        14887  sshd             7      1      112     0       O ptmx
        14887  sshd             1      7      16      0       S TCP
        16158  clear            2      0      8       0       R xterm-256color
        16150  filetop-bpfcc    2      0      2       0       R loadavg
        16158  clear            1      0      0       0       R libc-2.27.so
        16158  clear            1      0      0       0       R libtinfo.so.5.9
        16158  filetop-bpfcc    3      0      0       0       R clear
        16158  filetop-bpfcc    2      0      0       0       R ld-2.27.so
        16150  filetop-bpfcc    0      3      0       0       O 0
        16158  clear            0      1      0       0       O 0
        ```
    
    - opensnoop (BCC) traces file opens if you want to be specific about that.
 
9. What files are being created/deleted?
    - fatrace (you have to install it) uses the file access notify API and catches when files are accessed. It doesn't catch deletes though. I created the test files below and used `cat` to see content.
        ```
        root@vagrant:/home/vagrant# fatrace 
        touch(16731): O /home/vagrant/test2.txt
        touch(16731): CW /home/vagrant/test2.txt
        cat(16732): O /home/vagrant/test.txt
        cat(16732): R /home/vagrant/test.txt
        cat(16732): C /home/vagrant/test.txt
        ```
    - For deletes (and creates too) you can use the inotify API (apt install inotify-tools) directly. Below, I created test2, deleted it and checked for the content. The -r option tells it to set watches recursively on subdirectories, and the -m option not to exit after the first event. The set of events watched can be restricted with the -e option: eg. -e create,delete to only print info about directory entries that were created or deleted.
        ```
        root@vagrant:/home/vagrant# inotifywait -mr /home/vagrant
        Setting up watches.  Beware: since -r was given, this may take a while!
        Watches established.
        /home/vagrant/ CREATE test2.txt
        /home/vagrant/ OPEN test2.txt
        /home/vagrant/ ATTRIB test2.txt
        /home/vagrant/ CLOSE_WRITE,CLOSE test2.txt
        /home/vagrant/ DELETE test2.txt
        /home/vagrant/ OPEN test2.txt
        /home/vagrant/ CLOSE_NOWRITE,CLOSE test2.txt
        ```

10. How many errors have been encountered? Was this due to invalid requests or issues from the filesystem?
    - Regular tools like iostat/vmstat don't show i/o errors. All I can see are latency/throughput-related statistics

    - Doesn't look like there's a command that aggregates the count, but disk I/O errors will show up in dmesg output. Not entirely sure of an example, so I'll move on for now. Depending on the error, you can tell whether it's from an invalid request or the filesystem actually has an issue.

11. Why is the filesystem I/O issued? What is the user-level call path?
    - First step is to get the PID of a process that's doing I/O, and then gdb to see the call path (backtrace). I'll choose to use filetop:
        ```
        00:21:37 loadavg: 0.00 0.02 0.00 1/120 20042

        TID    COMM             READS  WRITES R_Kb    W_Kb    T FILE
        20042  clear            2      0      8       0       R xterm-256color
        17986  filetop-bpfcc    2      0      2       0       R loadavg
        20041  sleep            1      0      0       0       R libc-2.27.so
        20042  clear            1      0      0       0       R libtinfo.so.5.9
        20042  clear            1      0      0       0       R libc-2.27.so
        20042  filetop-bpfcc    3      0      0       0       R clear
        20041  bash             3      0      0       0       R sleep
        20041  bash             2      0      0       0       R ld-2.27.so
        20042  filetop-bpfcc    2      0      0       0       R ld-2.27.so
        16194  bash             0      1      0       0       R test.txt
        ```
    
    - Sample gdb backtrace after following instructions in https://wiki.python.org/moin/DebuggingWithGdb
        ```
        (gdb) bt
        #0  0x0000002a95b3b705 in raise () from /lib/libc.so.6
        #1  0x0000002a95b3ce8e in abort () from /lib/libc.so.6
        #2  0x00000000004c164f in posix_abort (self=0x0, noargs=0x0)
            at ../Modules/posixmodule.c:7158
        #3  0x0000000000489fac in call_function (pp_stack=0x7fbffff110, oparg=0)
            at ../Python/ceval.c:3531
        #4  0x0000000000485fc2 in PyEval_EvalFrame (f=0x66ccd8)
            at ../Python/ceval.c:2163
        ...
        ```

12. To what degree do applications directly request file I/O?
    - filetop pretty much shows the direct reads/writes. You can see what applications are doing reads/writes
    - inotify api is another option but it shows every read/write to filetop is still better
    - Getting a total value can be done with iostat

13. *What is the distribution of I/O arrival times?
    - What is an I/O arrival time?

14. Measure a full distribution of file system ops latency for the demo application
    - You can get the PID of the running application and use extdist to get the latency distributions. Either 1-second intervals or a general summary for the entire duration before you interrupt. I can't think of any traditional tools to get this, so we can look at how the BCC tool works.
        ```
        vagrant@vagrant:~$ sudo ext4dist-bpfcc -p 18855 1
        Tracing ext4 operation latency... Hit Ctrl-C to end.

        00:40:20:

        operation = read
            usecs               : count     distribution
                0 -> 1          : 1        |****************************************|
                2 -> 3          : 0        |                                        |
                4 -> 7          : 0        |                                        |
                8 -> 15         : 1        |****************************************|

        operation = write
            usecs               : count     distribution
                0 -> 1          : 0        |                                        |
                2 -> 3          : 0        |                                        |
                4 -> 7          : 0        |                                        |
                8 -> 15         : 0        |                                        |
                16 -> 31         : 0        |                                        |
                32 -> 63         : 1        |****************************************|

        operation = open
            usecs               : count     distribution
                0 -> 1          : 1        |****************************************|
                2 -> 3          : 1        |****************************************|

        00:40:21:
        ```

15. *Measure the portion of each second that the application threads spend in file system operations
    - iotop shows the threads doing I/O and the percentage
        ```
                Total DISK READ :       0.00 B/s | Total DISK WRITE :      27.80 K/s
        Actual DISK READ:       0.00 B/s | Actual DISK WRITE:      47.67 K/s
        TID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN     IO>    COMMAND                                                                                                       
        349 be/3 root        0.00 B/s   27.80 K/s  0.00 %  0.12 % [jbd2/dm-0-8]
        ```

16. Write an observability tool that provides metrics for synchronous/asynchronous file system writes. It should include their rate and latency and be able to identify the process ID that issued them, making it suitable for workload characterization.

17. Develop a tool to provide statistics for indirect and inflated filesystem I/O, additional bytes and I/O not issued directly by applications. The tool shoul d break down this additional I/O into different types to explain their reason.


* TODO - I will need a dummy nginx or mysql server running to simulate the file accesses so I can get a proper backtrace. Right now there's little to trace. Can't do 11-13 without it. Need to create an endpoint that serves an image and turn off caching so it needs to make filesystem requests.


