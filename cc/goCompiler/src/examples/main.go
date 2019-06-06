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
}
