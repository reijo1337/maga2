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

	k := []int{
		7,
		1,
		5,
	}

	d := k[0]
	fmt.Println(d)
	e := k[1]
	fmt.Println(e)
	f := k[2]
	fmt.Println(f)

	fmt.Println("\n")

	bubbleSort(k)

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

func bubbleSort(a []int) {
	n := len(a)
	for i := 0; i < n-1; i++ {
		for j := 0; j < n-i-1; j++ {
			b := a[j]
			c := a[j+1]
			if b > c {
				tmp := a[j]
				a[j] = a[j+1]
				a[j+1] = tmp
			}
		}
	}

	g := a[0]
	fmt.Println(g)
	h := a[1]
	fmt.Println(h)
	i := a[2]
	fmt.Println(i)
}
