from flask import redirect
from . import thepen


@thepen.route('/', subdomain='thepen')
def ThePenisMightier():
    return redirect('https://www.youtube.com/watch?v=5Zm7NR4-FFw')

