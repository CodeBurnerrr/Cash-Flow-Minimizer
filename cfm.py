from collections import Counter


class Bank:
    def __init__(self):
        self.name = ""
        self.netAmount = 0
        self.types = set()

    def minimize_cash_flow(self, num_banks, input_list, graph, max_num_types):
        # Find net amount of each bank
        list_of_net_amounts = []

        for b in range(num_banks):
            net_amount = 0

            # Incoming edges
            for i in range(num_banks):
                net_amount += graph[i][b]

            # Outgoing edges
            for j in range(num_banks):
                net_amount += (-1 * graph[b][j])

            list_of_net_amounts.append(
                {'name': input_list[b]['name'], 'netAmount': net_amount, 'types': list(input_list[b]['types'])})

        # Initialize answer graph
        ans_graph = [[(0, '') for _ in range(num_banks)] for _ in range(num_banks)]

        # Find min and max net amount
        num_zero_net_amounts = sum(1 for bank in list_of_net_amounts if bank['netAmount'] == 0)

        # While all banks are not settled
        while num_zero_net_amounts != num_banks:
            min_index = self.get_min_index(list_of_net_amounts, num_banks)  # Most in debt
            max_index, max_matching_type = self.get_max_index(list_of_net_amounts, num_banks, min_index, input_list,
                                                              max_num_types)

            if max_index == -1:
                amount = ans_graph[min_index][0][0] + abs(list_of_net_amounts[min_index]['netAmount'])
                ans_graph[min_index][0] = (
                    amount, list(list_of_net_amounts[min_index]['types'])[0])
                simple_max_index = self.get_simple_max_index(list_of_net_amounts, num_banks)
                amount2 = ans_graph[0][simple_max_index][0] + abs(list_of_net_amounts[min_index]['netAmount'])
                ans_graph[0][simple_max_index] = (amount2,
                                                  list(list_of_net_amounts[simple_max_index]['types'])[0])
                list_of_net_amounts[simple_max_index]['netAmount'] += list_of_net_amounts[min_index]['netAmount']
                list_of_net_amounts[min_index]['netAmount'] = 0
                num_zero_net_amounts += 1 if list_of_net_amounts[min_index]['netAmount'] == 0 else 0
                num_zero_net_amounts += 1 if list_of_net_amounts[simple_max_index]['netAmount'] == 0 else 0

            else:
                transaction_amount = min(abs(list_of_net_amounts[min_index]['netAmount']),
                                         abs(list_of_net_amounts[max_index]['netAmount']))
                ans_graph[min_index][max_index] = (transaction_amount, max_matching_type)
                list_of_net_amounts[min_index]['netAmount'] += transaction_amount
                list_of_net_amounts[max_index]['netAmount'] -= transaction_amount
                num_zero_net_amounts += 1 if list_of_net_amounts[min_index]['netAmount'] == 0 else 0
                num_zero_net_amounts += 1 if list_of_net_amounts[max_index]['netAmount'] == 0 else 0

        return self.print_ans(ans_graph, num_banks, input_list)

    def print_ans(self, ans_graph, num_banks, input_list):
        final_solution = []
        print("\n\t\t\t\t********************* FINAL TRANSACTIONS ***********************\n")

        print("\nThe transactions for minimum cash flow are as follows:\n")
        for i in range(num_banks):
            for j in range(num_banks):

                if i == j:
                    continue

                if ans_graph[i][j][0] != 0 and ans_graph[j][i][0] != 0:
                    if ans_graph[i][j][0] == ans_graph[j][i][0]:
                        ans_graph[i][j][0] = 0
                        ans_graph[j][i][0] = 0
                    elif ans_graph[i][j][0] > ans_graph[j][i][0]:
                        ans_graph[i][j][0] -= ans_graph[j][i][0]
                        ans_graph[j][i] = (0, '')  # Convert tuple to list for assignment
                        statement = f"{input_list[i]['name']} pays Rs {ans_graph[i][j][0]} to {input_list[j]['name']} via {ans_graph[i][j][1]}"
                        print(statement)
                        final_solution.append(statement)
                    else:
                        ans_graph[j][i][0] -= ans_graph[i][j][0]
                        ans_graph[i][j] = (0, '')  # Convert tuple to list for assignment
                        statement = f"{input_list[j]['name']} pays Rs {ans_graph[j][i][0]} to {input_list[i]['name']} via {ans_graph[j][i][1]}"
                        print(statement)
                        final_solution.append(statement)


                elif ans_graph[i][j][0] != 0:
                    statement = f"{input_list[i]['name']} pays Rs {ans_graph[i][j][0]} to {input_list[j]['name']} via {ans_graph[i][j][1]}"
                    print(statement)
                    final_solution.append(statement)

                elif ans_graph[j][i][0] != 0:
                    statement = f"{input_list[j]['name']} pays Rs {ans_graph[j][i][0]} to {input_list[i]['name']} via {ans_graph[j][i][1]}"
                    print(statement)
                    final_solution.append(statement)

                ans_graph[i][j] = (0, '')  # Convert tuple to list for assignment
                ans_graph[j][i] = (0, '')  # Convert tuple to list for assignment
        print("\n")
        return final_solution

    def get_max_index(self, list_of_net_amounts, num_banks, min_index, input_list, max_num_types):
        max_amount = float('-inf')
        max_index = -1
        matching_type = None

        for i in range(num_banks):
            if list_of_net_amounts[i]['netAmount'] == 0 or list_of_net_amounts[i]['netAmount'] < 0:
                continue

            common_types = Counter(list_of_net_amounts[min_index]['types']) & Counter(list_of_net_amounts[i]['types'])

            common_types_list = list(common_types.keys())
            if len(common_types_list) != 0 and max_amount < list_of_net_amounts[i]['netAmount']:
                max_amount = list_of_net_amounts[i]['netAmount']
                max_index = i
                matching_type = common_types_list[0]  # Extract the first common type


        return max_index, matching_type

    def get_min_index(self, list_of_net_amounts, num_banks):
        min_amount = float('inf')
        min_index = -1
        for i in range(num_banks):
            if list_of_net_amounts[i]['netAmount'] == 0:
                continue

            if list_of_net_amounts[i]['netAmount'] < min_amount:
                min_index = i
                min_amount = list_of_net_amounts[i]['netAmount']

        return min_index

    def get_simple_max_index(self, list_of_net_amounts, num_banks):
        max_amount = float('-inf')
        max_index = -1
        for i in range(num_banks):
            if list_of_net_amounts[i]['netAmount'] == 0:
                continue

            if list_of_net_amounts[i]['netAmount'] > max_amount:
                max_index = i
                max_amount = list_of_net_amounts[i]['netAmount']


        return max_index


