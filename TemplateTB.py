
##########################################################
######################## Functions #######################

def commaRpcSemiC (string):
    if string.find(',') >= 0:
        #print("comma found")
        string =string.replace(',', ';');
    else:
        string = string + ';';
    return string;

def paramExtract (string):
    if string.find('integer') > 0 or '[' in string:
        string = string.split();
        paramName = string[2];
    else:
        string = string.split();
        paramName = string[1];
    return paramName;

def portNameExtract (string):
    if '[' in string:
        string = string.split();
        if 'wire' in string or 'reg' in string:
            if 'signed' in string:
                portName = string[4].rstrip(',');
            else:
                portName = string[3].rstrip(',');
        else:
            portName = string[2].rstrip(',');
    else:
        string = string.split();
        if 'wire' in string or 'reg' in string:
            if 'signed' in string:
                portName = string[3].rstrip(',');
            else:
                portName = string[2].rstrip(',');
        else:
            portName = string[1].rstrip(',');
    return portName;

#############################################################

#paramName = paramExtract('parameter   C_BURST_LEN        = 16')
#print(paramName);
#pName = portNameExtract('input signed wire [ram-1:0] rajkclk');
#print(pName);
nameVerilog = input ("Enter verilog File name: ");
if len(nameVerilog) < 1 : nameVerilog = "axi_master.v";
fileTB = nameVerilog.split('.')[0] + '_TB.v';

clockFound = 0;
ports = [];
parameters = [];
moduleName = '';
functionFound = 0;
readHandler = open(nameVerilog,'r');
writeHandler = open(fileTB,'w');

for line in readHandler:
    #print(line.rstrip())
    if line.find('//') >= 0:
        continue;
    
    elif line.find('timescale') > 0:
        writeHandler.write(line);
        
    elif line.startswith('module'):
        lineSeg = line.split();
        moduleName = lineSeg[1];
        print('module ' + moduleName + 'TB' +';');
        writeHandler.write('module ' + moduleName + ';');
        writeHandler.write('\n \n');
        #break;

    elif line.find('parameter') >= 0:
        #print('in parameter block')
        parameters.append(paramExtract(line));
        if line.find(',') >= 0:
            #print("comma found")
            line =line.replace(',', ' ');
        print (line.lstrip().rstrip() + ';');
        writeHandler.write(line.lstrip().rstrip() + ';' + '\n');

    elif line.find('input')>= 0 or line.find('output') >= 0:
        #print('in ports block')
        if line.find('function') >= 0:
            functionFound = 1;
        elif line.find('endfunction') >= 0:
            functionFound = 0;
        if functionFound:
            continue
        
        ports.append(portNameExtract(line));
        if line.find('input') >= 0:
            line = line.replace('wire', '');
            line = line.replace('input ', 'reg ');
            if 'clk' in line or 'CLK' in line:
            #if 'clk' or 'CLK' in line: #logical and syntax error line
                clockFound = 1;
                #print("clk found in design in line:", line, '\n')
        elif line.find('output') >= 0:
            line = line.replace('reg ', '');
            line = line.replace('wire ', '');
            line = line.replace('output ', 'wire ');
        else:
            print('None')
            None;
        line = commaRpcSemiC(line.rstrip());
        print(line);
        writeHandler.write(line + '\n');


if clockFound:
    clockPeriod = input("Enter your desired clock period or press ENTER to get default period: ");
    if len(clockPeriod) < 1:
        clockPeriod = '10';
        print("DefaUlt clock period is: %d", int(clockPeriod))
    writeHandler.write(' \ninitial clk = 0; \n' + 'always #(' + str(int(int(clockPeriod)/2)) + ') clk = ~clk; \n');


#fPort = 0;
lParamInd = len(parameters) - 1;
for param in parameters:
    if param == parameters[0]:
        writeHandler.write( moduleName + '\n');
        writeHandler.write('#(.' + param + '(' + param + '),' + '\n');
    elif param == parameters[lParamInd]:
        writeHandler.write('  .' + param + '(' + param + '))' + '\n');
    else:
        writeHandler.write('  .' + param + '(' + param + '),' + '\n');
    
lPortInd = len(ports) - 1;
for port in ports:
    if port == ports[0]:
        writeHandler.write( moduleName + '_uut' + '\n');
        writeHandler.write(' (.' + port + '(' + port + '),' + '\n');
    elif port == ports[lPortInd]:
        writeHandler.write('  .' + port + '(' + port + '));,' + '\n');
    else:
        writeHandler.write('  .' + port + '(' + port + '),' + '\n');
        
    
writeHandler.write('\ninitial begin');

writeHandler.write('\nend');
writeHandler.write('\nendmodule');
writeHandler.close();
