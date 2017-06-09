import aiml

# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
#k.learn("std-startup.xml")
k.verbose(1)
k.bootstrap(learnFiles="std-startup.xml", commands="bootstrap")

#k.learn("std-test.xml")

#k.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
k.saveBrain("bot_brain.brn")
#k.saveBrain("test.brn")


# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.
k.respond("load aiml b")


# Loop forever, reading user input from the command
# line and printing responses.
while True: print(k.respond(input("> ")))

