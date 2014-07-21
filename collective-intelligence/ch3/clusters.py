# coding=utf-8

from cluster import bicluster


def readfile(filename):
    lines = [line for line in file(filename)]
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


from math import sqrt


def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0

    return 1.0 - num / den


def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # initially clust is all the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # Check cache
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # calculate average of two clusters
        mergevec = [
            (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0
            for i in range(len(clust[0].vec))
        ]

        # create new cluster
        newcluster = bicluster(mergevec,
                               left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]],
                               distance=closest,
                               id=currentclustid)

        # cluster ids that werent in the originial set are -ve
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def run():
    blognames, words, data = readfile('blogdata.txt')
    clust = hcluster(data)
    printclust(clust, labels=blognames)


def printclust(clust, labels=None, n=0):
    # indent to make hierarchy
    for i in range(n): print ' ',
    if clust.id < 0:
        # -ve means branch
        print('-')
    else:
        # +ve is endpoint
        if labels == None:
            print(clust.id)
        else:
            print(labels[clust.id])

    # Print left right
    if clust.left != None: printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None: printclust(clust.right, labels=labels, n=n + 1)


if __name__ == '__main__':
    run()