import sys
import shlex
import csv

from syntax_tree import Tree, visualize_tree

errors_dict = {
	"1": "Нельзя ставить операторы друг за другом, (кроме отрицания)",
	"2": "Нельзя ставить логические значения подряд",
	"3": "Нельзя перед знаком отрицания ставить логическое значение",
}

NUMBER = 0

s = list('' for _ in range(100))
t = 0
n = 0
prn = list('' for _ in range(100))
ch = str()
input_str = str()
input_id = 0
marker = '$'
symbols = list()


def gen_prn(c):
	global n, prn
	n = n + 1
	prn[n] = c


def getch():
	global ch, input_str, input_id
	ch = input_str[input_id]
	input_id = input_id + 1


def get_pol(input_string):
	global input_str, t, n, ch, s, symbols
	input_str = input_string.replace(" ", "")
	done = False
	flag = False
	matrix = []
	with open('order.csv', 'rU') as file2:
		order = csv.reader(file2)
		for row in order:
			matrix.append(row)
	while True:
		n = 0
		getch()
		if ch == marker:
			done = True
		else:
			s[0] = marker
			t = 0
			while t > 0 or ch != marker:
				symbols_s_t = symbols.index(s[t])
				symbols_ch = symbols.index(ch)
				case = matrix[symbols_s_t][symbols_ch]
				if case in ['<', '=']:
					t = t + 1
					s[t] = ch
					getch()
				elif case == '>':
					while True:
						gen_prn(s[t])
						t = t - 1
						if t == 0:
							break
				else:
					print("Строка не подходит")
					print(errors_dict[case])
					flag = True
					break
			if flag:
				flag = False
		if done:
			break


def main(input_string):
	global s, t, prn, input_str, ch, symbols
	input_str = input_string
	input_ind = list(shlex.shlex(input_string))
	input_ind.append('$')
	pol_list = list()
	
	master = {}
	non_terminals = set()
	start_symbol = ''
	grammar = open('grammar.txt', 'r')
	
	for row2 in grammar:
		rule = row2.rstrip('\n').split('->')
		master[rule[1]] = rule[0]
		non_terminals.add(rule[0])
		if start_symbol == '':
			start_symbol = rule[0]

	order_table = []
	with open('order.csv', 'rU') as file2:
		order = csv.reader(file2)
		for row in order:
			order_table.append(row)
	symbols = order_table[0]
	operators = order_table[0]
	stack = ['$']
	tree_stack = [Tree('$')]

	print("Stack", "\t\t\t\t", "Input", "\t\t\t\t", "Precedence relation", "\t\t", "Action")
	
	vlaag = 1
	while vlaag:
		if input_ind[0] == '$' and len(stack) == 2:
			vlaag = 0

		buffer_inp = input_ind[0]
		temp1 = operators.index(str(buffer_inp))
		print("stack",stack, stack[-1])
		if stack[-1] in non_terminals:
			buffer_stack = stack[-2]
		else:
			buffer_stack = stack[-1]
		temp2 = operators.index(str(buffer_stack))

		precedence = order_table[temp2][temp1]
			
		if precedence == '<' or precedence == '=':
			action = 'shift'
		elif precedence == '>':
			action = 'reduce'
		else:
			print("Строка не подходит")
			print(errors_dict[precedence])
			return int(precedence)
				
		print(stack, "\t\t", input_ind, "\t\t", precedence, "\t\t", action, "\n")
		tree_str = ""
		for t in tree_stack:
			tree_str = tree_str + str(t) + " "
		print(f'tree stack: {tree_str}')
		global NUMBER
		if action == 'shift':
			stack.append(buffer_inp)
			tree_stack.append(Tree(buffer_inp + "_" + str(NUMBER)))
			NUMBER = NUMBER + 1
			input_ind.remove(buffer_inp)
		elif action == 'reduce':
			has_reduce = True
			while has_reduce:
				has_reduce = False
				for i in range(1, len(stack)):
					key = ''.join(stack[i:])
					if key in master.keys():
						if len(key) == 3:
							stack_op = operators.index(key[1])
							if order_table[stack_op][temp2] in ['<', '=']:
								continue
						for ch in key:
							if ch not in non_terminals:
								pol_list.append(ch)
						has_reduce = True
						new_tree = Tree(master[key] + "_" + str(NUMBER))
						NUMBER = NUMBER + 1
						for j in range(i, len(tree_stack)):
							new_tree.childs.append(tree_stack[j])
						stack[i:] = master[key]
						tree_stack[i:] = [new_tree]
						print(stack, "\t\t", input_ind, "\t\t", precedence, "\t\t", action, "\n")
						tree_str = ""
						for t in tree_stack:
							tree_str = tree_str + str(t) + " "
						print(f'tree stack: {tree_str}')
		del buffer_inp, temp1, buffer_stack, temp2, precedence
		
		if vlaag == 0:
			print("Accepted!!")
			visualize_tree(tree_stack[1], name=input_string)
			print(f'Постфиксная запись: {"".join(pol_list)}')

			return 0


if __name__ == "__main__":
	input_string = 'a ! t & f'
	main(input_string)
