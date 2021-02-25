with open("sol") as file:
    lines = file.readlines()
    on_wires = []
    for line in lines:
        if line[0] == 'v':
            solution = line.strip().split(' ')
            for item in solution:
                if item[0] == '1':
                    on_wires.append(item[2:])
    print(on_wires)                
