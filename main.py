import hashlib as hasher
import datetime as date


class Blockchain:
    def __init__(self, index, time, data, previous_hash):
        self.index = index
        self.time = time
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.time) + str(self.data) + str(self.previous_hash)).encode())
        return sha.hexdigest()


# blok genezy
def genezy_block():
    return Blockchain(0, date.datetime.now(), "Genezy Blok", "0")


# wszystkie późniejsze bloki w łańcuchu bloków
def next_block(last_block):
    this_index = last_block.index + 1
    this_time = date.datetime.now()
    this_data = str(this_index)
    this_hash = last_block.hash
    return Blockchain(this_index, this_time, this_data, this_hash)


# łańcuch bloków i blok genezy
blockchain = [genezy_block()]
previous_block = blockchain[0]

# ile bloków
num_of_blocks = 20

# dodanie bloku
for i in range(0, num_of_blocks):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print("Blok {}: został dodany do łańcucha bloków!".format(block_to_add.index))
    print(f"Hash: {block_to_add.hash}\n")

# Press the green button in the gutter to run the script.
# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
# print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
# if __name__ == '__main__':
# print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
