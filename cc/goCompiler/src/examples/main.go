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
	printChoose(1337)
}

func printHelloWorld() {
    for i := 10; i < 20; i++ {
        fmt.Println(i)
    }
}

func printChoose(i int) {
	a := i
	fmt.Println(a)
}