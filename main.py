from project.function import replace_in_date
from project.function import hide_sensitive_info
from project.function import program_launch
from project.function import load_transactions
from project.function import execute_transaction

base_files = load_transactions()
base_good_files = execute_transaction(base_files)
sorted_files = replace_in_date(base_good_files)
sorted_list = hide_sensitive_info(sorted_files)
program_result = program_launch(sorted_list)

print(program_result)
