#!/usr/bin/env python3

import sys

stack = []
commands = dict([])
numbers = list(map(str, range(100)))

class Command:
    def __init__(self, name, fn, min_stack, returned):
        self.name = name
        self.fn = fn
        self.min_stack = min_stack
        self.returned = returned

def plus():
    one = stack.pop()
    two = stack.pop()
    stack.append(one+two)
    return False

def neg():
    one = stack.pop()
    stack.append(-1*one)
    return False

def swap():
    one = stack.pop()
    two = stack.pop()
    stack.append(one)
    stack.append(two)
    return False

def copy():
    one = stack[-1]
    stack.append(one)
    return False

def rot():
    one = stack.pop()
    two = stack.pop()
    three = stack.pop()
    stack.append(two)
    stack.append(one)
    stack.append(three)
    return False

def loop():
    count = stack.pop()
    repeated_command = com[2:]
    if not repeated_command in commands: print("Could not find command "+repeated_command)
    if count < 0: print("Negative count! Nothing was done.")
    while count > 0:
        count -= 1
        time_to_leave = do_command(repeated_command)
    return False

def print_top():
    print(stack[-1])
    return False

def print_pop():
    one = stack.pop()
    print(one)
    return False

def print_all():
    print(stack)
    return False

def quit():
    return True

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

  commands["+"]  = Command("+",  plus,           2, 1)
  commands["-"]  = Command("-",  neg,            1, 1)
  commands["<>"] = Command("<>", swap,           2, 2)
  commands["cp"] = Command("cp", copy,           1, 2)
  commands["rt"] = Command("rt", rot,            3, 3)
  commands["r"]  = Command("r",  loop,           1, 0)
  commands["p"]  = Command("p",  print_top,      1, 1)
  commands["p!"] = Command("p!", print_pop,      1, 0)
  commands["pa"] = Command("pa", print_all,      0, 0)
  commands["q"]  = Command("q",  quit,           0, 0)
  commands["."]  = Command(".",  define_command, 0, 0)

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
  fn = lambda: any([do_command(com) for com in com_list])
  commands[to_define] = Command(to_define, fn, need_len, max(0, stack_len))

def do_command(com):
    time_to_leave = False
    if com[:2] == "r ":
        if not check_stack(commands["r"].min_stack): return time_to_leave
        count = stack.pop()
        repeated_command = com[2:]
        if not repeated_command in commands: print("Could not find command "+repeated_command)
        if count < 0: print("Negative count! Nothing was done.")
        while count > 0:
            count -= 1
            commands[repeated_command].fn()
    elif com in list(map(str, range(100))):
        stack.append(int(com))
    elif com in commands:
        if not check_stack(commands[com].min_stack): return time_to_leave
        time_to_leave = commands[com].fn()
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
