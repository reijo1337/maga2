package main

import (
	"fmt"
)

func sample() int {
	a := 42
	c := a + 12
	b := c / 2
	return b
}

func main() {
	a := sample()
	fmt.Println(a)
	printHelloWorld()
}

func printHelloWorld() {
    for i := 0; i < 10; i++ {
        fmt.Println(i)
    }
}