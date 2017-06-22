
#jindonghtml
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re,datetime,random
ItemList=[]
class JD:
	 
	def __init__(self,mainurl,num):
		self.mainurl=mainurl
		self.num=num
		

	#shou ye feng lei 
	def GetStartUrl(self,mainurl):
		MainClassification0=[]
		html=urlopen(mainurl)
		MainUrlBsobj=BeautifulSoup(html,from_encoding='UTF-8')
		MainClassification1=MainUrlBsobj.findAll("a",{"target":"_blank","class":"cate_menu_lk"},href=re.compile(".*\.jd\.com.*"))
		for classi in MainClassification1:
			if 'href' in classi.attrs:
				MainClassification0.append(classi.attrs['href'][2:])
		MainClassification1=[]
		return MainClassification0[0]
	#get yi ji ye mian URL
	def GetOneLevel(self,onelevelurl):
		OneLevelList=[]
		OneLevelHtml=urlopen("https://"+onelevelurl)
		OneLevelBsobj=BeautifulSoup(OneLevelHtml)
		OneLevelScript=OneLevelBsobj.find("div",{"class":"mod_container"}).findAll("script")
		pattern = re.compile(r'"URL":"(https:\\/\\/list.*?)"', re.I | re.M)
		OneLevelJs=OneLevelScript[1].get_text()
		OneLevelUrl=pattern.findall(OneLevelJs)
		
		return OneLevelUrl[1].replace('\\','')

	def GetItemList(self,itemlisturl):
		

		ItemId=[]
		ItemListHtml=urlopen(itemlisturl)
		ItemListBsobj=BeautifulSoup(ItemListHtml,from_encoding='gb18030')
		
		ItemLists=ItemListBsobj.findAll("a",{"title":""},href=re.compile("^//item\.jd\.com/(.{7})\.html"))
		pagenums=ItemListBsobj.find("span",{"class":"p-skip"}).find('b').get_text()
		ItemListNextUrl="https://list.jd.com"+ItemListBsobj.find("a",{"class":"pn-next"}).attrs['href']
		ItemLists=ItemLists[::2]
		for itemurl in ItemLists:
			if 'href' in itemurl.attrs:
				itemurl="https:"+itemurl.attrs['href']
				ItemList.append(itemurl)
				ItemId.append(itemurl[-12:-5])
		#return ItemList[0]

		
	def GetItemDetail(self,ItemUrl):
		num=self.num
		
		ItemHtml=urlopen(ItemUrl)
		ItemBsobj=BeautifulSoup(ItemHtml,from_encoding="gb18030")
		ItemTitle=ItemBsobj.title
		ItemTitle=ItemTitle.get_text()
		ItemTitle=ItemTitle[:-16]
		print(ItemTitle)
		itemid=ItemUrl[-12:-5]
		PriceUrl="http://p.3.cn/prices/mgets?skuIds=J_"+str(itemid)
		PriceOpen=urlopen(PriceUrl).read().decode('UTF-8')
		ItemPrice=json.loads(PriceOpen)
		ItemPrice=ItemPrice[0]['p']
		print("价格是：",ItemPrice,"元")	
		packing=ItemBsobj.findAll("div",{"class":"Ptable-item"})
		for x in packing:
			packing0=x.find("h3")
			packing1=x.findAll("dt")
			packing2=x.findAll("dd")
			print(packing0.get_text())
			for i in range(len(packing1)):
				print(packing1[i].get_text(),packing2[i].string)
			print('\n')
		page0=1
		NewCommentList=[]
		NewUserNameList=[]
		count=0
		while(page0<4):
			page1=str(page0)
			html=urlopen("https://club.jd.com/review/"+itemid+"-3-"+page1+".html")
			bsObj=BeautifulSoup(html,from_encoding="gb18030")
			Commentlist=bsObj.findAll("div",{"class":"comment-content"})
			usernamelist=bsObj.findAll("div",{"class":"u-name"})
			for comment in Commentlist:
				comment0=comment.find("dt").get_text()
				if comment0=="心　　得：":
					comment1=comment.find("dd").get_text().replace("\n","")
					NewCommentList.append(comment1)
		
				if comment0=="标　　签：":
					comment2=comment.findAll("dd")
					comment3=comment2[1].get_text().replace("\n","")
					NewCommentList.append(comment3)	
			commentlen=len(NewCommentList)
			for username in usernamelist:
				username=username.get_text().replace(" ","")
				username=username[:-1]
				username=username.strip()
				NewUserNameList.append(username)
			print("第",page0,"页",'\n')
			if count==0:
				count=commentlen
				for i in range(0,commentlen-1):
					#print("第",page0,"页",'\n')
					print(NewUserNameList[i],":",NewCommentList[i])
			else :
				for i in range(count,commentlen-1):
					#print("第",page0,"页",'\n')
					print(NewUserNameList[i],":",NewCommentList[i])
				count=commentlen
			page0=page0+1
			print('')
	def Start(self):
		onelevelurl= self.GetStartUrl(mainurl)
		
		print("------------------正在爬取首页-------------------")
		
		itemlisturl=self.GetOneLevel(onelevelurl)
		print("-----------------正在解析一级分类标签--------------------")
		
		#print(itemlisturl)
		self.GetItemList(itemlisturl)
		#print(len(ItemList))
		print("-----------------正在获取商品详情信息-----------------------")
		#print(ItemUrl)
		for i in range(self.num):
			print("商品",i+1)
			self.GetItemDetail(ItemList[i])


mainurl="https://www.jd.com/"
spider=JD(mainurl,3)
spider.Start()

