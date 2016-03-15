import operator

class Processor:
    def __init__(self):
        self.top_symbols = {}
        self.ops_queue = {}
        
    def parse(self, operation):
        # disregard "S" at the beginning if it exists
        if operation[0] == "S":
            operation = operation[1:]
            
        timestamp = operation[0:8]
        op_type = operation[8:9]
        op_id = operation[9:21]
        
        # for Add Orders
        if op_type == "A":
            op_trans = operation[21:22]
            op_qty = int(operation[22:28])
            op_symbol = operation[28:34].strip()
            self.ops_queue[op_id] = (op_symbol, op_qty,)
            
        # for Order Executed
        if op_type == "E":
            op_qty = int(operation[21:27])
            queued_op = self.ops_queue.get(op_id)
            if queued_op:
                self.process_symbol_total(queued_op[0], op_qty)
                if op_qty < queued_op[1]:
                    self.ops_queue[op_id] = (self.ops_queue[op_id][0], self.ops_queue[op_id][1] - op_qty,)
                elif op_qty == queued_op[1]:
                    del self.ops_queue[op_id]

        # for Order Traded
        if op_type == "P":
            op_trans = operation[21:22]
            op_qty = int(operation[22:28])
            op_symbol = operation[28:34].strip()
            self.process_symbol_total(op_symbol, op_qty)

        # for Order Cancelled
        if op_type == "X":
            op_qty = int(operation[21:27])
            queued_op = self.ops_queue.get(op_id)
            if queued_op:
                if op_qty < queued_op[1]:
                    self.ops_queue[op_id] =  (self.ops_queue[op_id][0], self.ops_queue[op_id][1] - op_qty,)
                elif op_qty == queued_op[1]:
                    del self.ops_queue[op_id]

    def process_symbol_total(self, symbol, qty):
        total_shares = self.top_symbols.get(symbol)
        if total_shares:
            self.top_symbols[symbol] += qty
        else:
            self.top_symbols[symbol] = qty
        
    def print_top_symbols(self):
        sorted_symbols = sorted(self.top_symbols.items(), key=operator.itemgetter(1), reverse=True)
        for symbol in sorted_symbols[0:10]:
            print(symbol[0].ljust(8), " ", str(symbol[1]).rjust(8))
            
        
            