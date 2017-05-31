from random import random
from bisect import bisect

from flask import redirect, url_for, render_template, request

from bookish.app import app
from bookish.model import Pair


@app.route("/")
def de():
	evaluation = check(request.args.get("english"), request.args.get("german"))
	return render_template("main.jinja", pair=pick_one(Pair.select()), evaluation=evaluation)


def check(english, german):
	if not english or not german:
		return
	try:
		pair = Pair.get(Pair.english==english, Pair.german==german)
		pair.successes += 1
		result = ('CORRECT!', 'success')
	except Pair.DoesNotExist:
		pair = Pair.get(Pair.english==english)
		result = (pair.english + " = " + pair.german, 'danger')

	score = f'<div class="pull-right">{pair.successes}/{pair.attempts - 2}</div>'
	result = result[0] + score, result[1]
	pair.attempts += 1
	pair.save()

	return result


def pick_one(pairs):
	weights = [(p.attempts - p.successes) / p.attempts for p in pairs]
	total = 0
	cum_weights = []
	for w in weights:
		total += w
		cum_weights.append(total)
	x = random() * total
	i = bisect(cum_weights, x)
	return pairs[i]
