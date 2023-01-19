1. What is the IOPS rate system-wide? Per disk? Per controller?

2. What is the throughput rate system-wide? Per disk? Per controller?

3. Which applications/users are using the disks?

4. What file systems or files are being accessed?

5. Have any errors been encountered? Were they due to invalid requests, or issues on the disks?

6. How balanced is the I/O over available disks?

7. What is the IOPS for each transport bus involved?

8. What is the throughput for each transport bus involved?

9. What non-data-transfer disk commands are being issued?

10. Why is disk I/O issued (kernel call path)?

11. To what degree is I/O application-synchronous?

12. What is the distribution of I/O arrival times?

13. What are disk sectors?

14. Why is I/O utilization misleading?

15. Develop a tracing tool to trace all disk commands except for reads and writes