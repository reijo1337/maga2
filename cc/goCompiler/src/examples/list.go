package main

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
	с := &node{}
	с.val = 3
	с.next = b

}
