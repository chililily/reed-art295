package main

import (
    "fmt"
    "math"
    "math/rand"
    "time"
)

type packet struct {
    srce int
    dest int
}

// Creates an array of 2^k channels, used for internodal 
// communications.
func make_bundle(k int) (bs []chan packet) {
    width := int(math.Pow(2, float64(k)))
    bs = make([]chan packet, width)
    for i := 0; i < width; i++ {
        bs[i] = make(chan packet)
    }
    return
}

func make_injector(chs []chan packet) {
    n := len(chs)
    go func() {
        for {
            s := rand.Intn(n)
            t := rand.Intn(n)
            fmt.Printf("Injection of packet {%v --> %v}.\n", s, t)
            chs[s] <- packet{s,t}
            time.Sleep(time.Duration(2)*time.Second)
        }
    } ()
}


func node(index int, in <-chan packet, outs []chan packet, report chan packet) {
    
    // Builds list of adjacent nodes
    n := len(outs)
    numNB := int(math.Log2(float64(n)))
    neighbors := make([]int, numNB)
    for i := range neighbors {
        neighbors[i] = index^(1 << uint(i))
    }

    // Main communication/routing loop
    for {
        p := <-in
        if p.dest == index {
            fmt.Printf("Node %v received packet from %v.\n",index,p.srce)
            report <- p
        } else {

            // Selects neighbor to forward packet to.
            //
            // We are looking to bring the value of compare 'closer' 
            // to 11...1. Since a node's neighbors only 
            // differ from it by one bit, we need only find the 
            // neighbor whose 'compare' value is greater than the 
            // current node's.

            match := make([]int, 2)
            for _, v := range neighbors {

                // compare = (v & p.dest) | ~(v | p.dest)

                // Yields the pattern of matching bits between 'v' 
                // and 'p.dest'.
                // Slightly modified, since Go doesn't have a bitwise  
                // NOT operator: (n-1)-x is substituted for ~x, where 
                // n = 2^k.

                compare := (v & p.dest) | ((n-1)-(v | p.dest))
                if compare > match[1] {
                    match[1] = compare
                    match[0] = v
                }
            }
            fmt.Printf("Node %v forwarding packet to node %v {%v --> %v}.\n", index, match[0], p.srce, p.dest)
            outs[match[0]] <- p
        }
    }
}

// Takes an array of channels (built by make_bundle) and a report 
// channel and "builds" the network by allocating the comm channels 
// to individual 'node' goroutines; also assigns a node index and passes 
// the report channel.
func make_hypercube(chs []chan packet, rep chan packet) {
    n := len(chs)
    i := 0
    for i < n {
        go node(i, chs[i], chs, rep)
        i = i + 1
    }
}

func main() {
    chs := make_bundle(3)
    rep := make(chan packet)
    make_injector(chs)
    make_hypercube(chs,rep)
    for x := range rep {
        fmt.Printf("Packet {%v --> %v} routed.\n", x.srce, x.dest)
    }
}
