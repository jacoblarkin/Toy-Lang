#!/usr/bin/env python3

import sys

stack = []
commands = dict([])
min_stack = dict([])
returned = dict([])
numbers = list(map(str, range(100)))

def initialize():
  print("Welcome to the test lang!!! Usefull commands are:")
  print("\t +: add top two numbers on stack")
  print("\t -: negate top number on stack")
  print("\t<>: swap top two objects on stack")
  print("\t p: print top object on stack")
  print("\tp!: pop top object from stack and print it")
  print("\tpa: print the whole stack")
  print("\t .: define a new command")
  print("\t q: quit")
  print("\n")

  commands["+"]  = ["+"]
  commands["-"]  = ["-"]
  commands["<>"] = ["<>"]
  commands["p"]  = ["p"]
  commands["p!"] = ["p!"]
  commands["pa"] = ["pa"]
  commands["q"]  = ["q"]
  commands["."]  = ["."]

  min_stack["+"]  = 2
  min_stack["-"]  = 1
  min_stack["<>"] = 2
  min_stack["p"]  = 1
  min_stack["p!"] = 1
  min_stack["pa"] = 0
  min_stack["q"]  = 0

  returned["+"]  = 1
  returned["-"]  = 1
  returned["<>"] = 2
  returned["p"]  = 1
  returned["p!"] = 0
  returned["pa"] = 0
  returned["q"]  = 0

def check_stack(n):
  good = len(stack) >= n
  if not good:
    print("This command requires at lest "+str(n)+" elements on the stack, but there are only "
    +str(len(stack))+" elements on the stack. Please enter more numbers or a different command.")
  return good

def define_command():
  to_define = input("Enter a name for the new command:\n% ")
  if to_define in commands or to_define in numbers:
    print("ERROR!: "+to_define+" is already defined. Returning to main loop.")
    return
  print("Continue entering existing commands to define a new one.\nEnter . when finished.")
  prompt = "% "
  com_list = []
  stack_len = 0
  need_len = 0
  returned_to_stack = 0
  while True:
    com = input(prompt)
    if com == ".": break
    if com not in commands and com not in numbers:
      print("Unrecognized Command!!!")
      continue
    com_list.append(com)
    if com in numbers:
      stack_len += 1
      returned_to_stack += 1
    else:
      # NEED TO FIX!!!! This is broken right now.
      # UPDATE: Maybe not broken. Need to write test.
      need_len += max(0,(min_stack[com] - returned_to_stack))
      stack_len -= (min_stack[com] - returned[com])
      returned_to_stack = returned[com] + max(0,(returned_to_stack - min_stack[com]))
  min_stack[to_define] = need_len
  returned[to_define] = max(0, stack_len)
  commands[to_define] = com_list


def do_command(com):
    time_to_leave = False
    if com == "+":
      if not check_stack(min_stack[com]): return time_to_leave
      one = stack.pop()
      two = stack.pop()
      stack.append(one+two)
    elif com == "-":
      if not check_stack(min_stack[com]): return time_to_leave
      one = stack.pop()
      stack.append(-1*one)
    elif com == "<>":
      if not check_stack(min_stack[com]): return time_to_leave
      one = stack.pop()
      two = stack.pop()
      stack.append(one)
      stack.append(two)
    elif com in list(map(str, range(100))):
      stack.append(int(com))
    elif com == "p":
      if not check_stack(min_stack[com]): return time_to_leave
      print(stack[-1])
    elif com == "p!":
      if not check_stack(min_stack[com]): return time_to_leave
      one = stack.pop()
      print(one)
    elif com == "pa":
      print(stack)
    elif com == ".":
      define_command()
    elif com == "q":
      time_to_leave = True
    elif com in commands:
      if not check_stack(min_stack[com]): return time_to_leave
      for c in commands[com]:
        time_to_leave = do_command(c)
    else:
      print("Unrecognized Command!!!")
    return time_to_leave

def main_loop():
  prompt = "> "
  while True:
    com = input(prompt)
    time_to_leave = do_command(com)
    if time_to_leave: break


def leave():
  print("Goodbye!")
  sys.exit(0)

if __name__ == "__main__":
  initialize()
  main_loop()
  leave()
