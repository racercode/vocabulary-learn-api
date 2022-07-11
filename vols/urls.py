from django.urls import path, include
from vols import views

urlpatterns = [
    path('latest_categories/<int:pk>/', views.latest_categories.as_view()),
    # 最新的單字庫 pk:第幾頁
    path('get_sentences/<int:id>/', views.get_sentences.as_view()),
    # 獲取每個單字庫的單字的隨機句子 id: 單字庫編碼
    path('get_category/<int:id>', views.get_category.as_view()),
    # 獲取每個單字庫的單字的資訊 id: 單字庫編碼
    path('check/', views.check.as_view()),
    # 提交答案 ( 先不用管他 )
    path('add_category/', views.add_category.as_view()),
    # 新增資料庫 ( params: {name:'', description:'', vol_list:''})
    path('all_categories/', views.all_categories.as_view()),
    # 所有資料庫資訊
    path('edit_category/<int:id>', views.edit_category.as_view()),
    
]