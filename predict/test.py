from sklearn import datasets
iris = datasets.load_iris()
data = iris.data[:100]
print (data)
label = iris.target[:100]
print (label)

from sklearn.cross_validation import train_test_split
train_x, test_x, train_y, test_y = train_test_split(data, label, random_state=0)
import xgboost as xgb
dtrain=xgb.DMatrix(train_x,label=train_y)
dtest=xgb.DMatrix(test_x)

params={'booster':'gbtree',
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'max_depth':4,
    'lambda':10,
    'subsample':0.75,
    'colsample_bytree':0.75,
    'min_child_weight':2,
    'eta': 0.025,
    'seed':0,
    'nthread':8,
     'silent':1}

watchlist = [(dtrain,'train')]
bst=xgb.train(params,dtrain,num_boost_round=100,evals=watchlist)

bst.save_model('0001.model')

ypred=bst.predict(dtest)

# 设置阈值, 输出一些评价指标
y_pred = (ypred >= 0.5)*1

from sklearn import metrics
print ('AUC: %.4f' % metrics.roc_auc_score(test_y,ypred))
print ('ACC: %.4f' % metrics.accuracy_score(test_y,y_pred))
print ('Recall: %.4f' % metrics.recall_score(test_y,y_pred))
print ('F1-score: %.4f' %metrics.f1_score(test_y,y_pred))
print ('Precesion: %.4f' %metrics.precision_score(test_y,y_pred))
metrics.confusion_matrix(test_y,y_pred)


ypred = bst.predict(dtest)
ypred
#ypred_leaf = bst.predict(dtest, pred_leaf=True)
#ypred_leaf
#xgb.to_graphviz(bst, num_trees=0)
#可视化第一棵树的生成情况
#直接输出模型的迭代工程
#bst.dump_model("model.txt")
