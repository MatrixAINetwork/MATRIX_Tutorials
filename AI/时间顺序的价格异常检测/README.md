## Time Series of Price Anomaly Detection

### Anomaly detection detects data points in data that does not fit well with the rest of the data


Also known as outlier detection, anomaly detection is a data mining process used to determine types of anomalies found in a data set and to determine details about their occurrences. Automatic anomaly detection is critical in today’s world where the sheer volume of data makes it impossible to tag outliers manually. Auto anomaly detection has a wide range of applications such as fraud detection, system health monitoring, fault detection, and event detection systems in sensor networks, and so on.

But I would like to apply anomaly detection to hotel room prices. The reason is somewhat selfish.

Have you had experience that, lets say, you travel to a certain destination for business regularly and you always stay at the same hotel. While most of the time, the room rate is almost similar but occasionally for the same hotel, same room type, the rate is unacceptably high, and you’d have to change to another hotel because your travel allowance does not cover that rate. I had been through this several times and this makes me think, what if we could create a model to detect this kind of price anomaly automatically?

Of course there are circumstance that some anomaly happens only once a life time and we have known them in advance and probably it will not happen the same time in the future years, such as the ridiculous hotel prices in Atlanta on February 2 to February 4, 2019.


In this post, I will explore different anomaly detection techniques and our goal is to search for anomalies in the time series of hotel room prices with unsupervised learning. Let’s get started!




### The Data

It is very hard to get the data, I was able to get some but the data is not perfect.

The data we are going to use is a subset of [Personalize Expedia Hotel Searches](https://www.kaggle.com/c/expedia-personalized-sort/data) data set that can be found [here](https://www.kaggle.com/c/expedia-personalized-sort/data).

We are going to slice a subset of the training.csv set like so:

Select one single hotel which has the most data point property_id = 104517 .
Select visitor_location_country_id = 219 , as we know from the another analysis that country id 219 is the Unites States. The reason we do that is to unify the price_usd column. Since different countries have different conventions regarding displaying taxes and fees and the value may be per night or for the whole stay. And we know that price displayed to US visitors is always per night and without taxes.
Select search_room_count = 1.
Select the features we need: date_time, price_usd, srch_booking_window, srch_saturday_night_bool.