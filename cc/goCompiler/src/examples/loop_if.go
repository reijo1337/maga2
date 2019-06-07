package main

import (
	"fmt"
)

func printLotsHelloWorld() {
	for i := 0; i < 10; i++ {
		if i%2 == 0 {
			fmt.Println("HELLO")
		} else {
			fmt.Println("WORLD")
		}
	}
}

func main() {
	printLotsHelloWorld()
}
