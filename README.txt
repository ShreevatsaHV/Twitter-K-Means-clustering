To Compile and Run the code:

Use the below command format:
There may be two cases:
1. tweets-k-means <numberOfClusters> <initialSeedsFile> <TweetsDataFile> <outputFile>
2. In this case, if numberOfClusters is not given, then 25 will be default taken
	tweets-k-means <initialSeedsFile> <TweetsDataFile> <outputFile>

For Example:
1. python tweets-k-means.py 25 InitialSeeds.txt Tweets.json tweets-k-means-output.txt
2. python tweets-k-means.py InitialSeeds.txt Tweets.json tweets-k-means-output.txt
