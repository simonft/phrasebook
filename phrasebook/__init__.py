import signal

# Handle a ctrl+c at the terminal
signal.signal(signal.SIGINT, signal.SIG_DFL)
