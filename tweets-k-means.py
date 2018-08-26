import json
import sys

def sse(clusters, centroid_values, tweet_data):
    result = 0
    for cluster in clusters:
        for tweet in clusters[cluster]:
            result += jaccard_distance(tweet_data[tweet], tweet_data[centroid_values[cluster]]) ** 2
    return result
	
def wordCounts(word_list):
    counts = {}
    for word in word_list:
        if word in counts:
            counts[word] = counts[word] + 1
        else:
            counts[word] = 1
    return counts

def intersection(bucket_1, bucket_2):
    result = 0
    for word in bucket_1:
        while bucket_1[word] != 0 and word in bucket_2:
            if word in bucket_2:
                bucket_2[word] = bucket_2[word] - 1
                bucket_1[word] = bucket_1[word] - 1
                if bucket_2[word] == 0:
                    bucket_2.pop(word, None)
                result += 1
    return result

def union(bucket_1, bucket_2):
    result = 0
    for word in bucket_1:				
        if word in bucket_2:
            result = result + max(bucket_1[word], bucket_2[word])
            bucket_2.pop(word, None)
        else:
            result = result + bucket_1[word]
    for word in bucket_2:
        result = result + bucket_2[word]
    return result


def jaccard_distance(tweet_a, tweet_b):
    bucket_a = wordCounts(tweet_a)
    bucket_b = wordCounts(tweet_b)
    bucket_union = union(dict(bucket_a), dict(bucket_b))
    bucket_intersect = intersection(dict(bucket_a), dict(bucket_b))
    return 1.0 - bucket_intersect*1.0/bucket_union
	
def recalculateCentroid(cluster, tweet_data):
    cent = cluster[0]
    min_distance = 1
    for tweet in cluster:
        total_distance = 0
        for other_tweet in cluster:
            total_distance = total_distance + jaccard_distance(tweet_data[tweet],tweet_data[other_tweet])
        mean_distance = total_distance*1.0/len(cluster)
        if mean_distance < min_distance:
            min_distance = mean_distance
            cent = tweet
    return cent
	
def writeClusters(tweet_centroids, tweet_data):
    clusters = {}
    for index in range(len(tweet_centroids)):
        clusters[index] = []
    for tweet in tweet_data:
        min_jaccard_dist = 1
        cluster = 0
        for cent in tweet_centroids:
            dist_to_centroid = 1
            dist_to_centroid = jaccard_distance(tweet_data[tweet_centroids[cent]],tweet_data[tweet])
            if dist_to_centroid < min_jaccard_dist:
                min_jaccard_dist = dist_to_centroid
                cluster = cent
        clusters[cluster].append(tweet)
    return clusters

tweetsData = {}
tweetCentroids = {}
new_centroids = {}

if len(sys.argv) >= 5:
    numOfClusters = int(sys.argv[1])
    initialSeedsFile = sys.argv[2]
    tweetsDataFile = sys.argv[3]
    outputFile = sys.argv[4]
elif len(sys.argv) == 4:
    print ("Using default: ")
    print ("Number of Clusters : 25")
    numOfClusters = 25
    initialSeedsFile = sys.argv[1]
    tweetsDataFile = sys.argv[2]
    outputFile = sys.argv[3]

with open(initialSeedsFile) as tweet_centroid_file:
    centroids = tweet_centroid_file.read().rsplit(",\n")
    if len(centroids) == numOfClusters:
        for idx in range(0, numOfClusters):
            tweetCentroids[idx] = centroids[idx]
    else:
        print ("Error: It seems the Initial seed file contains more/less values than the clusters entered")
        sys.exit(1)
		
with open(tweetsDataFile) as tweet_data_file:
    for line in tweet_data_file:
        tweet = json.loads(line)
        tweet["text"].split()
        tweetsData[str(tweet["id"])] = tweet["text"]

while True:
    clusters = writeClusters(tweetCentroids, tweetsData)
    for cluster in clusters:
        new_centroids[cluster] = recalculateCentroid(clusters[cluster], tweetsData)
    if new_centroids == tweetCentroids:
        print ("SSE: " + str(sse(clusters, new_centroids, tweetsData)))
        break
    else:
        tweetCentroids = new_centroids

fileToOutput = open(outputFile, 'w')
fileToOutput.write("SSE Value: ")
fileToOutput.write(str(sse(clusters, new_centroids, tweetsData)))
fileToOutput.write("\n\nClusters:\n")
for cluster in clusters:
    fileToOutput.write(str(cluster))
    fileToOutput.write("\t")
    for tweet in clusters[cluster]:
        fileToOutput.write(tweet)
        fileToOutput.write(", ")
    fileToOutput.write("\n")