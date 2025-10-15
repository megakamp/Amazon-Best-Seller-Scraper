📘 Overview

Amazon Best Seller Scraper is a lightweight Python automation tool that automatically collects the latest top-selling products from Amazon’s Best Sellers page.
It helps developers, analysts, and e-commerce enthusiasts track popular products and price trends without manual browsing.

The script uses web scraping, data formatting, and scheduling to provide continuous updates on trending products — perfect for market research, competitive analysis, or data-driven decision-making.

⚙️ Key Features

Automated Web Scraping:
Uses requests and BeautifulSoup to fetch and parse Amazon’s Best Sellers page.

Top 10 Products:
Extracts the first 10 products with their names and prices for a concise view.

Data Presentation:
Displays results in a clean pandas DataFrame format directly in the console.

Scheduled Execution:
Utilizes the schedule library to re-run scraping every 12 hours, keeping data fresh and relevant.

Error-Tolerant Structure:
Handles missing price data gracefully and continues scraping even if certain elements aren’t found.

🧩 Technologies Used

Python 3

Libraries:

requests → to send HTTP requests

BeautifulSoup4 → to parse HTML data

pandas → to organize and display product data

schedule → to automate scraping intervals

time → for controlled looping and task timing

🧠 How It Works

The script sends a GET request to Amazon’s Best Sellers page using a custom user-agent.

It parses the HTML structure to extract product names and prices.

Results are stored in a Python list and displayed as a DataFrame.

The scraping function runs automatically every 12 hours via the scheduling module.

🚀 Use Cases

Market and competitor analysis.

Tracking trending products for e-commerce research.

Building datasets for machine learning or data visualization projects.

Educational use for learning web scraping and automation.

🧠 Future Enhancements

Export scraped data to CSV/Excel.

Integrate email or Discord notifications when new bestsellers appear.

Support for multiple Amazon regions (e.g., .co.uk, .de, .ca).

Add proxy rotation and user-agent randomization to prevent request blocking.
