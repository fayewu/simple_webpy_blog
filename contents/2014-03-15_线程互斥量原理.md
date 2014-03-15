QUQ好久没写了，前几天面试问到的一个问题，线程互斥量的实现，其实很早就发现各个方面都缺乏深入，很容易被问到底。。

说说futex机制（是一个内核态和用户态结合的东西。。他的意思是快速用户空间互斥体。这个快速是从何而来呢？据说futex之前的设计思想都是：不管竞争是否存在，都会进入内核看是否有多个等待同一变量，显然这样是很耗时间的。而futex才用的策略是：创建一个futex同步变量，当某一线程想要访问这个互斥量，这个变量原子性的减1，如果变为0，那么没有竞争的条件发生，如果变为负数，就有竞争的条件发生，需要系统调用，来看一下pthread_mutex_lock和pthread_mutex_unlock代码这部分的示意（很简化）  

pthread_mutex_lock:  

        if  (pthread_mutex_t.value != 0)  
                futex(WAIT)  
        else  
                xxxxxxxxxx 

pthread_mutex_unlock:
       
        if  (pthread_mutex_t.value != 1)  
                futex(WAIT)  
        else  
                xxxxxxxxxx 

<!--more-->
