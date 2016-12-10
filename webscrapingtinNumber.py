import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import sys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
import dropbox
import datetime
#import warnings

#warnings.filterwarnings('error')
homepath = str(os.getcwd() )

def fun(tin_num) :
    
    os.environ["webdriver.chrome.driver"] = homepath + '/chromedriver' # set the os environ attribute webdriver.chrome.driver where chromedriver is installed

    driver = webdriver.Chrome() #the browser...and it opens 
    driver.set_page_load_timeout(30)  #if the page doesnot load within 30 sec, then TimeOut exception occurs 
    search_page_url = "http://www.tinxsys.com/TinxsysInternetWeb/searchByTin_Inter.jsp" #url to open the page to be scraped
    try:
        driver.get(search_page_url) #load the url into the browser
        search_box = driver.find_element_by_name("tinNumber") #fetch the input field where the tinNumber has to be enetered to be seached
        search_btn = driver.find_element_by_name("Submit2") #fetch the Search btn to take action of searching
        #tin_num = raw_input("Enter the tin number :")  #take the input from the user
        search_box.send_keys(tin_num)  #send the input to the search box
        search_btn.click()      #click on the search button
        #time.sleep(5)       #let the user actually see somethin
        
        src_code = driver.page_source
        driver.close()      #close the browser
        
        soup = BeautifulSoup(src_code)

        key_tag = soup.findAll('td',{'class' : 'tdGrey'})       #all key tags 
        key = []
        
        val_tag = soup.findAll('td',{'class' : 'tdWhite'})   #all key values
        val = []
        
        for _key,_value in zip(key_tag,val_tag) :
            temp1 = _key.getText().strip()
            temp2 = _value.getText().strip()
            key.append(temp1.replace(u'\xa0',u'').replace(u'\n',u'').replace(u'  ',u'')) 
            val.append(temp2.replace(u'\xa0',u'').replace(u'\n',u'').replace(u'  ',u'')) 
        

        if len(soup.findAll('table')[2].findAll('tr')) == 1 :
            print "\n\n\n\n\n\n\n\nTin number is not valid"
            return
        
        
             
        length = len(key)   #length of total number of key value pairs
        os.chdir(homepath)
        if not os.path.isdir('temp') :          #check if the directory where test file is to be stored already  exists
            os.makedirs('temp')                     #if directory doesn't exists,make a new one
        os.chdir('temp')
        file_name = str( val[0] ) + '.txt'
        with open(file_name,'w') as f :             #create the text document and write the details into the file
            for i in xrange(0,length,1) :
                f.write('{0} : {1}\n'.format(key[i],val[i]))

        print "\n\n\n\n\n\n\n\nTin no. is valid."
    except TimeoutException as ex:
        print "Timeout due to Network Error  "# + str(ex)
        return
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return
    try :
        os.chdir(homepath)
        app_key = 'remzyqx4qjlt8ou'    # app-key of the dropbox apis
        app_secret = '0taw5wy0xz0k9my'  # app-secret of the dropbox apis
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        authorize_url = flow.start()                #generates the authorization url


        #Now starts the process, where user authorizes the scipt the access to  user's dropbox
        driver = webdriver.Chrome()     #instance of chrome browser
        driver.get(authorize_url)       #load the authorization url in the instance of the above browser
        code = raw_input("Enter the authorization code here to store the details in dropbox : ").strip()  #enter your authorization code through console
        driver.close()      #close the browser
        access_token, user_id = flow.finish(str(code))     #fetch the access token
        client = dropbox.client.DropboxClient(access_token)         #create an instance of dropbox
        path = homepath + '/temp/'          
        file = open(path + file_name, 'rb')        #fetch the file to be uploaded

        dt = datetime.datetime.now()
        timestamp = '{0:%d}-{0:%m}-{0:%Y}-{0:%I}-{0:%M}-{0:%S}-{0:%p}'.format(dt)           #create a timestamp to name the new directory inside dropbox

        response = client.put_file(timestamp + '/'+ file_name , file)  #while creating new directories if necessary, place the file in the given directory
        file.close()
        print "\n\n\n\n\nCongrats " +file_name + " has been uploaded successfull in folder : " + timestamp 
        return
    except :
        print "\n\n\n\n\nOops! Error!"
        return

if __name__ == '__main__':
    fun(str(raw_input("Enter Tin No. :")))
