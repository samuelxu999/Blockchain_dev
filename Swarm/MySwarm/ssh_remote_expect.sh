#!/usr/bin/expect -f

## ----------------------- Install dependency ------------------------
## 				sudo apt-get update
## 				sudo apt-get install expect
## -------------------------------------------------------------------

# parse parameters
set argv_len [llength $argv]

if { $argv_len < 3 } {
	send_user "Usage: ./ssh_remote_expect.sh @target_name @target_address @command_lines
	If @command_lines is empty, automaticall login remote machine.\n"
} else {
	set target_name [lindex $argv 0];
	set target_address [lindex $argv 1];
	set command_lines [lindex $argv 2];

	# Get password from local host_password.sec
	set f [open "host_password.sec"];
	set password [ read $f ];
	close $f;

	# Execute ssh command given parameter
	spawn ssh $target_name@$target_address $command_lines;
	expect "assword:";
	send "$password";
	interact;
}