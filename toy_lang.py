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
  print("\t r: repeat next command\n\t\t"+
          "number of times defined by top element of stack")
  print("\t<>: swap top two objects on stack")
  print("\tcp: copy top object on stack")
  print("\trt: rotate top 3 objects on stack")
  print("\t      e.g.: a b c -> b c a")
  print("\t p: print top object on stack")
  print("\tp!: pop top object from stack and print it")
  print("\tpa: print the whole stack")
  print("\t .: define a new command")
  print("\t q: quit")
  print("\n")

  commands["+"]  = ["+"]
  commands["-"]  = ["-"]
  commands["<>"] = ["<>"]
  commands["cp"] = ["cp"]
  commands["rt"] = ["rt"]
  commands["r"]  = ["r"]
  commands["p"]  = ["p"]
  commands["p!"] = ["p!"]
  commands["pa"] = ["pa"]
  commands["q"]  = ["q"]
  commands["."]  = ["."]

  min_stack["+"]  = 2
  min_stack["-"]  = 1
  min_stack["<>"] = 2
  min_stack["cp"] = 1
  min_stack["rt"] = 3
  min_stack["r"]  = 1
  min_stack["p"]  = 1
  min_stack["p!"] = 1
  min_stack["pa"] = 0
  min_stack["q"]  = 0

  returned["+"]  = 1
  returned["-"]  = 1
  returned["<>"] = 2
  returned["cp"] = 2
  returned["rt"] = 3
  returned["r"]  = 0
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
    if com not in commands and com not in numbers and com[:2] != "r ":
      print("Unrecognized Command!!!")
      continue
    if not com[2:] in commands:
      print("Could not find command "+com[2:])
      continue
    com_list.append(com)
    if com in numbers:
      stack_len += 1
      returned_to_stack += 1
    elif com[:2] != "r ":
      # NEED TO FIX!!!! This is broken right now.
      # UPDATE: Maybe not broken. Need to write test.
      need_len += max(0,(min_stack[com] - returned_to_stack))
      stack_len -= (min_stack[com] - returned[com])
      returned_to_stack = returned[com] + max(0,(returned_to_stack - min_stack[com]))
  # min_stack and returned don't work with looping right now
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
    elif com == "cp":
      if not check_stack(min_stack[com]): return time_to_leave
      one = stack[-1]
      stack.append(one)
    elif com == "rt":
      if not check_stack(min_stack[com]): return time_to_leave
      one = stack.pop()
      two = stack.pop()
      three = stack.pop()
      stack.append(two)
      stack.append(one)
      stack.append(three)
    elif com[:2] == "r ":
      if not check_stack(min_stack["r"]): return time_to_leave
      count = stack.pop()
      repeated_command = com[2:]
      if not repeated_command in commands: print("Could not find command "+repeated_command)
      if count < 0: print("Negative count! Nothing was done.")
      while count > 0:
        count -= 1
        time_to_leave = do_command(repeated_command)
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
