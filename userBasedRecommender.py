#encoding:utf-8
from math import sqrt

# 加载数据
def loadData():
    sexSet = {' F ': 0, ' M ': 1}
    i,j = 0,0
    trainSet = {}
    testSet = {}
    trainRecoSet = {}
    jobSet = {}
    addressSet = {}

    TrainFile = './data/db_test(1).txt'

    # 加载训练集
    for line in open(TrainFile):
        (userID, sex, age, job, address, trainRecoItems,white) = line.split('|')
        # 需要根据职业和地区的购买力，事先在数据集上对其进行降序排序
        if job not in jobSet:
            jobSet[job] = i
            i += 1
        if address not in addressSet:
            addressSet[address] = j
            j += 1

        sex = sexSet[sex] * 0.5
        age = int(age) * 0.02
        job = jobSet[job] * 0.2
        address = addressSet[address] * 0.2

        trainSet.setdefault(userID,{})
        trainSet[userID].setdefault('sex',sex)
        trainSet[userID].setdefault('age', age)
        trainSet[userID].setdefault('job', job)
        trainSet[userID].setdefault('address',address)

        trainRecoSet.setdefault(userID,trainRecoItems.split('::'))

    return trainSet,testSet,trainRecoSet

# Pearson相关系数法衡量用户相似度
# # 计算一个用户的平均评分
# def getAverageRating(user):
#     average  = (sum(trainSet[user].values()) * 1.0) / len(trainSet[user].keys())
#     return average
#
# # 计算用户相似度
# def getUserSim(trainSet):
#     userSim = {}
#
#     for u in trainSet.keys():  # 对每个用户u
#         for n in trainSet.keys():  # 对每个用户n
#             userSim.setdefault(u,{})
#             average_u_rate,average_n_rate = getAverageRating(u),getAverageRating(n)  # 获取用户u,n各项平均得分
#             userSim[u].setdefault(n,0)
#
#             part1 = 0  # 皮尔逊相关系数的分子部分
#             part2 = 0  # 皮尔逊相关系数的分母的一部分
#             part3 = 0  # 皮尔逊相关系数的分母的一部分
#
#             for i in trainSet[u].keys():
#                 urating = trainSet[u][i]
#                 nrating = trainSet[n][i]
#                 part1 += (urating - average_u_rate) * (nrating - average_n_rate) * 1.0
#                 part2 += pow(urating - average_u_rate,2) * 1.0
#                 part3 += pow(nrating - average_n_rate,2) * 1.0
#
#             part2 = sqrt(part2)
#             part3 = sqrt(part3)
#
#             if part2 == 0 or part3 == 0:
#                 userSim[u][n] = 0  # 若分母为0，相似度为0
#             elif u == n:
#                 del (userSim[u][n])
#             else:
#                 userSim[u][n] = round(part1 / (part2 * part3),4)
#     # print(userSim)
#     return userSim

# 余弦相似度法衡量用户相似度
def getUserSim(trainSet):
    userSim = {}

    for u in trainSet.keys():  # 对每个用户u
        for n in trainSet.keys():  # 对每个用户n
            sum,A,B = 0,0,0
            userSim.setdefault(u,{})
            userSim[u].setdefault(n,0)
            for i in trainSet[u].keys():
                urating = trainSet[u][i]
                nrating = trainSet[n][i]
                sum += urating * nrating
                A += urating ** 2
                B += nrating ** 2

            if u == n:
                del (userSim[u][n])
            else:
                userSim[u][n] = round(sum / (sqrt(A) * sqrt(B)),4)  # 计算用户间余弦相似度

    return userSim

# 寻找用户最近邻并生成推荐结果
def getRecommendation(N,trainSet,userSim,trainRecoSet):
    recoResult = {}

    for user in trainSet.keys():  # 对每个用户
        allitems = []
        for key, v in enumerate(trainRecoSet[user]):
            # 只对目标用户没有的产品类别进行推荐
            if v == '  ':

                simUser = sorted(userSim[user].items(),key = lambda x:x[1],reverse=True)[0:N]  # 得到用户N近邻列表

                for i in range(N):
                    if (trainRecoSet[simUser[i][0]][key] != '  '):
                        allitems.append(trainRecoSet[simUser[i][0]][key])
                simUser.append(allitems)

                simUser[-1] = list(set(simUser[-1]))  # 推荐商品去重

                recoResult.update({user:simUser})  # 根据N近邻列表推荐商品

    return recoResult



if __name__ == '__main__':

    print('正在加载数据……')
    trainSet,testSet,trainRecoSet = loadData()

    print('正在计算用户相似度……')
    userSim = getUserSim(trainSet)

    print('正在寻找最近邻并推荐……')
    recoResult = getRecommendation(3,trainSet,userSim,trainRecoSet)

    with open("result.txt", "w") as f:
        for key,value in recoResult.items():
            f.write('用户ID：' + key + '|' + ' 近似用户:' + str(value[0:3]) + ' 推荐产品：' + str(value[-1]))
            f.write('\n')
            f.write('\n')

    print('推荐完毕')

    # print(recoResult['1'][:3]) # 针对UserId为'6'的用户的推荐结果查询
