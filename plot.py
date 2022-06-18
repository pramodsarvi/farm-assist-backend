
# importing package
import matplotlib.pyplot as plt
  
# create data
epoch=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
train = [63,66,70,71,75,81,86,90,91,93,94,95,97,96,95,96,97,97,98,98]
valid = [54,55,60,62,64,68,75,78,80,88,91,93,94,95,96,97,98,97,97,97]
  
# # plot lines
# plt.xlabel("Epochs")
plt.ylabel('Accuracy')
plt.plot(epoch, train, label = "train")
plt.plot(epoch, valid, label = "valid")
# plt.savefig("Transfer.jpg")


epochs=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
train1=[25,26,24,25,28,30,34,46,40,48,50,53,54,49,54,55,58,60,58,59,62,64,65,67,70,69,75,78,75,81]
valid1=[26,27,28,26,28,29,30,32,34,35,33,40,42,45,43,46,47,48,50,52,53,51,60,67,70,69,75,78,73,79]
print(len(train1))
print(len(valid1))
plt.plot(epochs, train1, label = "train")
plt.plot(epochs, valid1, label = "valid")
plt.savefig("Normal.jpg")
plt.legend()
plt.show()