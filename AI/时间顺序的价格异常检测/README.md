##
 Time Series of Price Anomaly Detection

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

+ Select one single hotel which has the most data point property_id = 104517 .

+ Select visitor_location_country_id = 219 , as we know from the another analysis that country id 219 is the Unites States. The reason we do that is to unify the price_usd column. Since different countries have different conventions regarding displaying taxes and fees and the value may be per night or for the whole stay. And we know that price displayed to US visitors is always per night and without taxes.

+ Select search_room_count = 1.

+ Select the features we need: date_time, price_usd, srch_booking_window, srch_saturday_night_bool.


    expedia = pd.read_csv('expedia_train.csv')
    df = expedia.loc[expedia['prop_id'] == 104517]
    df = df.loc[df['srch_room_count'] == 1]
    df = df.loc[df['visitor_location_country_id'] == 219]
    df = df[['date_time', 'price_usd', 'srch_booking_window', 'srch_saturday_night_bool']]
After slice and dice, this is the data we will be working with:

    df.info()


At this point, we have detected one extreme anomaly which was the Max price_usd at 5584.

If an individual data instance can be considered as anomalous with respect to the rest of the data, we call it Point Anomalies (e.g. purchase with large transaction value). We could go back to check the log to see what was it about. After a little bit investigation, I guess it was either a mistake or user searched a presidential suite by accident and had no intention to book or view. In order to find more anomalies that are not extreme, I decided to remove this one.

expedia.loc[(expedia['price_usd'] == 5584) & (expedia['visitor_location_country_id'] == 219)]


At this point, I am sure you have found that we are missing something, that is, we do not know what room type a user searched for, the price for a standard room could be very different with the price for a King bed room with Ocean View. Keep this in mind, for the demonstration purpose, we have to continue.

### Time Series Visualizations
 
    df.plot(x='date_time', y='price_usd', figsize=(12,6))
    plt.xlabel('Date time')
    plt.ylabel('Price in USD')
    plt.title('Time Series of room price by date time of search');

    a = df.loc[df['srch_saturday_night_bool'] == 0, 'price_usd']
    b = df.loc[df['srch_saturday_night_bool'] == 1, 'price_usd']
    plt.figure(figsize=(10, 6))
    plt.hist(a, bins = 50, alpha=0.5, label='Search Non-Sat Night')
    plt.hist(b, bins = 50, alpha=0.5, label='Search Sat Night')
    plt.legend(loc='upper right')
    plt.xlabel('Price')
    plt.ylabel('Count')
    plt.show();


In general, the price is more stable and lower when searching Non-Saturday night. And the price goes up when searching Saturday night. Seems this property gets popular during the weekend.

### Clustering-Based Anomaly Detection

    k-means algorithm


k-means is a widely used clustering algorithm. It creates ‘k’ similar clusters of data points. Data instances that fall outside of these groups could potentially be marked as anomalies. Before we start k-means clustering, we use elbow method to determine the optimal number of clusters.



