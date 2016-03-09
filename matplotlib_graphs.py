def allocation_bar(allocation, save_to = None):
	# http://matplotlib.org/examples/api/barchart_demo.html
	# http://matplotlib.org/examples/pylab_examples/barchart_demo.html
	funds = list(ETF_ALLOCATION_DICT[allocation].keys())
	percentages = [x * 100 for x in ETF_ALLOCATION_DICT[allocation].values()]

	width = 0.35
	y_pos = np.arange(len(funds))

	# fig = plt.figure(figsize = (8,8)) 
	fig, ax = plt.subplots()
	# ax = fig.add_axes([0.1, 0.2, 0.7, 0.7])
	# colors: http://matplotlib.org/examples/color/named_colors.html
	ax.set_xlabel('Portfolio Percentage (%)')
	ax.set_ylabel('Vanguard ETF Ticker')
	ax.set_yticks(y_pos)
	ax.set_yticklabels(funds)
	ax.set_title('Your Portfolio Allocation: ' + allocation)
	ax.set_xlim(0, 1.1 * max(percentages))
	ax.set_ylim(-1, len(funds))

	rects = ax.barh(y_pos, percentages, 0.65, align='center', color = 'thistle')

	for rect in rects: 
		ax.text(rect.get_width() + 0.40, rect.get_y() + rect.get_height()/4., rect.get_width())

	if save_to is None: 
		plt.show()
	else: 
		fig.savefig(save_to)

	# plot_url = py.plot_mpl(fig, filename='User-Allocation')
	# tls.get_embed(py.plot_mpl(fig, filename='User-Allocation'))


def fund_performance_graph(allocation, hist_period, wealth, save_to = None):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF;")
	prices = pf_prices.fetchall()
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [x[1] * wealth for x in prices]
	x_pos = np.arange(len(date_list))

	# fig = plt.figure(figsize = (8,8))
	# ax = fig.add_axes([0.1, 0.2, 0.85, 0.75])

	fig, ax = plt.subplots()

	ax.plot(date_list, price_list, color = 'skyblue')
	ax.fill_between(date_list, price_list, facecolor='skyblue', alpha = 0.5, lw=0.5)

	ax.set_ylim(min(price_list) - (wealth // 10), max(price_list) + (wealth // 10))
	ax.set_xlabel('Year')
	ax.set_ylabel('Portfolio Value ($)')
	ax.set_title(allocation + " Past " + hist_period[:-1] + "-Year Portfolio Performance")

	# ax.text(1000, 2500, 'Value After 10 Years: ' + str(price_list[-1]), fontsize=10)

	# if save_to is None: 
	# 	plt.show()
	# else: 
	# 	fig.savefig(save_to)

	plot_url = py.plot_mpl(fig, filename='User-Portfolio-Performance')
	# tls.get_embed(py.plot_mpl(fig, filename='User-Portfolio-Performance'))


def graph_worst_year(allocation, hist_period, wealth, save_to = None):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	worst_year_change, worst_year_start_date, worst_year_end_date, best_year_start_date, best_year_end_date, best_year_change = find_worst_and_best_year(allocation, hist_period)
	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF WHERE Date >= '" + worst_year_start_date + "' AND Date <= '" + worst_year_end_date + "';")
	prices = pf_prices.fetchall()
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [(x[1] / prices[0][1]) * wealth for x in prices]
	x_pos = np.arange(len(date_list))

	# fig = plt.figure(figsize = (8,8))
	# ax = fig.add_axes([0.1, 0.2, 0.85, 0.75])

	fig, ax = plt.subplots()

	ax.plot(date_list, price_list, color = 'red')
	ax.fill_between(date_list, price_list, facecolor='red', alpha = 0.5, lw=0.5)


	ax.set_ylim(min(price_list) - (wealth // 10), max(price_list) + (wealth // 10))
	ax.set_xlabel('Year')
	ax.set_ylabel('Portfolio Value ($)')
	ax.set_title(allocation + " Worst 12 Month Performance Over Past 10 Years")

	# http://stackoverflow.com/questions/10998621/rotate-axis-text-in-python-matplotlib
	for tick in ax.get_xticklabels():
		tick.set_rotation(90)

	# if save_to is None: 
	# 	plt.show()
	# else: 
	# 	fig.savefig(save_to)

	plot_url = py.plot_mpl(fig, filename='User-Worst-Year')
	# tls.get_embed(py.plot_mpl(fig, filename='User-Worst-Year'))