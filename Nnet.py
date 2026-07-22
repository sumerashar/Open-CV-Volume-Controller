#A very Simple Nueral Net in PY. With 3 inputs, 3 weights and a bias.
#You can RMV CMT and try (context: PY)
##****Code****##
#inputs=[1,2,3] #Inputs
#Weights=[0.2,0.5,0.3] #Weights
#bias=0.4 #bias
#output=(inputs[0]*Weights[0]+inputs[1]*Weights[1]+inputs[2]*Weights[2]+bias) #OP calculations
#print("Output of the neuron is:",output) #Prints the output
#4 Input Nnet

#inputs=[1.0,2.0,3.0,2.6]
#weights=[0.2,0.8,-0.5,1.0]
#bias=2.3
#output=(inputs[0]*weights[0]+inputs[1]*weights[1]+inputs[2]*weights[2]+inputs[3]*weights[3]+bias)
#print("Output of the neuron is:",output) #Prints the output

# A complex (bit of) NEts.
inputs=[1.0,2.0,3.0,2.5]
weights=[[0.2,0.8,-0.5,1] 
          ,[91,0.26,0.5,0.3],
          [0.1,0.2,0.3,0.4],
         ]
weights1=weights[0] #1
weights2=weights[1]#2
weights3=weights[2] #3

biases=[2,3,0.5]
bias1=2
bias2=3
bias3=0.5
outputss=[
#Net1
inputs[0]*weights1[1]+
inputs[1]*weights1[2]+
inputs[2]*weights1[3]+
bias1,
]
[
#Net2
inputs[0]*weights2[1]+
inputs[1]*weights2[2]+
inputs[2]*weights2[3]+
bias2,
]

[
#Net3
inputs[0]*weights3[1]+
inputs[1]*weights3[2]+
inputs[2]*weights3[3]+
+bias3,
]





print("Output of the neuron is:",outputss) #Prints the output










