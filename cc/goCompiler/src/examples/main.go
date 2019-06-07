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
	printLotsHelloWorld()
}

func printHelloWorld() {
	for i := 0; i < 10; i++ {
		for j := 0; j < 3; j++ {
			fmt.Println(i)
			fmt.Println(j)
		}
	}
}

func printChoose(i int) {
	if i%2 == 0 {
		fmt.Println("HELLO")
	} else {
		fmt.Println("WORLD")
	}
}

func printLotsHelloWorld() {
	for i := 0; i < 10; i++ {
		if i%2 == 0 {
			fmt.Println("HELLO")
		} else {
			fmt.Println("WORLD")
		}
	}
}
