import argparse

def check_mult(var_manager, inputA, inputB, output, n):
    for i in range(n):
        row = var_manager[inputA][i*n:i*n+n]
        for j in range(n):
            column = var_manager[inputB][j::n]
            output_element = var_manager[output][i*n+j]
            string = ""
            for k in range(n):
                string += row[k] + "*" + column[k] + " + "   
            string +=  output_element + " + 1"
            print(string)
    return 0

def node_var_initializer(variable_manager, node_type, number, offset):
    variable_manager[node_type] = ["x"+str(i) for i in range(offset, offset+number)]
    return variable_manager, offset+number

def sigma_connect(variable_manager, in_layer, out_layer,  offset):
    for node_out in variable_manager[out_layer]:
        connection = node_out + " + "
        for node_in in variable_manager[in_layer]:
            connection += node_in + "*x" + str(offset) + " + "
            offset += 1
        connection += "1"
        print(connection)
 
    return variable_manager, offset

def pi_connect(variable_manager, in_layer, out_layer, fanin, offset):
    for node_out in variable_manager[out_layer]:
        switches = []
        for node_A in variable_manager[in_layer[0]]:
            for node_B in variable_manager[in_layer[1]]:
                switches.append(offset)
                print( node_A + "*" + node_B + "*x" + str(offset) + " + " + node_out + "*x" + str(offset) + " + 1") 
                offset+=1
        for switch_1 in switches:
            for switch_2 in switches:
                if switch_1 != switch_2:
                    print("x"+str(switch_1) + "*x" + str(switch_2) + " + 1")
    # enforce atmost 2 fan-in condition by banning 2 incoming wires from same matrix.
    return variable_manager, offset


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--size", type=int, help='input side length of the matrix')
    parser.add_argument("--pi", type=int, help='gates in pi layer')
    parser.add_argument("--fanin", type=int, help='fan in for and gates')
    args = parser.parse_args()
    n = args.size
    fanin = args.fanin

    num_pi_nodes = 0 

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

    var_manager, offset = sigma_connect(var_manager, 'matA', 'input_sigmaA', offset)
    var_manager, offset = sigma_connect(var_manager, 'matB', 'input_sigmaB', offset)
    var_manager, offset = pi_connect(var_manager, ['input_sigmaA', 'input_sigmaB'], 'middle_pi',fanin , offset)
    var_manager, offset = sigma_connect(var_manager, 'middle_pi', 'output_sigma', offset)

    check_mult(var_manager, 'matA', 'matB', 'output_sigma', n)
    
    #print(var_manager)

if __name__== "__main__":
    main()


