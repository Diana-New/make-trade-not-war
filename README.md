# Make Trade, Not War

This repo contains supporting resources for a big data project titled *Make Trade, Not War*, carried out by Gordon Xiang, Huahao Zhou, and Daniel Zhao. We undertook this project as the final project for Professor William King's Fall 2018 course at Yale University's Jackson Institute for Global Affairs, *Big Data and Global Policies* (GLBL 849).

The project centers on tracking government news sources over the source of the last two years (at time of writing) to analyze the texts' attitude towards the trade war. We scrape three news sources: press releases found on the White House.gov website, People's Daily, and China Daily, the former of which represents the official viewpoint of the United States government and the latter two of which serves as the official mouthpiece of the Chinese government. We then track how sentiment contained in these articles changes over time and extract the most common keywords used in each corpus.

The `scrapers` folder contains the Python code we used to scrape the text of all three sites, the `scrapedText` folder contains the raw unprocessed .csv files that we obtained from the scrapers, and the `analysis` folder contains the RMarkdown script we used to pre-process the text, analyze the data, and generate the output graphs.

Please contact iamdanzhao@gmail.com if you would like to read the full text or have questions about the code. You may use the code for your own purposes, but all code is provided as-is.
