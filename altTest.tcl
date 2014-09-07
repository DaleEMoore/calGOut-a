##########
# From http://python.6.x6.nabble.com/Tkinter-and-Alt-bindings-td4374593.html
# Run it with "wish altTest.tcl"
# It works perfectly on "Ubuntu 13.10 \n \l"
entry .e
grid .e -column 0 -row 0
bind . <Alt-s> {puts "Alt-s pressed"}
focus .e
#########