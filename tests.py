import unittest
from processor import Processor

class ProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.pitch = Processor()
        self.op_timestamp = "28800012"
        self.op_orderid = "AK27GA0000DW"
        self.op_orderid2 = "AK27GA0000DX"
        self.op_orderid3 = "AK27GA0000DY"
        self.op_orderid4 = "AK27GA0000DZ"
        self.shares = "000100"
        self.shares2 = "000200"
        self.shares3 = "000300"
        self.shares4 = "000400"
        self.stock_symbol = "AAPL    "
        self.stock_symbol4 = "GOOG    "
        
    def add_op1(self):
        add_op = self.op_timestamp + "A" + self.op_orderid + "B" + self.shares + self.stock_symbol
        self.pitch.parse(add_op)
        
    def add_op2(self):
        add_op = self.op_timestamp + "A" + self.op_orderid2 + "S" + self.shares2 + self.stock_symbol
        self.pitch.parse(add_op)        

    def add_op3(self):
        add_op = self.op_timestamp + "A" + self.op_orderid3 + "S" + self.shares3 + self.stock_symbol
        self.pitch.parse(add_op)

    def add_op4(self):
        add_op = self.op_timestamp + "A" + self.op_orderid4 + "S" + self.shares4 + self.stock_symbol4
        self.pitch.parse(add_op)

    def test_add_order(self):
        # Add an order and check that the queue has it
        self.add_op1()
        self.assertEqual(self.pitch.ops_queue[self.op_orderid][0], 'AAPL')
        self.assertEqual(self.pitch.ops_queue[self.op_orderid][1], 100)
        
        # Add a second order and check that the queue has the second order
        self.add_op2()
        self.assertEqual(self.pitch.ops_queue[self.op_orderid2][1], 200)

    def test_execute_order(self):
        # Add an order and execute
        self.add_op1()
        exec_op = self.op_timestamp + "E" + self.op_orderid + self.shares
        self.pitch.parse(exec_op)

        # Check that the queue emptied after the execute and that the shares were
        # added to top symbols
        self.assertEqual(self.pitch.ops_queue.get(self.op_orderid), None)
        self.assertEqual(self.pitch.top_symbols[self.stock_symbol.strip()], 100)

        # Add a second order and execute, total should be sum of op1 + op2
        self.add_op2()
        exec_op = self.op_timestamp + "E" + self.op_orderid2 + self.shares2
        self.pitch.parse(exec_op)
        self.assertEqual(self.pitch.top_symbols[self.stock_symbol.strip()], 300)

        # Add a third order and do a trade this, total should be sum of op1 + op2 + op2
        self.add_op3()
        trade_op = self.op_timestamp + "P" + self.op_orderid3 + self.shares3
        self.pitch.parse(trade_op)
        self.assertEqual(self.pitch.top_symbols[self.stock_symbol.strip()], 600)
        
        # Add a fourth order with and do a trade this, total should be sum of op1 + op2 + op2
        self.add_op4()
        trade_op = self.op_timestamp + "P" + self.op_orderid4 + self.shares4
        self.pitch.parse(trade_op)
        self.assertEqual(self.pitch.top_symbols[self.stock_symbol4.strip()], 400)
        
    def test_cancel_order(self):
        # Add an order and cancel it
        self.add_op1()
        cancel_op = self.op_timestamp + "X" + self.op_orderid + self.shares
        self.pitch.parse(cancel_op)

        # Check that the queue emptied after the cancel
        self.assertEqual(self.pitch.ops_queue.get(self.op_orderid), None)        
                        
if __name__ == '__main__':
    unittest.main()