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
	b.val = 5
	d := &node{}
	d.next = b
	d.val = -10
	g := &node{}
	g.next = d
	g.val = -20
	c := &node{}
	c.val = 7
	c.next = g

	temp := c
	for temp != nil {
		sas := temp.val
		temp := temp.next
		fmt.Println(sas)
	}

	fmt.Println("\n")

	nex := &node{}
	prev := nil
	cur := c
	for cur != nil {
		nex := cur.next
		cur.next = prev
		prev := cur
		cur := nex
	}

	temp := prev
	for temp != nil {
		sas := temp.val
		temp := temp.next
		fmt.Println(sas)
	}
}
