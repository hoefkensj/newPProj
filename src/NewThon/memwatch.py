# #!/usr/bin/env python
#
# import click
# import psutil
# import time
# import csv
# from datetime import datetime
#
#
# # Define the click command
# @click.command()
# @click.argument('process_name', type=str)
# @click.option('-i', '--interval', type=float, default=1.0, help='Interval in seconds for searching processes')
# def monitor_process(process_name, interval):
# 	"""Monitor processes matching PROCESS_NAME and log memory usage."""
# 	process_list = []
# 	process_memory_log = {}
# 	csv_filename = f'process_memory_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
#
# 	# Set up CSV file and headers
# 	with open(csv_filename, 'w', newline='') as csvfile:
# 		csv_writer = csv.writer(csvfile)
# 		csv_writer.writerow(['Timestamp', 'PID', 'Process Name', 'Memory Usage (MB)'])
#
# 	click.echo("Monitoring processes. Press Ctrl+C to stop.")
# 	try:
# 		while True:
# 			# Track rows for terminal positioning
# 			n = 0
#
# 			# Re-check for matching processes
# 			for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
# 				try:
# 					if process_name.lower() in proc.info['name'].lower():
# 						# Add new process to list if not already tracked
# 						if proc.info['pid'] not in process_memory_log:
# 							process_list.append(proc.info['pid'])
# 							process_memory_log[proc.info['pid']] = []
#
# 						# Get memory usage in MB
# 						memory_usage_mb = proc.info['memory_info'].rss / (1024 * 1024)
#
# 						# Append memory usage to log
# 						process_memory_log[proc.info['pid']].append(memory_usage_mb)
#
# 						# Print to terminal
# 						click.echo(f'\x1b[{n + 5};1H{proc.info["pid"]}\t{proc.info["name"]}\t{memory_usage_mb:.2f} MB', nl=False)
# 						n += 1
#
# 						# Write to CSV file
# 						with open(csv_filename, 'a', newline='') as csvfile:
# 							csv_writer = csv.writer(csvfile)
# 							csv_writer.writerow([datetime.now().isoformat(), proc.info['pid'], proc.info['name'], memory_usage_mb])
# 				except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
# 					continue
#
# 			# Wait for the specified interval
# 			time.sleep(interval)
#
# 	except KeyboardInterrupt:
# 		click.echo("\nMonitoring stopped. Data written to CSV file.")
# 		click.echo(f"CSV file saved as: {csv_filename}")
#
#
# if __name__ == '__main__':
# 	print('\x12b[2J\x1b[1;1H')
# 	monitor_process()


class mydict(dict):
	def __init__(__s,*a,**k):
		super().__init__(*a,**k)

md=mydict()
sd=dict()
args=[md,sd]
argtypes=[dict,list]
argistype = [([a, type(a)], True) for a in args if type(a) in argtypes]
print(argistype)
argistype=[i for i in [*zip([[a,t] for a in args for t in argtypes],[*map(lambda at:isinstance(*at),[[a,t] for a in args for t in argtypes])])] if i[-1] is True]
print(argistype)
