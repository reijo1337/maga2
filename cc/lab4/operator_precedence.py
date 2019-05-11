import sys
import shlex
import csv


errors_dict = {
	"1": "Нельзя ставить операторы друг за другом, (кроме отрицания)",
	"2": "Нельзя ставить логические значения подряд",
	"3": "Нельзя перед знаком отрицания ставить логическое значение",
}


def main(input_string):
	input_ind = list(shlex.shlex(input_string))
	input_ind.append('$')
	
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
	
	operators = order_table[0]
	stack = ['$']

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
		
		if action == 'shift':
			stack.append(buffer_inp)
			input_ind.remove(buffer_inp)
		elif action == 'reduce':
			has_reduce = True
			while has_reduce:
				has_reduce = False
				for i in range(1, len(stack)):
					key = ''.join(stack[i:])
					if key in master.keys():
						has_reduce = True
						stack[i:] = master[key]
						print(stack, "\t\t", input_ind, "\t\t", precedence, "\t\t", action, "\n")
		del buffer_inp, temp1, buffer_stack, temp2, precedence
		
		if vlaag == 0:
			print("Accepted!!")
			return 0
		

if __name__ == "__main__":
	input_string = 't ! ~ f & a'
	main(input_string)
