import signal
import gettext
import os

# Handle a ctrl+c at the terminal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Set up translation handling
_ = gettext.translation(
    'phrasebook',
    os.path.join(os.path.dirname(__file__), 'locale/'),
    fallback=True,
).gettext
