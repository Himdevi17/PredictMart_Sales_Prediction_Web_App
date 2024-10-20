from flask import Flask,render_template,request
from flask_cors import cross_origin
import pickle
from datetime import date

# import requests
app = Flask(__name__)

with open("rf_model.pkl","rb") as model_file:
    model=pickle.load(model_file)

@app.route('/')
@cross_origin()
def index():
   return render_template('home.html')


@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
       output=0
       Item_Weight=float(request.form["Item_Weight"])
       
       Item_Fat_Content=request.form["Item_Fat_Content"]

       Item_Visibility=float(request.form["Item_Visibility"])

       Item_Type=request.form["Item_Type"]
       
       Item_MRP=int(request.form["Item_MRP"])
       
       Outlet_Establishment_Year=int(request.form["Outlet_Establishment_Year"])
       
       Outlet_Size=request.form["Outlet_Size"]
       
       Outlet_Location_Type=request.form["Outlet_Location_Type"]
       
       Outlet_Type=request.form["Outlet_Type"]
      #  Item_Weight=float(request.form["Item_Weight"])
      #  Item_Fat_Content = request.form["Item_Fat_Content"]
      #  Item_Visibility = float(request.form["Item_Visibility"])
      #  Item_Type_Combined = data["Item_Type"] 
      #  Item_MRP  =data["Item_MRP"]
      #  Outlet_Establishment_Year= data["Outlet_Establishment_Year"]  
      #  Outlet_Size = data["Outlet_Size"] 
      #  Outlet_Location_Type=data["Outlet_Location_Type"] 
      #  Outlet_Type =data["Outlet_Type"]
       #Outlet years
       todays_date = date.today()
       Outlet_Years=todays_date.year-Outlet_Establishment_Year
       Item_Visibility_MeanRatio=1.061884


       if Item_Fat_Content=="Low Fat":
        Item_Fat_Content_0=1
        Item_Fat_Content_1=0
        Item_Fat_Content_2=0  
       elif Item_Fat_Content=="Non-Edible":
        Item_Fat_Content_0=0
        Item_Fat_Content_1=1
        Item_Fat_Content_2=0   
       else:
        Item_Fat_Content_0=0
        Item_Fat_Content_1=0
        Item_Fat_Content_2=1  

       if Outlet_Size=="High":
        Outlet_Size_0 = 1       
        Outlet_Size_1 = 0               
        Outlet_Size_2 = 0
       elif Outlet_Size=="Medium":
        Outlet_Size_0 = 0       
        Outlet_Size_1 = 1              
        Outlet_Size_2 = 0
       else:
        Outlet_Size_0 = 0       
        Outlet_Size_1 = 0               
        Outlet_Size_2 = 1

    #Outlet Location Type
       if Outlet_Location_Type=="Tier 1":
        Outlet_Location_Type_0 = 1   
        Outlet_Location_Type_1 = 0       
        Outlet_Location_Type_2 = 0
       elif Outlet_Location_Type=="Tier 2":
        Outlet_Location_Type_0 = 0   
        Outlet_Location_Type_1 = 1       
        Outlet_Location_Type_2 = 0
       else:
        Outlet_Location_Type_0 = 0   
        Outlet_Location_Type_1 = 0       
        Outlet_Location_Type_2 = 1

    #Outlet Type
       if Outlet_Type=="Glocery Store":
        Outlet_Type_0 = 1             
        Outlet_Type_1 = 0             
        Outlet_Type_2 = 0            
        Outlet_Type_3 = 0
       elif Outlet_Type=="Supermarket Type1":
        Outlet_Type_0 = 0             
        Outlet_Type_1 = 1            
        Outlet_Type_2 = 0            
        Outlet_Type_3 = 0
       elif Outlet_Type=="Supermarket Type2":
        Outlet_Type_0 = 0             
        Outlet_Type_1 = 0             
        Outlet_Type_2 = 1            
        Outlet_Type_3 = 0
       else:
        Outlet_Type_0 = 0             
        Outlet_Type_1 = 0             
        Outlet_Type_2 = 0            
        Outlet_Type_3 = 1
    #Item Type  
       if Item_Type=="Drinks":
        Item_Type_0 = 1     
        Item_Type_1 = 0       
        Item_Type_2 = 0
       elif Item_Type=="Food":
        Item_Type_0 = 0     
        Item_Type_1 = 1       
        Item_Type_2 = 0
       else:
        Item_Type_0 = 0     
        Item_Type_1 = 0       
        Item_Type_2 = 1
       features=[Item_Weight,Item_Visibility,Item_MRP,Outlet_Years,Item_Visibility_MeanRatio,
        Item_Fat_Content_0,Item_Fat_Content_1,
        Item_Fat_Content_2,Outlet_Size_0,Outlet_Size_1,Outlet_Size_2,
        Outlet_Location_Type_0,Outlet_Location_Type_1,Outlet_Location_Type_2,
        Outlet_Type_0,Outlet_Type_1,Outlet_Type_2,Outlet_Type_3,Item_Type_0,
        Item_Type_1,Item_Type_2] 

       try:
        #Predicting Sales
        result=model.predict([features])[0]
        print("good")
        print(result)
        r=str(result)
        return render_template('home.html',output=r)
       except:
         return render_template('home.html',output=r)


    return render_template("home.html")

if __name__ == '__main__':
   
   app.run(debug = False)
   