import pandas as pd #csv 모듈
from selenium import webdriver #셀레니움 모듈
import time    #지연시간 모듈
import sys  #파일 읽기,쓰기 모듈
import re   #정규식 모듈

link_list_load = []
All_Data = []

driver = webdriver.Chrome('./chromedriver.exe') #드라이버 경로
driver.implicitly_wait(3)#지연시간 설정

f = open("./list.txt", 'r') #링크주소 파일 오픈

while True:        
    temp = []       #임시 데이터 저장
    line = f.readline()     #텍스트파일 라인읽기
    if not line: break      #공백이 나올 때 까지 반복하고 종료
    temp.append(line)       #temp로 line 값 치환
    link_list_load.extend(temp)     #link_list로 temp 값 대입
#while 끝
f.close     #list.txt 닫기

load = 0    #변수 초기화
for try_crawling in link_list_load:
    
    temp_Data = []
    
    load_url = ("".join(link_list_load[load]))   # link_list에 있는 load번째에 있는 주소 1개씩 들고오기
    load += 1           #load 변수 증가
    temp_Data.append(load)
    print('반복횟수: ',load)
    
    url = (load_url)    #read_list 값을 지정
    driver.get(url)     #셀레니움에 주소 값 입력
    temp_Data.append(url)
    print('\n',url)    

    try:    
        Brand = driver.find_element_by_xpath('//*[@id="bylineInfo"]').text #브랜드 정보 로드
        temp_Data.append(Brand) #브랜드 정보 저장
        print('Brand: ',Brand) 

    except:
        print('에러:브랜드 정보를 찾을 수 없음')    #에러 출력
        temp_Data.append('')
        pass
    #try 끝

    try:
        Product_Name = driver.find_element_by_xpath('//*[@id="productTitle"]').text #제품이름 로드
        temp_Data.append(Product_Name) #제품 이름 저장
        print('Product Name: ',Product_Name)

    except:
        print('에러:제품 이름을 찾을 수 없음')    #에러 출력
        temp_Data.append('')
        pass
    #try 끝

    Category = ('DongSeo University') #카테고리 지정
    temp_Data.append(Category) #카테고리 저장

    try: 
        Price = driver.find_element_by_id('price').text #가격 로드
        Product_Price = re.findall('([0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[\.]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9])',Price) #가격 숫자 추출
        temp_Data.append(Product_Price[0]) #가격 저장
        print('Price: ',Product_Price[0])
        
    except:
        print('에러:가격 정보를 찾을 수 없음')    #에러 출력
        temp_Data.append('')
        pass
    #try 끝

    try:
        
        Product_Info = driver.find_element_by_xpath('//*[@id="detail-bullets"]/table/tbody/tr/td').text #상품정보 내역 로드
        Product_Dimensions_str1 = re.findall('Product Dimensions:.+',Product_Info) #상품 규격 리페달링
        Product_Dimensions_str2 = ("".join(map(str, Product_Dimensions_str1))) 
        Product_Dimensions_str3 = re.findall('([0-9]*[0-9]*[0-9]*[\.]*[0-9]*[0-9]*[0-9]*[ ][x][ ][0-9]*[0-9]*[0-9]*[\.]*[0-9]*[0-9]*[0-9]*[ ][x][ ][0-9]*[0-9]*[0-9]*[\.]*[0-9]*[0-9]*[0-9])',Product_Dimensions_str2) #숫자 추출
        Product_Dimensions_str4 = ("".join(map(str, Product_Dimensions_str3))) #문자화
        print('Dimensions: ',Product_Dimensions_str4) 
        Product_Dimensions = re.findall('([0-9]*[0-9]*[0-9]*[\.]*[0-9]*[0-9]*[0-9])',Product_Dimensions_str4) #규격 로드

        Dimensions_loading = 0

        Dimensions = []
        for load_Dimensions in Product_Dimensions: #추출 된 제품 규격을 로드
            temp = []
            temp.append(Product_Dimensions[Dimensions_loading])
            Dimensions_loading += 1
            Dimensions.extend(temp) 
        #load_Dimensions for 문 끝
    
        temp_Data.extend(Dimensions)

        Dimensions_Conversion_2 = []
        Dimensions_Conversion = [float(i) for i in Dimensions]
        size = ((Dimensions_Conversion[0]*Dimensions_Conversion[1]*Dimensions_Conversion[2])/166) #온즈 규격 변환율 연산
        temp_Data.append(size)
        Dimensions_Conversion_2.append(size) # 연산결과 저장

    except:
        print('에러: 규격 정보를 찾을 수 없음')    #에러 출력
        temp_Data.append('')
        temp_Data.append('')
        temp_Data.append('')
        temp_Data.append(0)
        pass #멈추지 않고 진행 (except 문끝)
    #try 끝
           
    try:
        Shipping_Weight_str1 = re.findall('Shipping Weight:.+',Product_Info)
        Shipping_Weight_str2 = (",\n".join(map(str, Shipping_Weight_str1))) #추출 된 무게 정보 로드
        Shipping_Weight = re.findall('([ ][0-9]*[0-9]*[0-9]*[\.]*[0-9]*[0-9]*[0-9]*[ ][A-z][A-z][A-z][A-z][A-z][A-z])',Shipping_Weight_str2) #무게 정보에서 숫자 추출
        temp_Data.append(Shipping_Weight[0])
        print('Shipping_Weight: ',Shipping_Weight[0])

        Shipping_Weight_str3 = ("".join(map(str, Shipping_Weight)))

        Shipping_Weight_str4 = 'pounds' #파운드 문자열 추출
        Shipping_Weight_str5 = 'ounces' #온즈 문자열 추출

        Shipping_Weight_select = []
        
        if Shipping_Weight_str4 in Shipping_Weight_str3: #판단 Shipping_Weight_Conversion[0] / 16 한 값의 큰 값의 규격으로 저장
            Shipping_Weight_num = re.findall('([0-9]*[0-9]*[0-9]*[\.]*[0-9]*[0-9]*[0-9])',Shipping_Weight_str3)
            temp_Data.append(Shipping_Weight_num[0])
            Shipping_Weight_select.append(Shipping_Weight_num[0])
            
        elif Shipping_Weight_str5 in Shipping_Weight_str3:
            Shipping_Weight_num = re.findall('([0-9]*[0-9]*[0-9]*[\.]*[0-9]*[0-9]*[0-9])',Shipping_Weight_str3)
            Shipping_Weight_Conversion = [float(i) for i in Shipping_Weight_num]
            Ounces_Conversion_Pound = (Shipping_Weight_Conversion[0] / 16)
            temp_Data.append(Ounces_Conversion_Pound)
            Shipping_Weight_select.extend(Shipping_Weight_num)
            
        else:
            temp_Data.append('')
            
    except:
        print('에러: 무게 정보를 찾을 수 없음')    #에러 출력
        temp_Data.append('')
        temp_Data.append('')
        pass #멈추지 않고 진행 (except 문끝) 
    #try 끝
    
    try:
        Dimension = [float(i) for i in Dimensions_Conversion_2] #예외처리
        ShippingWeight = [float(i) for i in Shipping_Weight_select]

        Dimensions_Conversion_2 = []
        Shipping_Weight_select = []
    
        if Dimension > ShippingWeight:
            temp_Data.append(Dimension[0])
        else:
            temp_Data.append(ShippingWeight[0])
    except:
        print('에러:제품 정보를 찾을 수 없음')   #에러 출력
        temp_Data.append('')
        pass #멈추지 않고 진행 (except 문끝)
    #try 끝
    
    try:
        Asins = re.findall(r'/[^/]+/dp/([^"?/]+)', url) #asin넘버 추출
        temp_Data.append(Asins[0])
        print('Asins: ', Asins[0])
        
    except:
        print('에러:ASIN 정보를 찾을 수 없음')    #에러 출력
        temp_Data.append('')
        pass #멈추지 않고 진행 (except 문끝)
    #try 끝
    
    main_img = [] #이미지 추출
    main_image_load = driver.find_element_by_id('landingImage')
    main_img_get = main_image_load.get_attribute('src')
    main_img.append(main_img_get)
    
    img_link = []
    img_html = []

    try:

        driver.find_element_by_xpath('//*[@id="imgTagWrapperId"]').click()    #이미지 클릭
    
        for load_img in range(100):#100번 반복
            driver.find_element_by_xpath('//*[@id="ivImage_{}"]'.format(load_img)).click()   #다른 이미지 변경
            #time.sleep(2)
            img = driver.find_element_by_xpath('//*[@id="ivLargeImage"]/img').get_attribute('src')     #확대이미지 주소 추출
            
            img_link.append(img)
            print('link: ',img)

            image_html = ('<img src="'+img+'" width="860" align="center"/><br>')   
            img_html.append(image_html)
            print('html link: ',image_html)
        
        #load_img for 문 끝
            
    except:
        print('에러: 이미지를 찾을 수 없음')    #에러 출력
        pass #멈추지 않고 진행
    #try 끝
    
    main_image = ("".join(map(str, main_img)))
    Image_link = (",\n".join(map(str, img_link)))
    Image_html = ("\n".join(map(str, img_html)))

    temp_Data.append(main_image)
    temp_Data.append(Image_link)
    temp_Data.append(Image_html)
    All_Data.append(temp_Data)

    Write = pd.DataFrame(All_Data) #배열의 데이터 엑셀화
    Write.columns = ['#','Link', 'Brand', 'Product Name', 'Category','Price','Dimensions','','','Dimensions /166','Weight','oz/16 = pound','','ASIN','Main Image','image1','img2']
    Write.to_excel('test.xlsx', index=False, encoding="utf-8-sig")
    
print('크롤링 완료') #완료 알림
driver.close()
