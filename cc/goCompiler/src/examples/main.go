package main

import (
	"fmt"
)

func sample() int {
	a := 42
	b := a / 2
	return b
}

func main() {
	fmt.Println(sample())
}
