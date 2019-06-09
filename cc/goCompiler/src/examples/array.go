package main

import "fmt"

func main() {
	a := []int{
		7,
		1,
		5,
	}

	d := a[0]
	fmt.Println(d)
	e := a[1]
	fmt.Println(e)
	f := a[2]
	fmt.Println(f)

	fmt.Println("\n")

	bubbleSort(a)
}

func bubbleSort(a []int) {
	n := len(a)
	for i := 0; i < n-1; i++ {
		for j := 0; j < n-i-1; j++ {
			b := a[j]
			c := a[j+1]
			fmt.Println(b)
			fmt.Println(c)
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
