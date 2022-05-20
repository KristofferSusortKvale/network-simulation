# Actual loop
setup()
if is_test:
    test_setup()

while not end_of_simulation:
    check_received()
    process_package()
    #send_package()

    if is_one_cycle:
        end_of_simulation = True

    if datetime.now() > end_time:
        end_of_simulation = True

write_results()
clean_up()