def main():
    print("\n\t\t\t\t********************* Welcome to CASH FLOW MINIMIZER SYSTEM ***********************\n\n\n")
    print(
        "This system minimizes the number of transactions among multiple banks in the different corners of the world that use different modes of payment. There is one world bank (with all payment modes) to act as an intermediary between banks that have no common mode of payment.\n")
    num_banks = int(input("Enter the number of banks participating in the transactions: "))

    input_list = []
    index_of = {}  # stores index of a bank

    print("\nEnter the details of the banks and transactions as stated:")
    print("Bank name, number of payment modes it has, and the payment modes.")
    print("Bank name and payment modes should not contain spaces.\n")

    max_num_types = 0
    for i in range(num_banks):
        if i == 0:
            bank_name = input(f"Bank {i} (World Bank) : ").strip()
        else:
            bank_name = input(f"Bank {i} : ").strip()

        index_of[bank_name] = i
        num_types = int(input("Enter the number of payment modes: "))

        if i == 0:
            max_num_types = num_types

        types = set()
        for _ in range(num_types):
            type_name = input("Enter payment mode: ").strip()
            types.add(type_name)

        input_list.append({'name': bank_name, 'types': types})

    graph = [[0] * num_banks for _ in range(num_banks)]  # adjacency matrix

    num_transactions = int(input("\nEnter number of transactions: "))

    print("\nEnter the details of each transaction as stated:")
    print("Debtor Bank, creditor Bank, and amount. (Give comma separated values)")
    print("The transactions can be in any order.\n")


    for i in range(num_transactions):
        print(f"{i} th transaction : ", end="")
        s1, s2, amount = input().split(',')
        graph[index_of[s1.strip()]][index_of[s2.strip()]] += int(amount.strip())

    # Create an instance of the Bank class
    bank_instance = Bank()

    # Call the method minimize_cash_flow on the bank_instance
    bank_instance.minimize_cash_flow(num_banks, input_list, graph, max_num_types)


if __name__ == "__main__":
    main()

