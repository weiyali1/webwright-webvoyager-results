# Task Date Updates

## Submission and source

- Submission: `webvoyager-2026-11-03`.
- Base collection: [browser-control-fable-5 from omxyz/webvoyager](https://github.com/omxyz/webvoyager/tree/df42681582be8125c5296473ad8efcd86f926cb6/benchmark/data/browser-control-fable-5).
- Fixed upstream comparison commit: `df42681582be8125c5296473ad8efcd86f926cb6`.
- Upstream task file: [WebVoyager_data.jsonl](https://github.com/omxyz/webvoyager/blob/df42681582be8125c5296473ad8efcd86f926cb6/benchmark/data/browser-control-fable-5/WebVoyager_data.jsonl).
- SHA-256 of that upstream file: `3be3e58768816c8a0249ba48c4dec5d25a91047a2f9bb0e028bcbba73669ac40`.
- Exact executed and evaluated task definitions: [`tasks/`](tasks/).

Before execution, stale dates in date-sensitive tasks were updated. The agent and external judge used the same updated task instructions. This document records every task-instruction difference between the fixed upstream reference and the task definitions published with this submission.

The fixed commit above identifies the upstream comparison reference; the published files in `tasks/` define the exact collection used for this evaluation.

## Verified scope of changes

Both collections contain the same 615 unique task IDs across 15 websites. There are no added, removed, or duplicate task IDs. Website names, starting URLs, and every field other than the instruction field (`ques`) match the upstream reference.

Of the 615 instruction strings, 566 are identical character for character and 49 differ. All differences in those 49 strings are English month-name substitutions: 79 substitutions in total. Day numbers, years, and all text outside those month names are unchanged. The updated month names are November or December; the explicit years remain 2026.

| Website | Total tasks | Unchanged instructions | Updated instructions |
| --- | ---: | ---: | ---: |
| Allrecipes | 40 | 40 | 0 |
| Amazon | 40 | 40 | 0 |
| Apple | 40 | 40 | 0 |
| ArXiv | 43 | 43 | 0 |
| BBC News | 39 | 39 | 0 |
| Booking | 40 | 21 | 19 |
| Cambridge Dictionary | 41 | 41 | 0 |
| Coursera | 40 | 40 | 0 |
| ESPN | 44 | 44 | 0 |
| GitHub | 41 | 41 | 0 |
| Google Flights | 40 | 10 | 30 |
| Google Map | 40 | 40 | 0 |
| Google Search | 42 | 42 | 0 |
| Huggingface | 39 | 39 | 0 |
| Wolfram Alpha | 46 | 46 | 0 |
| **Total** | **615** | **566** | **49** |

## Updated-task index

Month substitutions are listed in their order of appearance in each instruction.

| Task ID | Month substitutions: upstream → executed |
| --- | --- |
| Booking--5 | October → November; October → November |
| Booking--19 | August → November; August → November |
| Booking--21 | July → November |
| Booking--22 | June → November; June → November |
| Booking--23 | June → November |
| Booking--25 | August → November; August → November |
| Booking--26 | July → November |
| Booking--27 | June → November; July → December |
| Booking--28 | June → November; June → November |
| Booking--29 | July → November; July → November |
| Booking--30 | July → November; July → November |
| Booking--31 | July → November |
| Booking--34 | July → November; July → November |
| Booking--36 | July → November; July → November |
| Booking--37 | July → November; July → November |
| Booking--38 | June → November; July → December |
| Booking--39 | July → November |
| Booking--40 | July → November; July → November |
| Booking--42 | July → November; July → November |
| Google Flights--1 | June → November |
| Google Flights--10 | April → November; May → December |
| Google Flights--11 | July → November; July → November |
| Google Flights--12 | June → November; July → December |
| Google Flights--13 | July → November; July → November |
| Google Flights--14 | July → November; July → November |
| Google Flights--15 | July → November; July → November |
| Google Flights--17 | June → November; July → December |
| Google Flights--18 | June → November; July → December |
| Google Flights--19 | July → November |
| Google Flights--21 | July → November |
| Google Flights--22 | June → November; June → November |
| Google Flights--23 | July → November |
| Google Flights--24 | July → November; July → November |
| Google Flights--25 | July → November |
| Google Flights--26 | July → November; July → November |
| Google Flights--27 | July → November |
| Google Flights--28 | July → November; August → December |
| Google Flights--29 | July → November; July → November |
| Google Flights--30 | July → November |
| Google Flights--31 | July → November |
| Google Flights--32 | July → November; July → November |
| Google Flights--33 | July → November |
| Google Flights--34 | July → November |
| Google Flights--35 | July → November |
| Google Flights--36 | July → November; August → December |
| Google Flights--37 | June → November; July → December |
| Google Flights--38 | July → November |
| Google Flights--39 | July → November |
| Google Flights--41 | July → November |

## Full task instructions before and after

The instruction strings below are reproduced verbatim, including source spelling and punctuation.

### Booking

Executed task definitions: [`tasks/Booking.json`](tasks/Booking.json).

#### Booking--5

**Upstream instruction**

> Search a hotel with free WiFi and air conditioning in Bali from October 1 to October 4, 2026.

**Executed and evaluated instruction**

> Search a hotel with free WiFi and air conditioning in Bali from November 1 to November 4, 2026.

#### Booking--19

**Upstream instruction**

> Look for a hotel with customer ratings above an 8.0 in Paris, France for a weekend stay from August 18, 2026, to August 20, 2026, and list top three suggestions based on user reviews.

**Executed and evaluated instruction**

> Look for a hotel with customer ratings above an 8.0 in Paris, France for a weekend stay from November 18, 2026, to November 20, 2026, and list top three suggestions based on user reviews.

#### Booking--21

**Upstream instruction**

> Find a hotel in Sydney with a rating of 8 or higher, providing free Wi-Fi and parking, available for a four-night stay starting on July 10, 2026.

**Executed and evaluated instruction**

> Find a hotel in Sydney with a rating of 8 or higher, providing free Wi-Fi and parking, available for a four-night stay starting on November 10, 2026.

#### Booking--22

**Upstream instruction**

> Search for a hotel in Amsterdam with a customer review score of 9 or higher, offering bicycle rentals, for a week-long stay from June 15 to June 22, 2026, for two adults.

**Executed and evaluated instruction**

> Search for a hotel in Amsterdam with a customer review score of 9 or higher, offering bicycle rentals, for a week-long stay from November 15 to November 22, 2026, for two adults.

#### Booking--23

**Upstream instruction**

> Identify a hotel in Tokyo with a spa and wellness center, rated 9 or above, with availability for a five-night stay starting on June 20, 2026. Check if free cancellation is offered.

**Executed and evaluated instruction**

> Identify a hotel in Tokyo with a spa and wellness center, rated 9 or above, with availability for a five-night stay starting on November 20, 2026. Check if free cancellation is offered.

#### Booking--25

**Upstream instruction**

> Search for a hotel in Lisbon with airport shuttle, rated 8.5 or above, available for a six-night stay from August 1 to August 7, 2026, for two adults, breakfast included.

**Executed and evaluated instruction**

> Search for a hotel in Lisbon with airport shuttle, rated 8.5 or above, available for a six-night stay from November 1 to November 7, 2026, for two adults, breakfast included.

#### Booking--26

**Upstream instruction**

> Check Booking.com for a 3-star hotel or higher in Paris with a guest rating above 8.0 and available parking for dates July 20-23, 2026.

**Executed and evaluated instruction**

> Check Booking.com for a 3-star hotel or higher in Paris with a guest rating above 8.0 and available parking for dates November 20-23, 2026.

#### Booking--27

**Upstream instruction**

> Locate a hotel in Melbourne offering free parking and free WiFi, for a stay from June 28 to July 4, 2026.

**Executed and evaluated instruction**

> Locate a hotel in Melbourne offering free parking and free WiFi, for a stay from November 28 to December 4, 2026.

#### Booking--28

**Upstream instruction**

> Find a hotel in Dubai with a swimming pool, for a week-long stay from June 22 to June 29, 2026.

**Executed and evaluated instruction**

> Find a hotel in Dubai with a swimming pool, for a week-long stay from November 22 to November 29, 2026.

#### Booking--29

**Upstream instruction**

> Search for a hotel in Toronto with a fitness center and a rating of 8+, available for a two-night stay from July 5 to July 7, 2026.

**Executed and evaluated instruction**

> Search for a hotel in Toronto with a fitness center and a rating of 8+, available for a two-night stay from November 5 to November 7, 2026.

#### Booking--30

**Upstream instruction**

> Search for hotels in London from July 20 to July 23, 2026, on Booking. How many hotels are left after applying the Breakfast included and Fitness center filters?

**Executed and evaluated instruction**

> Search for hotels in London from November 20 to November 23, 2026, on Booking. How many hotels are left after applying the Breakfast included and Fitness center filters?

#### Booking--31

**Upstream instruction**

> Search for hotels in Rio de Janeiro from July 1-7, 2026, check the Brands filter to see which brand has the most hotels and which brand has the fewest.

**Executed and evaluated instruction**

> Search for hotels in Rio de Janeiro from November 1-7, 2026, check the Brands filter to see which brand has the most hotels and which brand has the fewest.

#### Booking--34

**Upstream instruction**

> Search for a hotel in Berlin available for a three-night stay from July 15 to July 18, 2026, for one adult. Tell me the price in USD and CNY for the three-night stay.

**Executed and evaluated instruction**

> Search for a hotel in Berlin available for a three-night stay from November 15 to November 18, 2026, for one adult. Tell me the price in USD and CNY for the three-night stay.

#### Booking--36

**Upstream instruction**

> Search for a budget hotel in Rome under $100 per night for one adult from July 20 to July 23, 2026. Sort the results by price, identify if any of top three results offer breakfast.

**Executed and evaluated instruction**

> Search for a budget hotel in Rome under $100 per night for one adult from November 20 to November 23, 2026. Sort the results by price, identify if any of top three results offer breakfast.

#### Booking--37

**Upstream instruction**

> Search for a resort (not hotel) in Bali, detailing the available dates between July 20, 2026, and July 25, 2026, and checking any provided tour or cultural experiences.

**Executed and evaluated instruction**

> Search for a resort (not hotel) in Bali, detailing the available dates between November 20, 2026, and November 25, 2026, and checking any provided tour or cultural experiences.

#### Booking--38

**Upstream instruction**

> Look up Vienna hotel options with availability for a 4-night stay from June 28 to July 2, 2026, with amenities that include a Parking, breakfast included, and a rating of 8+ on Booking.com.

**Executed and evaluated instruction**

> Look up Vienna hotel options with availability for a 4-night stay from November 28 to December 2, 2026, with amenities that include a Parking, breakfast included, and a rating of 8+ on Booking.com.

#### Booking--39

**Upstream instruction**

> Find a pet-friendly hotel with parking available in downtown Toronto for the stay of July 24-26, 2026.

**Executed and evaluated instruction**

> Find a pet-friendly hotel with parking available in downtown Toronto for the stay of November 24-26, 2026.

#### Booking--40

**Upstream instruction**

> I need to choose a hotel in Shenzhen, please select date (6 July to 8 July 2026) and click the search button. How much it costs when convert the price to Chinese Yuan on the page.

**Executed and evaluated instruction**

> I need to choose a hotel in Shenzhen, please select date (6 November to 8 November 2026) and click the search button. How much it costs when convert the price to Chinese Yuan on the page.

#### Booking--42

**Upstream instruction**

> Search for a hotel in Hokkaido for the period July 1 to July 7, 2026, with a rating of 9+, check out its user reviews, which categories are greater than 9 and which are less than 9?

**Executed and evaluated instruction**

> Search for a hotel in Hokkaido for the period November 1 to November 7, 2026, with a rating of 9+, check out its user reviews, which categories are greater than 9 and which are less than 9?

### Google Flights

Executed task definitions: [`tasks/google_flight.json`](tasks/google_flight.json).

#### Google Flights--1

**Upstream instruction**

> Show me the list of one-way flights on June 17, 2026 from Chicago to Paris.

**Executed and evaluated instruction**

> Show me the list of one-way flights on November 17, 2026 from Chicago to Paris.

#### Google Flights--10

**Upstream instruction**

> Locate the cheapest round-trip flights from New York to Tokyo leaving on April 25, 2026, and returning on May 15, 2026.

**Executed and evaluated instruction**

> Locate the cheapest round-trip flights from New York to Tokyo leaving on November 25, 2026, and returning on December 15, 2026.

#### Google Flights--11

**Upstream instruction**

> Compare the prices for round-trip flights from New York to Tokyo for a departure on July 10, 2026, and a return on July 24, 2026, and select the option with the least number of stops.

**Executed and evaluated instruction**

> Compare the prices for round-trip flights from New York to Tokyo for a departure on November 10, 2026, and a return on November 24, 2026, and select the option with the least number of stops.

#### Google Flights--12

**Upstream instruction**

> Find the best-priced round-trip flight from New York to London leaving on June 25, 2026, and returning on July 5, 2026, with one stop or fewer.

**Executed and evaluated instruction**

> Find the best-priced round-trip flight from New York to London leaving on November 25, 2026, and returning on December 5, 2026, with one stop or fewer.

#### Google Flights--13

**Upstream instruction**

> Find the cheapest round-trip flight option from New York City to Tokyo for a departure on July 10, 2026, and a return on July 24, 2026.

**Executed and evaluated instruction**

> Find the cheapest round-trip flight option from New York City to Tokyo for a departure on November 10, 2026, and a return on November 24, 2026.

#### Google Flights--14

**Upstream instruction**

> Compare flight options and find the lowest round trip fare from New York to London departing on July 10, 2026, and returning on July 17, 2026.

**Executed and evaluated instruction**

> Compare flight options and find the lowest round trip fare from New York to London departing on November 10, 2026, and returning on November 17, 2026.

#### Google Flights--15

**Upstream instruction**

> Compare the prices and total duration of non-stop flights from New York to Tokyo Narita Airport departing on July 12th, 2026, and returning on July 26th, 2026.

**Executed and evaluated instruction**

> Compare the prices and total duration of non-stop flights from New York to Tokyo Narita Airport departing on November 12th, 2026, and returning on November 26th, 2026.

#### Google Flights--17

**Upstream instruction**

> Find the cheapest round-trip flight from New York to Paris leaving on June 27, 2026, and returning on July 10, 2026.

**Executed and evaluated instruction**

> Find the cheapest round-trip flight from New York to Paris leaving on November 27, 2026, and returning on December 10, 2026.

#### Google Flights--18

**Upstream instruction**

> Compare flight options from New York to Tokyo for a round trip leaving on June 25, 2026, and returning on July 15, 2026, for one adult. Prioritize the comparisons by the shortest travel time.

**Executed and evaluated instruction**

> Compare flight options from New York to Tokyo for a round trip leaving on November 25, 2026, and returning on December 15, 2026, for one adult. Prioritize the comparisons by the shortest travel time.

#### Google Flights--19

**Upstream instruction**

> Find the cheapest one-way flight from London to Paris, departing on July 25, 2026. Include the airline, total travel time, and layovers for the chosen flight.

**Executed and evaluated instruction**

> Find the cheapest one-way flight from London to Paris, departing on November 25, 2026. Include the airline, total travel time, and layovers for the chosen flight.

#### Google Flights--21

**Upstream instruction**

> Locate the lowest-priced one-way flight from Tokyo to Sydney for an adult, departing o6 July 25, 2026, and include the flight duration and number of layovers.

**Executed and evaluated instruction**

> Locate the lowest-priced one-way flight from Tokyo to Sydney for an adult, departing o6 November 25, 2026, and include the flight duration and number of layovers.

#### Google Flights--22

**Upstream instruction**

> Find a round-trip flight from Rio de Janeiro to Los Angeles, leaving on June 15, 2026, and returning on June 22, 2026, and select the option with the least carbon dioxide emissions.

**Executed and evaluated instruction**

> Find a round-trip flight from Rio de Janeiro to Los Angeles, leaving on November 15, 2026, and returning on November 22, 2026, and select the option with the least carbon dioxide emissions.

#### Google Flights--23

**Upstream instruction**

> Search for a one-way flight from Mumbai to Vancouver on July 28, 2026, filtering the results to show only 1-stop flights.

**Executed and evaluated instruction**

> Search for a one-way flight from Mumbai to Vancouver on November 28, 2026, filtering the results to show only 1-stop flights.

#### Google Flights--24

**Upstream instruction**

> Compare prices for economy class round-trip flights from Dubai to Rome, departing on July 1, 2026, and returning on July 8, 2026, and select the option with the fewest stops.

**Executed and evaluated instruction**

> Compare prices for economy class round-trip flights from Dubai to Rome, departing on November 1, 2026, and returning on November 8, 2026, and select the option with the fewest stops.

#### Google Flights--25

**Upstream instruction**

> Find a one-way business class flight from Buenos Aires to Amsterdam on July 10, 2026, and provide the details of the flight with the shortest duration.

**Executed and evaluated instruction**

> Find a one-way business class flight from Buenos Aires to Amsterdam on November 10, 2026, and provide the details of the flight with the shortest duration.

#### Google Flights--26

**Upstream instruction**

> Search for the cheapest round-trip flights from Bangkok to Madrid, leaving on July 26, 2026, and returning on July 28, 2026, and provide options under $1000.

**Executed and evaluated instruction**

> Search for the cheapest round-trip flights from Bangkok to Madrid, leaving on November 26, 2026, and returning on November 28, 2026, and provide options under $1000.

#### Google Flights--27

**Upstream instruction**

> Locate a one-way flight from Johannesburg to Toronto on July 30, 2026, for one adult, and analyze the price trends for the following month.

**Executed and evaluated instruction**

> Locate a one-way flight from Johannesburg to Toronto on November 30, 2026, for one adult, and analyze the price trends for the following month.

#### Google Flights--28

**Upstream instruction**

> Find the best-priced round-trip flight from Seattle to Paris, departing on July 27, 2026, and returning on August 1, 2026, with a maximum of one stop.

**Executed and evaluated instruction**

> Find the best-priced round-trip flight from Seattle to Paris, departing on November 27, 2026, and returning on December 1, 2026, with a maximum of one stop.

#### Google Flights--29

**Upstream instruction**

> Compare the prices and total travel time of non-stop flights from Mexico City to Frankfurt, departing on July 5, 2026, and returning on July 15, 2026.

**Executed and evaluated instruction**

> Compare the prices and total travel time of non-stop flights from Mexico City to Frankfurt, departing on November 5, 2026, and returning on November 15, 2026.

#### Google Flights--30

**Upstream instruction**

> Find the most affordable one-way flight from Cape Town to Singapore, departing on July 20, 2026, and include the airline and total number of layovers.

**Executed and evaluated instruction**

> Find the most affordable one-way flight from Cape Town to Singapore, departing on November 20, 2026, and include the airline and total number of layovers.

#### Google Flights--31

**Upstream instruction**

> Find a one-way economy flight from Auckland to Honolulu on July 25, 2026, browse the full page and display a flight option with the most stops.

**Executed and evaluated instruction**

> Find a one-way economy flight from Auckland to Honolulu on November 25, 2026, browse the full page and display a flight option with the most stops.

#### Google Flights--32

**Upstream instruction**

> Search for round-trip flights from Stockholm to Toronto, departing on July 3, 2026, and returning on July 10, 2026, and sort the results to find the shortest total travel time.

**Executed and evaluated instruction**

> Search for round-trip flights from Stockholm to Toronto, departing on November 3, 2026, and returning on November 10, 2026, and sort the results to find the shortest total travel time.

#### Google Flights--33

**Upstream instruction**

> Find a one-way flight from Shanghai to Vancouver on July 27, 2026, and compare the options based on carbon dioxide emissions.

**Executed and evaluated instruction**

> Find a one-way flight from Shanghai to Vancouver on November 27, 2026, and compare the options based on carbon dioxide emissions.

#### Google Flights--34

**Upstream instruction**

> Compare business class flight options from Lisbon to Singapore for a one-way trip on July 15, 2026, select one of the flights and see which websites offer its booking options. Which one is the cheapest.

**Executed and evaluated instruction**

> Compare business class flight options from Lisbon to Singapore for a one-way trip on November 15, 2026, select one of the flights and see which websites offer its booking options. Which one is the cheapest.

#### Google Flights--35

**Upstream instruction**

> Find the lowest-priced one-way flight from Cairo to Montreal on July 21, 2026, including the total travel time and number of stops.

**Executed and evaluated instruction**

> Find the lowest-priced one-way flight from Cairo to Montreal on November 21, 2026, including the total travel time and number of stops.

#### Google Flights--36

**Upstream instruction**

> Search for round-trip flights from Helsinki to New Delhi, departing on July 28, 2026, and returning on August 4, 2026, and filter the results to show only flights under $1000.

**Executed and evaluated instruction**

> Search for round-trip flights from Helsinki to New Delhi, departing on November 28, 2026, and returning on December 4, 2026, and filter the results to show only flights under $1000.

#### Google Flights--37

**Upstream instruction**

> Locate a round-trip flight from Buenos Aires to Beijing, leaving on June 28, 2026, and returning on July 3, 2026, check out one of the options and tell me if the airline for my return flight is the same as my departure flight.

**Executed and evaluated instruction**

> Locate a round-trip flight from Buenos Aires to Beijing, leaving on November 28, 2026, and returning on December 3, 2026, check out one of the options and tell me if the airline for my return flight is the same as my departure flight.

#### Google Flights--38

**Upstream instruction**

> Compare the prices and flight durations for economy class flights from Oslo to Dubai, departing on July 8, 2026, and show the options with no more than two layovers.

**Executed and evaluated instruction**

> Compare the prices and flight durations for economy class flights from Oslo to Dubai, departing on November 8, 2026, and show the options with no more than two layovers.

#### Google Flights--39

**Upstream instruction**

> Find a one-way flight from Prague to a city in Japan on July 20, 2026, which city in Japan is cheaper to go to, Tokyo or a certain city in Hokkaido?

**Executed and evaluated instruction**

> Find a one-way flight from Prague to a city in Japan on November 20, 2026, which city in Japan is cheaper to go to, Tokyo or a certain city in Hokkaido?

#### Google Flights--41

**Upstream instruction**

> Choose one way business class ticket from Hong Kong to Glacier National Park on 6 July 2026, offering a 1 stop ticket.

**Executed and evaluated instruction**

> Choose one way business class ticket from Hong Kong to Glacier National Park on 6 November 2026, offering a 1 stop ticket.

This disclosure records the task definitions used for the submitted execution and evaluation artifacts.
