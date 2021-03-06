import argparse
import random

def node_var_initializer(variable_manager, node_type, number, offset):
    variable_manager[node_type] = ["x"+str(i) for i in range(offset, offset+number)]
    return variable_manager, offset+number

def sigma_connect(variable_manager, in_layer, out_layer,  offset):
    for node_out in variable_manager[out_layer]:
        connection = node_out + " + "
        fanin = []
        for node_in in variable_manager[in_layer]:
            connection += node_in + "*x" + str(offset) + " + "
            fanin.append(offset)
            offset += 1
        
        fanin_constraint = "1 + "
        for i in range(len(fanin)):
            fanin_constraint += "x" + str(fanin[i]) + " + "
            for j in range(i,len(fanin)):
                fanin_constraint += "x" + str(fanin[j]) + "*x" + str(fanin[i]) + " + "

        print(connection[:-3])
        print(fanin_constraint[:-3])
 
    return variable_manager, offset

def pi_connect(variable_manager, in_layer, out_layer, fanin, offset):
    for node_out in variable_manager[out_layer]:
        switches = []
        for node_A in variable_manager[in_layer[0]]:
            for node_B in variable_manager[in_layer[1]]:
                switches.append(offset)
                print( node_A + "*" + node_B + "*x" + str(offset) + " + " + node_out + "*x" + str(offset)) 
                offset+=1
        
        # fanin maximum 2 for each and node, suspiciious`
        for switch_1 in switches:
            for switch_2 in switches:
                if switch_1 != switch_2:
                    print("x"+str(switch_1) + "*x" + str(switch_2))
    return variable_manager, offset

def generate_random_mat(var_manager, matA, matB, matC, n):
    assign = {}
    for i in var_manager[matA]:
        bit = random.randint(0,1)
        assign[i] = bit
        if(bit==0):
            print(i)
        else: 
            print("1 +" + str(i))
        
    for i in var_manager[matB]:
        bit = random.randint(0,1)
        assign[i] = bit
        if(bit==0):
            print(i)
        else:
            print("1 +"+ i)
    
    for i in range(n):
        row = var_manager[matA][i*n:i*n+n]
        for j in range(n):
            column = var_manager[matB][j::n]
            output_element = var_manager[matC][i*n+j]
            val = 0
            for k in range(n):
                val += assign[row[k]] * assign[column[k]]
            if val%2 == 0:
                print(output_element)
            else:    
                print("1 +" + output_element) 

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--size", type=int, help='input side length of the matrix')
    parser.add_argument("--pi", type=int, help='gates in pi layer')
    parser.add_argument("--fanin", default = 2, type=int, help='fan in for and gates')
    parser.add_argument("--seed", default = 42, type=int, help='enter seed')
    args = parser.parse_args()
    n = args.size
    fanin = args.fanin

    num_pi_nodes = 0 

    random.seed(args.seed)

    if args.pi is None:
        num_pi_nodes = n**3 - 1   #better than trivial
    else:
        num_pi_nodes = args.pi

    var_manager = {}  # a dict to keep track of variables
    offset  = 1

    var_manager, offset = node_var_initializer(var_manager, 'matA', n**2, offset)
    var_manager, offset = node_var_initializer(var_manager, 'matB', n**2, offset)
    var_manager, offset = node_var_initializer(var_manager, 'input_sigmaA', n**2, offset)
    var_manager, offset = node_var_initializer(var_manager, 'input_sigmaB', n**2, offset)
    var_manager, offset = node_var_initializer(var_manager, 'middle_pi', num_pi_nodes, offset)
    var_manager, offset = node_var_initializer(var_manager, 'output_sigma', n**2, offset)
    
    last_node_var =  offset-1
    
    var_manager, offset = sigma_connect(var_manager, 'matA', 'input_sigmaA', offset)
    var_manager, offset = sigma_connect(var_manager, 'matB', 'input_sigmaB', offset)
    var_manager, offset = pi_connect(var_manager, ['input_sigmaA', 'input_sigmaB'], 'middle_pi',fanin , offset)
    var_manager, offset = sigma_connect(var_manager, 'middle_pi', 'output_sigma', offset)

    generate_random_mat(var_manager, 'matA', 'matB', 'output_sigma', n) 
    
    print("c "+ str(var_manager))

if __name__== "__main__":
    main()


