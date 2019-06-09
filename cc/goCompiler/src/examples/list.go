package main

import "fmt"

type node struct {
	val  int
	next *node
}

func main() {
	a := &node{}
	a.val = 1
	a.next = nil
	b := &node{}
	b.next = a
	b.val = 2
	c := &node{}
	c.val = 3
	c.next = b

	temp := c.val
	fmt.Println(temp)
	c := c.next
	temp := c.val
	fmt.Println(temp)
	c := c.next
	temp := c.val
	fmt.Println(temp)
}
