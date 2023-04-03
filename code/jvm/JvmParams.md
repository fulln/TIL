---
dg-publish: true
---

#java #jvm 

## G1相关JVM参数

1. DisableExplicitGC

> -XX:+DisableExplicitGC

禁止调用System.gc()；但jvm的gc仍然有效

2. ExplicitGCInvokesConcurrent

> -XX:+ExplicitGCInvokesConcurren

该命令表示JVM无论什么时候调用系统GC，都执行CMS GC，而不是Full GC。

3. G1ReservePercent

> -XX:G1ReservePercent

It determines the minimum reserve we should have in the heap to minimize the probability of promotion failure.

4. UseLargePages 

> -XX:+UseLargePages/ -XX:+UseHugeTLBFS.

Large pages, or sometimes huge pages, is a technique to **reduce the pressure** on the processors [TLB](https://en.wikipedia.org/wiki/Translation_lookaside_buffer) caches. These caches are used to speed up the time to translate virtual addresses to physical memory addresses. Most architectures support **multiple page sizes**, often with a base page size of 4 KB. For applications using a lot of memory, for example large Java heaps, it makes sense to have the memory mapped with a **larger page granularity** to increase the chance of a hit in the TLB. On x86-64, 2 MB and 1 GB pages can be used for this purpose and for memory intense workloads this can have a really **big impact**. 

 to leverage large pages the OS needs to be **properly configured** as well

#### Linux

##### Transparent Huge Pages

- `always` - transparent huge pages are used automatically by any application.
- `madvise` - transparent huge pages are only used if the application uses [`madvise()`](https://man7.org/linux/man-pages/man2/madvise.2.html) with the flag `MADV_HUGEPAGE` to mark that certain memory segments should be backed by large pages.
- `never` - transparent huge pages are never used.

The configuration is stored in `/sys/kernel/mm/transparent_hugepage/enabled` and can easily be changed like this:

```
$ echo "madvise" > /sys/kernel/mm/transparent_hugepage/enabled
```

##### HugeTLB pages

When the JVM uses this type of large pages it commits the whole memory range backed by large pages up front[3](https://kstefanj.github.io/2021/05/19/large-pages-and-java.html#fn:zgc). This is needed to ensure that no other reservation depletes the pool of large pages allocated by the OS. This also means that there need to be enough large pages pre-allocated to back the whole memory range at the time of the reservation, otherwise the JVM will fall back to use normal pages.

To configure this type of large pages first check the page sizes available:

```
$ ls /sys/kernel/mm/hugepages/
hugepages-1048576kB  hugepages-2048kB
```

Then configure the number of pages you like for a give size like this[2](https://kstefanj.github.io/2021/05/19/large-pages-and-java.html#fn:root):

```
$ echo 2500 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
```

5. Checking the JVM

To see some basic GC configuration you can run with `-Xlog:gc+init`

6. GCLogFileSize

> -XX:GCLogFileSize=_

GC log file size, requires UseGCLogFileRotation. Set to 0 to only trigger rotation via jcmd

7. HeapDumpOnOutOfMemoryError	

>-XX:+HeapDumpOnOutOfMemoryError

Dump heap to file when java.lang.OutOfMemoryError is thrown

- 配合 `-XX:HeapDumpPath` 指定输出路径;

- 在发生OufOfMemoryError时进行heap dump，那么如果一直发生OutOfMemoryError，是否会一直进行heap dump呢？

  `/hotspot/src/share/vm/utilities/debug.cpp`

  ```cpp
  void report_java_out_of_memory(const char* message) {
    static jint out_of_memory_reported = 0;
  
    // A number of threads may attempt to report OutOfMemoryError at around the
    // same time. To avoid dumping the heap or executing the data collection
    // commands multiple times we just do it once when the first threads reports
    // the error.
    // 许多线程可能会尝试报告 OutOfMemoryError 大约在同时。避免转储堆或执行数据收集多次命令我们只在第一个线程报告时执行一次错误
    if (Atomic::cmpxchg(1, &out_of_memory_reported, 0) == 0) {
      // create heap dump before OnOutOfMemoryError commands are executed
      if (HeapDumpOnOutOfMemoryError) {
        tty->print_cr("java.lang.OutOfMemoryError: %s", message);
        HeapDumper::dump_heap_from_oome();
      }
  
      if (OnOutOfMemoryError && OnOutOfMemoryError[0]) {
        VMError err(message);
        err.report_java_out_of_memory();
      }
  
      if (CrashOnOutOfMemoryError) {
        tty->print_cr("Aborting due to java.lang.OutOfMemoryError: %s", message);
        fatal(err_msg("OutOfMemory encountered: %s", message));
      }
  
      if (ExitOnOutOfMemoryError) {
        tty->print_cr("Terminating due to java.lang.OutOfMemoryError: %s", message);
        exit(3);
      }
    }
  }
  ```

8. MaxGCPauseMillis

> -XX:MaxGCPauseMillis=___

Adaptive size policy maximum GC pause time goal in millisecond, or (G1 Only) the maximum GC time per MMU time slice

- 如果这个参数的值满足不了,会影响响应时间和后续的正常gc

  到达时间阈值之后，G1只是暂停回收还未回收的Region，这些Region会被顺延到之后的GC去执行

- 如果G1设置了`-Xmn`,会导致该参数失效

9. MaxMetaspaceSize

> Maximum size of Metaspaces (in bytes)

这个参数会限制metaspace(包括了Klass Metaspace以及NoKlass Metaspace)被committed的内存大小，会保证committed的内存不会超过这个值，一旦超过就会触发GC，这里要注意和MaxPermSize的区别，MaxMetaspaceSize并不会在jvm启动的时候分配一块这么大的内存出来，而MaxPermSize是会分配一块这么大的内存的。

10. ParallelGCThreads

> -XX:ParallelGCThreads=___

- 默认计算逻辑

```c
unsigned int Abstract_VM_Version::calc_parallel_worker_threads() {
  return nof_parallel_worker_threads(5, 8, 8);
}

unsigned int Abstract_VM_Version::nof_parallel_worker_threads(
                                                      unsigned int num,
                                                      unsigned int den,
                                                      unsigned int switch_pt) {
  if (FLAG_IS_DEFAULT(ParallelGCThreads)) {
    assert(ParallelGCThreads == 0, "Default ParallelGCThreads is not 0");
    // For very large machines, there are diminishing returns
    // for large numbers of worker threads.  Instead of
    // hogging the whole system, use a fraction of the workers for every
    // processor after the first 8.  For example, on a 72 cpu machine
    // and a chosen fraction of 5/8
    // use 8 + (72 - 8) * (5/8) == 48 worker threads.
    unsigned int ncpus = (unsigned int) os::initial_active_processor_count();
    return (ncpus <= switch_pt) ?
           ncpus :
          (switch_pt + ((ncpus - switch_pt) * num) / den);
  } else {
    return ParallelGCThreads;
  }
}
```

- 一般建议和CPU个数相等，因为过多的线程数，可能会影响性能

11. ParallelRefProcEnabled

> -XX:+ParallelRefProcEnabled

Enable parallel reference processing whenever possible

12. PrintGCDateStamps

> -XX:+PrintGCDateStamps

Print date stamps at garbage collection

13. PrintGCDetails

>-XX:-PrintGCDetails

Print more details at garbage collection

`-XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps` 打印绝对时间和相对时间

14. PrintHeapAtGC

> -XX:+PrintHeapAtGC

Print heap layout before and after each GC

15. UseGCLogFileRotation

> -XX:+UseGCLogFileRotation

Rotate gclog files (for long running applications). It requires -Xloggc:<filename>

16. Xloggc

> -Xloggc:___

17. Xms

> -Xms___ ==-XX:InitialHeapSize=___

Initial heap size (in bytes); zero means OldSize + NewSize

Xms Xmx  可以设置相同的值,以免触发扩容

18. Xmx

> -Xmx___ == -XX:MaxHeapSize=___

Maximum heap size (in bytes)

19. Xss

> -Xss___

Thread Stack Size (in Kbytes)
