from function import replace_in_date
from function import hide_sensitive_info
from function import program_launch

sorted_files = replace_in_date()
sorted_list = hide_sensitive_info(sorted_files)
program_result = program_launch(sorted_list)

print(program_result)
